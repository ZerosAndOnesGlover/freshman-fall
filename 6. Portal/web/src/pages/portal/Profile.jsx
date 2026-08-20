import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../auth.jsx';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { initials } from '../../format.js';

export default function Profile() {
  const { user, logout } = useAuth();
  const nav = useNavigate();
  const { data } = useApi(() => api.grades.summary().catch(() => null), []);

  return (
    <div className="wrap wrap-narrow section">
      <div className="card card-pad">
        <div className="row" style={{ gap: '1.25rem' }}>
          <span className="avatar" style={{ width: '4rem', height: '4rem', fontSize: '1.1rem', background: 'var(--navy-900)' }}>
            {initials(user.full_name)}
          </span>
          <div className="grow">
            <h1 style={{ fontSize: 'var(--t-xl)' }}>{user.title ? `${user.title} ` : ''}{user.full_name}</h1>
            <p className="small muted">{user.email}</p>
          </div>
        </div>

        <dl style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '0.5rem 1.5rem', margin: '2rem 0 0', fontSize: 'var(--t-sm)' }}>
          <dt className="muted">Role</dt><dd style={{ margin: 0, textTransform: 'capitalize' }}>{user.role}</dd>
          {user.student_id && (<><dt className="muted">Registry number</dt><dd style={{ margin: 0 }} className="mono">{user.student_id}</dd></>)}
          {user.programme && (<><dt className="muted">Programme</dt><dd style={{ margin: 0 }}>{user.programme}</dd></>)}
          {user.year_level && (<><dt className="muted">Year</dt><dd style={{ margin: 0 }}>{user.year_level}</dd></>)}
          {data && (<><dt className="muted">Credits earned</dt><dd style={{ margin: 0 }}>{data.credits_earned} of 142</dd></>)}
        </dl>

        <div className="row" style={{ marginTop: '2rem', gap: '0.5rem' }}>
          <Link to="/portal/password" className="btn btn-ghost">Change password</Link>
          <button className="btn btn-quiet"
            onClick={async () => { await logout(); nav('/'); }}>
            Sign out
          </button>
        </div>
      </div>
    </div>
  );
}
