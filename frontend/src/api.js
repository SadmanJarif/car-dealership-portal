// API client for the Django Car Dealership Portal back end
// (~/workspace/course12-capstone, djangoapp/views.py).
//
// Endpoints (all JSON, GET):
//   GET /api/dealers/                  -> [{id, full_name, city, address, state, zip, lat, long, short_name}]
//   GET /api/dealers/<id>/            -> {id, full_name, city, address, state, zip}
//   GET /api/dealers/<id>/reviews/    -> [{name, purchase, purchase_date, car_make, car_model, car_year, sentiment, review}]
//   GET /api/inventory/               -> [{id, name, car_type, year, dealer_id, car_make__name}]
//   GET /api/cars/                    -> [{id, name, description}]
//
//   POST /api/dealers/<id>/reviews/ -> 201, the created review (JSON,
//        login + CSRF required; the Django view also forwards it to the
//        external reviews service via restapis.post_review when configured)
//   POST /dealer/<id>/add-review/    -> form-encoded fallback for the same
//        review (login required, CSRF protected)
//   POST /register/                  -> form-encoded registration
// The submitReview() / registerUser() helpers fetch the Django form page
// first to read its CSRF token, then post with the Django session cookie
// (credentials: 'include'). They only work when the user is logged in to
// the Django site in the same browser (log in at /login/ first) and when
// the React app is served same-origin with the Django back end (Vite proxy
// in dev/preview, or VITE_API_BASE_URL pointing at the Django host with
// matching cookies).

const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

async function getJson(path) {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status} ${res.statusText}`)
  return res.json()
}

export const api = {
  getDealers: () => getJson('/api/dealers/'),
  getDealer: (id) => getJson(`/api/dealers/${id}/`),
  getDealerReviews: (id) => getJson(`/api/dealers/${id}/reviews/`),
  getInventory: () => getJson('/api/inventory/'),
  getCarMakes: () => getJson('/api/cars/'),
  // Who is logged in (Django session)? Drives the nav Login/Register
  // vs username/Logout. Never throws — anonymous on any failure.
  getMe: async () => {
    try {
      const res = await fetch(`${API_BASE}/api/me/`, { credentials: 'include' })
      if (!res.ok) return { authenticated: false, username: null }
      return await res.json()
    } catch {
      return { authenticated: false, username: null }
    }
  },
  // POST a review as JSON to POST /api/dealers/<id>/reviews/
  // (Django api_dealer_reviews, login + CSRF required). Returns the
  // created review on 201.
  postReviewJson: async (dealerId, data, csrfToken) => {
    const res = await fetch(`${API_BASE}/api/dealers/${dealerId}/reviews/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify(data),
    })
    if (res.status === 403) throw new Error('You must log in on the Django site first (open /login/ in this browser, then try again).')
    if (!res.ok) {
      let detail = ''
      try { detail = JSON.stringify(await res.json()) } catch { /* ignore */ }
      throw new Error(`Review submission failed: ${res.status} ${res.statusText}${detail ? ' — ' + detail : ''}`)
    }
    return res.json()
  },
}

function extractCsrfToken(html) {
  const m = html.match(/name=["']csrfmiddlewaretoken["']\s+value=["']([^"']+)["']/)
  return m ? m[1] : null
}

export async function submitReview(dealerId, data) {
  // 1. Load the Django form page to obtain a CSRF token.
  const pageRes = await fetch(`${API_BASE}/dealer/${dealerId}/add-review/`, {
    credentials: 'include',
  })
  if (pageRes.url.includes('/login/')) {
    throw new Error('You must log in on the Django site first (open /login/ in this browser, then try again).')
  }
  if (!pageRes.ok) {
    throw new Error(`Could not load the review form: ${pageRes.status} ${pageRes.statusText}`)
  }
  const token = extractCsrfToken(await pageRes.text())
  if (!token) {
    throw new Error('Could not find a CSRF token on the review form page.')
  }

  // 2. Preferred path: POST the review as JSON to the back-end review
  // endpoint (POST /api/dealers/<id>/reviews/), which saves it locally
  // and forwards it to the external reviews service via
  // restapis.post_review when REVIEWS_API_URL is configured.
  // 3. Fallback: the original form-encoded POST to the Django form view,
  // if the JSON endpoint is unavailable for any reason.
  const payload = {
    name: data.name,
    review: data.review,
    purchase: !!data.purchase,
    purchase_date: data.purchase_date || null,
    car_make: data.car_make || '',
    car_model: data.car_model || '',
    car_year: data.car_year ? Number(data.car_year) : 2024,
  }
  try {
    await api.postReviewJson(dealerId, payload, token)
    return true
  } catch (err) {
    if (/log in/i.test(err.message)) throw err
    // Fall through to the form POST below.
  }

  const body = new URLSearchParams({
    name: data.name,
    review: data.review,
    purchase: data.purchase ? 'on' : '',
    purchase_date: data.purchase_date || '',
    car_make: data.car_make || '',
    car_model: data.car_model || '',
    car_year: data.car_year || '',
  })
  const res = await fetch(`${API_BASE}/dealer/${dealerId}/add-review/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': token,
    },
    body: body.toString(),
  })

  // Django redirects to the dealer detail page on success, and to the
  // login page when the session is not authenticated.
  if (res.url.includes('/login/')) {
    throw new Error('You must log in on the Django site first (open /login/ in this browser, then try again).')
  }
  if (res.status === 403) {
    throw new Error('The back end rejected the review (403, CSRF). Make sure you are logged in and the React app is served same-origin with the Django back end.')
  }
  if (!res.ok) {
    throw new Error(`Review submission failed: ${res.status} ${res.statusText}`)
  }
  return true
}

// Register a new user through the Django registration form
// (POST /register/, form-encoded, CSRF protected). The form page is
// fetched first to read its CSRF token, mirroring submitReview().
export async function registerUser(data) {
  const pageRes = await fetch(`${API_BASE}/register/`, { credentials: 'include' })
  if (!pageRes.ok) throw new Error(`Could not load the registration form: ${pageRes.status} ${pageRes.statusText}`)
  const token = extractCsrfToken(await pageRes.text())
  if (!token) throw new Error('Could not find a CSRF token on the registration form page.')
  const body = new URLSearchParams({
    username: data.username,
    email: data.email,
    password1: data.password1,
    password2: data.password2,
  })
  const res = await fetch(`${API_BASE}/register/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': token,
    },
    body: body.toString(),
  })
  if (!res.ok) throw new Error(`Registration failed: ${res.status} ${res.statusText} — check the username is not taken and the password meets the requirements.`)
  return true
}

export { API_BASE }
