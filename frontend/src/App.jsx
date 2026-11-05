import { useEffect, useState } from 'react'
import DealerList from './components/DealerList.jsx'
import DealerDetail from './components/DealerDetail.jsx'
import ReviewForm from './components/ReviewForm.jsx'
import Register from './components/Register.jsx'
import { API_BASE, api } from './api.js'

// Tiny state-based routing (no router dependency):
//   { view: 'list' }
//   { view: 'detail', dealerId }
//   { view: 'review', dealerId }
//   { view: 'register' }
export default function App() {
  const [route, setRoute] = useState({ view: 'list' })
  const [me, setMe] = useState({ authenticated: false, username: null })

  const goList = () => setRoute({ view: 'list' })
  const goDetail = (dealerId) => setRoute({ view: 'detail', dealerId })
  const goReview = (dealerId) => setRoute({ view: 'review', dealerId })
  const goRegister = () => setRoute({ view: 'register' })

  // Who is logged in? Re-checked on every navigation change so the nav
  // bar (Login/Register vs username/Logout) is always current.
  useEffect(() => {
    let cancelled = false
    api.getMe().then((m) => { if (!cancelled) setMe(m) })
    return () => { cancelled = true }
  }, [route])

  return (
    <>
      <header className="header">
        <h1>Best Cars Dealership</h1>
        <nav>
          <button onClick={goList}>Dealers</button>
          <a href={`${API_BASE}/about/`} target="_blank" rel="noreferrer">About Us</a>
          <a href={`${API_BASE}/contact/`} target="_blank" rel="noreferrer">Contact Us</a>
          {me.authenticated ? (
            <>
              <span style={{ alignSelf: 'center' }}>Hi, {me.username}!</span>
              <a href={`${API_BASE}/logout/`}>Logout</a>
            </>
          ) : (
            <>
              <a href={`${API_BASE}/login/`} target="_blank" rel="noreferrer">Login</a>
              <button onClick={goRegister}>Register</button>
            </>
          )}
        </nav>
      </header>
      <main className="main">
        {route.view === 'list' && <DealerList onSelect={goDetail} />}
        {route.view === 'detail' && (
          <DealerDetail
            dealerId={route.dealerId}
            onBack={goList}
            onAddReview={() => goReview(route.dealerId)}
          />
        )}
        {route.view === 'review' && (
          <ReviewForm
            dealerId={route.dealerId}
            onDone={() => goDetail(route.dealerId)}
            onCancel={() => goDetail(route.dealerId)}
          />
        )}
        {route.view === 'register' && (
          <Register onDone={goList} onGoLogin={() => window.open(`${API_BASE}/login/`, '_blank')} />
        )}
      </main>
    </>
  )
}
