import { useState } from 'react'
import { registerUser } from '../api.js'

// React registration page — posts to the Django registration form
// (POST /register/, form-encoded, CSRF protected), exactly as the
// Django site does. On success the new user is logged in by Django
// and the app returns to the dealer list.
export default function Register({ onDone, onGoLogin }) {
  const [form, setForm] = useState({ first_name: '', last_name: '', username: '', email: '', password1: '', password2: '' })
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  async function onSubmit(e) {
    e.preventDefault()
    setError(null)
    if (form.password1 !== form.password2) {
      setError('The two passwords do not match.')
      return
    }
    setSubmitting(true)
    try {
      await registerUser(form)
      onDone()
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="card form">
      <h2>Create an account</h2>
      <p className="muted">
        Registration is handled by the Django back end — the account it
        creates is the same account used to log in and add reviews.
      </p>
      {error && <div className="error">{error}</div>}
      <form onSubmit={onSubmit}>
        <label htmlFor="reg-first-name">First Name</label>
        <input id="reg-first-name" type="text" value={form.first_name} onChange={set('first_name')} required />

        <label htmlFor="reg-last-name">Last Name</label>
        <input id="reg-last-name" type="text" value={form.last_name} onChange={set('last_name')} required />

        <label htmlFor="reg-username">Username</label>
        <input id="reg-username" type="text" value={form.username} onChange={set('username')} required />

        <label htmlFor="reg-email">Email</label>
        <input id="reg-email" type="email" value={form.email} onChange={set('email')} required />

        <label htmlFor="reg-password1">Password</label>
        <input id="reg-password1" type="password" value={form.password1} onChange={set('password1')} required />

        <label htmlFor="reg-password2">Confirm password</label>
        <input id="reg-password2" type="password" value={form.password2} onChange={set('password2')} required />

        <div style={{ marginTop: 16 }}>
          <button className="btn" type="submit" disabled={submitting}>
            {submitting ? 'Creating…' : 'Register'}
          </button>{' '}
          <button className="btn secondary" type="button" onClick={onGoLogin}>Already have an account? Log in</button>
        </div>
      </form>
    </div>
  )
}
