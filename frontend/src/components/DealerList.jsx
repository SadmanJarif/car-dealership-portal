import { useEffect, useState } from 'react'
import { api } from '../api.js'

export default function DealerList({ onSelect }) {
  const [dealers, setDealers] = useState(null)
  const [makes, setMakes] = useState([])
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('')

  useEffect(() => {
    let cancelled = false
    api.getDealers()
      .then((d) => { if (!cancelled) setDealers(d) })
      .catch((e) => { if (!cancelled) setError(e.message) })
    api.getCarMakes()
      .then((m) => { if (!cancelled) setMakes(m) })
      .catch(() => { /* car makes are a bonus strip; dealers are the page */ })
    return () => { cancelled = true }
  }, [])

  if (error) return <div className="error">Could not load dealers: {error}</div>
  if (dealers === null) return <div className="loading">Loading dealers…</div>

  const q = query.trim().toLowerCase()
  const filtered = q
    ? dealers.filter((d) =>
        [d.full_name, d.city, d.state, d.short_name].filter(Boolean).join(' ').toLowerCase().includes(q))
    : dealers

  return (
    <>
      <h2>Our Dealers</h2>
      <input
        className="search"
        type="search"
        placeholder="Search by dealer name, city or state…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {makes.length > 0 && (
        <p className="muted">
          Car makes we carry: {makes.map((m) => m.name).join(', ')}
        </p>
      )}
      {filtered.length === 0 ? (
        <p className="muted">No dealers match “{query}”.</p>
      ) : (
        <div className="dealer-grid">
          {filtered.map((d) => (
            <article key={d.id} className="dealer-card">
              <h3>{d.full_name}</h3>
              <p className="muted">
                {d.address}<br />
                {d.city}, {d.state} {d.zip}
              </p>
              <button className="btn" onClick={() => onSelect(d.id)}>
                View dealer &amp; reviews
              </button>
            </article>
          ))}
        </div>
      )}
    </>
  )
}
