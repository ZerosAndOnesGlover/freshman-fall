import { useState } from 'react';
import { useNavigate, useLocation, Navigate } from 'react-router-dom';
import { useAuth } from '../auth.jsx';
import { Wordmark } from '../components/Chrome.jsx';

/**
 * The seeded development accounts. The database is local by design; these are
 * printed by the importer too. Change them before this ever leaves the machine.
 */
const DEMO = [
  { role: 'Student', email: 'adebayo.glover@ist.edu', password: 'student2026' },
  { role: 'Instructor', email: 'david.malan@ist.edu', password: 'teach2026' },
  { role: 'Registry (admin)', email: 'registrar@ist.edu', password: 'teach2026' },
];

export default function Login() {
  const { user, login } = useAuth();
  const nav = useNavigate();
  const loc = useLocation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to={loc.state?.from || '/portal'} replace />;

  async function onSubmit(e) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await login(email, password);
      nav(loc.state?.from || '/portal', { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-split">
      <aside className="login-aside">
        <Wordmark />
        <div>
          <span className="eyebrow eyebrow-light">Student &amp; Faculty Portal</span>
          <h2 style={{ marginTop: '0.75rem' }}>Your courses, your work, your marks.</h2>
          <p className="lede" style={{ color: 'rgba(255,255,255,0.7)', marginTop: '1rem', maxWidth: '38ch' }}>
            Read every lecture, hand in coursework, and watch your grade build against the
            rubric your course published on day one.
          </p>
        </div>
        <p className="tiny" style={{ color: 'rgba(255,255,255,0.4)' }}>
          © {new Date().getFullYear()} Institute of Science &amp; Technology
        </p>
      </aside>

      <main className="login-main">
        <form className="login-form" onSubmit={onSubmit}>
          <h1 style={{ fontSize: 'var(--t-xl)' }}>Sign in</h1>
          <p className="small muted" style={{ marginTop: '0.5rem', marginBottom: '2rem' }}>
            Use the address the registry has on file.
          </p>

          {error && <div className="notice notice-error" style={{ marginBottom: '1.25rem' }}>{error}</div>}

          <div className="field">
            <label htmlFor="email">Email address</label>
            <input id="email" className="input" type="email" autoComplete="username"
              value={email} onChange={(e) => setEmail(e.target.value)} required autoFocus />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input id="password" className="input" type="password" autoComplete="current-password"
              value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>

          <button className="btn btn-block" style={{ marginTop: '1.75rem' }} disabled={busy}>
            {busy ? 'Signing in…' : 'Sign in'}
          </button>

          <div className="cred-card">
            <strong style={{ display: 'block', marginBottom: '0.5rem' }}>Development accounts</strong>
            {DEMO.map((d) => (
              <div key={d.email} style={{ marginTop: '0.35rem' }}>
                <span className="muted">{d.role}: </span>
                <button type="button" onClick={() => { setEmail(d.email); setPassword(d.password); }}>
                  {d.email}
                </button>
              </div>
            ))}
            <p className="muted" style={{ margin: '0.65rem 0 0' }}>
              Click one to fill the form. This database is local only.
            </p>
          </div>
        </form>
      </main>
    </div>
  );
}
