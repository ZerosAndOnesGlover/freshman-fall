import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../api.js';
import { useAuth } from '../../auth.jsx';

export default function ChangePassword() {
  const { user, refresh } = useAuth();
  const nav = useNavigate();
  const [current, setCurrent] = useState('');
  const [next, setNext] = useState('');
  const [confirm, setConfirm] = useState('');
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  const forced = Boolean(user?.must_change_password);

  async function submit(e) {
    e.preventDefault();
    setErr(null);
    if (next !== confirm) return setErr('The two new passwords do not match');
    if (next.length < 8) return setErr('Choose a password of at least 8 characters');

    setBusy(true);
    try {
      await api.auth.changePassword(current, next);
      await refresh?.();
      setDone(true);
      setTimeout(() => nav('/portal'), 900);
    } catch (e2) {
      setErr(e2.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="wrap wrap-narrow section">
      <div className="card card-pad" style={{ maxWidth: '30rem', margin: '0 auto' }}>
        <h1 style={{ fontSize: 'var(--t-xl)' }}>
          {forced ? 'Choose your password' : 'Change your password'}
        </h1>
        <p className="small muted" style={{ marginTop: '0.5rem' }}>
          {forced
            ? 'You are signed in with a temporary password issued by the registry. Pick your own before going on.'
            : 'Signing in elsewhere will be ended when you change this.'}
        </p>

        {done && <div className="notice notice-ok" style={{ marginTop: '1.5rem' }}>Password changed.</div>}
        {err && <div className="notice notice-error" style={{ marginTop: '1.5rem' }}>{err}</div>}

        {!done && (
          <form onSubmit={submit} style={{ marginTop: '1.5rem' }}>
            <div className="field">
              <label htmlFor="cur">{forced ? 'Temporary password' : 'Current password'}</label>
              <input id="cur" className="input" type="password" autoComplete="current-password"
                value={current} onChange={(e) => setCurrent(e.target.value)} required />
            </div>
            <div className="field">
              <label htmlFor="new">New password</label>
              <input id="new" className="input" type="password" autoComplete="new-password"
                value={next} onChange={(e) => setNext(e.target.value)} required minLength={8} />
              <p className="hint">At least 8 characters.</p>
            </div>
            <div className="field">
              <label htmlFor="conf">Repeat the new password</label>
              <input id="conf" className="input" type="password" autoComplete="new-password"
                value={confirm} onChange={(e) => setConfirm(e.target.value)} required />
            </div>
            <button className="btn btn-block" style={{ marginTop: '1.5rem' }} disabled={busy}>
              {busy ? 'Saving…' : 'Save password'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
