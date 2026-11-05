import { useEffect, useState } from 'react'
import { api } from '../api.js'

function sentimentBadge(sentiment) {
  if (!sentiment) return null
  const s = sentiment.toLowerCase()
  const cls = s === 'positive' ? 'positive' : s === 'negative' ? 'negative' : 'neutral'
  return <span className={`badge ${cls}`}>{sentiment}</span>
}

export default function DealerDetail({ dealerId, onBack, onAddReview }) {
  const [dealer, setDealer] = useState(null)
  const [reviews, setReviews] = useState(null)
  const [inventory, setInventory] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    setDealer(null)
    setReviews(null)
    setError(null)
    api.getDealer(dealerId)
      .then((d) => { if (!cancelled) setDealer(d) })
      .catch((e) => { if (!cancelled) setError(e.message) })
    api.getDealerReviews(dealerId)
      .then((r) => { if (!cancelled) setReviews(r) })
      .catch((e) => { if (!cancelled) setError(e.message) })
    api.getInventory()
      .then((cars) => { if (!cancelled) setInventory(cars.filter((c) => c.dealer_id === dealerId)) })
      .catch(() => { /* inventory is a bonus section; dealer + reviews are the page */ })
    return () => { cancelled = true }
  }, [dealerId])

  if (error) return (
    <>
      <button className="btn secondary" onClick={onBack}>← Back to dealers</button>
      <div className="error">Could not load this dealer: {error}</div>
    </>
  )
  if (dealer === null || reviews === null) return <div className="loading">Loading dealer…</div>

  return (
    <>
      <button className="btn secondary" onClick={onBack}>← Back to dealers</button>
      <div className="card" style={{ marginTop: 16 }}>
        <h2>{dealer.full_name}</h2>
        <p className="muted">
          {dealer.address}<br />
          {dealer.city}, {dealer.state} {dealer.zip}
        </p>
        <button className="btn" onClick={onAddReview}>Add a review</button>
      </div>

      {inventory.length > 0 && (
        <div className="card">
          <h3>Cars in stock here</h3>
          <ul>
            {inventory.map((c) => (
              <li key={c.id}>
                {c.car_make__name} {c.name} ({c.year}) — {c.car_type}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="card">
        <h3>Reviews ({reviews.length})</h3>
        {reviews.length === 0 ? (
          <p className="muted">No reviews yet — be the first to write one.</p>
        ) : (
          reviews.map((r, i) => (
            <article key={i} className="review">
              <strong>{r.name}</strong>
              {sentimentBadge(r.sentiment)}
              <p className="muted">
                {r.purchase ? `Purchased a ${r.car_year || ''} ${r.car_make || ''} ${r.car_model || ''}`.trim() : 'Did not purchase'}
                {r.purchase_date ? ` on ${r.purchase_date}` : ''}
              </p>
              <p>{r.review}</p>
            </article>
          ))
        )}
      </div>
    </>
  )
}
