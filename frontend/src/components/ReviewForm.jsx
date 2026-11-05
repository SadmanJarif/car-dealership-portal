import { useEffect, useState } from 'react'
import { api, submitReview } from '../api.js'

export default function ReviewForm({ dealerId, onDone, onCancel }) {
  const [dealer, setDealer] = useState(null)
  const [makes, setMakes] = useState([])
  const [form, setForm] = useState({
    name: '', review: '', purchase: false,
    purchase_date: '', car_make: '', car_model: '', car_year: '',
  })
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    let cancelled = false
    api.getDealer(dealerId)
      .then((d) => { if (!cancelled) setDealer(d) })
      .catch((e) => { if (!cancelled) setError(e.message) })
    api.getCarMakes()
      .then((m) => { if (!cancelled) setMakes(m) })
      .catch(() => {})
    return () => { cancelled = true }
  }, [dealerId])

  const set = (field) => (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    setForm((f) => ({ ...f, [field]: value }))
  }

  async function onSubmit(e) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      await submitReview(dealerId, form)
      setSuccess(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (success) {
    return (
      <div className="card">
        <div className="success">Your review was submitted. Thank you!</div>
        <button className="btn" onClick={onDone}>Back to {dealer ? dealer.full_name : 'dealer'}</button>
      </div>
    )
  }

  return (
    <>
      <button className="btn secondary" onClick={onCancel}>← Back to dealer</button>
      <div className="card form" style={{ marginTop: 16 }}>
        <h2>Add a review{dealer ? ` — ${dealer.full_name}` : ''}</h2>
        <p className="muted">
          Reviews are saved through the Django back end, which requires a login.
          If you are not logged in, open the Django site’s login page first, then
          come back here. Submitting without a login will show an error, not a
          fake success.
        </p>
        {error && <div className="error">{error}</div>}
        <form onSubmit={onSubmit}>
          <label htmlFor="rf-name">Your name</label>
          <input id="rf-name" type="text" value={form.name} onChange={set('name')} required />

          <label htmlFor="rf-review">Your review</label>
          <textarea id="rf-review" value={form.review} onChange={set('review')} required />

          <label>
            <input type="checkbox" checked={form.purchase} onChange={set('purchase')} /> I purchased a car here
          </label>

          {form.purchase && (
            <>
              <div className="row">
                <div>
                  <label htmlFor="rf-date">Purchase date</label>
                  <input id="rf-date" type="date" value={form.purchase_date} onChange={set('purchase_date')} />
                </div>
                <div>
                  <label htmlFor="rf-year">Car year</label>
                  <input id="rf-year" type="number" min="1900" max="2100" value={form.car_year} onChange={set('car_year')} />
                </div>
              </div>
              <div className="row">
                <div>
                  <label htmlFor="rf-make">Car make</label>
                  <select id="rf-make" value={form.car_make} onChange={set('car_make')}>
                    <option value="">— select —</option>
                    {makes.map((m) => <option key={m.id} value={m.name}>{m.name}</option>)}
                  </select>
                </div>
                <div>
                  <label htmlFor="rf-model">Car model</label>
                  <input id="rf-model" type="text" value={form.car_model} onChange={set('car_model')} placeholder="e.g. Camry" />
                </div>
              </div>
            </>
          )}

          <div style={{ marginTop: 16 }}>
            <button className="btn" type="submit" disabled={submitting}>
              {submitting ? 'Submitting…' : 'Submit review'}
            </button>{' '}
            <button className="btn secondary" type="button" onClick={onCancel}>Cancel</button>
          </div>
        </form>
      </div>
    </>
  )
}
