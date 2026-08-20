import { NavLink, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../auth.jsx';
import { initials } from '../format.js';

export function Crest({ className = 'crest' }) {
  return <span className={className} aria-hidden="true">IST</span>;
}

export function Wordmark({ to = '/' }) {
  return (
    <Link to={to} className="wordmark">
      <Crest />
      <span className="wordmark-text">
        <span className="wordmark-name">Institute of Science &amp; Technology</span>
        <span className="wordmark-sub">Computer Science &amp; Engineering</span>
      </span>
    </Link>
  );
}

const PUBLIC_NAV = [
  { to: '/', label: 'Home', end: true },
  { to: '/academics', label: 'Academics' },
  { to: '/courses', label: 'Courses' },
  { to: '/calendar', label: 'Calendar' },
  { to: '/faculty', label: 'Faculty' },
  { to: '/about', label: 'About' },
];

const PORTAL_NAV = [
  { to: '/portal', label: 'Dashboard', end: true },
  { to: '/portal/courses', label: 'My Courses' },
  { to: '/portal/work', label: 'Coursework' },
  { to: '/portal/grades', label: 'Grades' },
];

const STAFF_NAV = [
  { to: '/portal', label: 'Dashboard', end: true },
  { to: '/portal/teaching', label: 'Teaching' },
  { to: '/portal/marking', label: 'Marking' },
];

export function Masthead() {
  const { user, isStaff } = useAuth();
  const { pathname } = useLocation();
  const inPortal = pathname.startsWith('/portal');
  const nav = inPortal ? (isStaff ? STAFF_NAV : PORTAL_NAV) : PUBLIC_NAV;

  return (
    <>
      <header className="masthead">
        <div className="wrap masthead-inner">
          <Wordmark to={inPortal ? '/portal' : '/'} />
          <nav className="nav" aria-label={inPortal ? 'Portal' : 'Main'}>
            {nav.map((n) => (
              <NavLink key={n.to} to={n.to} end={n.end}
                className={({ isActive }) => (isActive ? 'active' : undefined)}>
                {n.label}
              </NavLink>
            ))}
          </nav>
          <div className="masthead-user">
            {user ? (
              <>
                {!inPortal && <Link to="/portal" className="btn btn-gold btn-sm">Portal</Link>}
                <Link to="/portal/profile" className="row" style={{ textDecoration: 'none' }}>
                  <span className="avatar">{initials(user.full_name)}</span>
                </Link>
              </>
            ) : (
              <Link to="/login" className="btn btn-gold btn-sm">Sign in</Link>
            )}
          </div>
        </div>
      </header>
      {inPortal && user && (
        <div className="subnav">
          <div className="wrap">
            {(isStaff ? STAFF_NAV : PORTAL_NAV).map((n) => (
              <NavLink key={n.to} to={n.to} end={n.end}
                className={({ isActive }) => (isActive ? 'active' : undefined)}>
                {n.label}
              </NavLink>
            ))}
            <NavLink to="/portal/transcript" className={({ isActive }) => (isActive ? 'active' : undefined)}>
              Transcript
            </NavLink>
            <NavLink to="/" style={{ marginLeft: 'auto', whiteSpace: 'nowrap' }}>
              Public site ↗
            </NavLink>
          </div>
        </div>
      )}
    </>
  );
}

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <div className="wrap">
        <div className="footer-cols">
          <div>
            <div className="row" style={{ gap: '0.75rem', marginBottom: '1rem' }}>
              <Crest />
              <strong style={{ color: '#fff', fontFamily: 'var(--serif)', fontSize: '1rem' }}>
                Institute of Science &amp; Technology
              </strong>
            </div>
            <p className="small" style={{ maxWidth: '28ch' }}>
              School of Computer Science &amp; Engineering — a four-year B.Sc. built on
              rigorous foundations and work that ships.
            </p>
          </div>
          <div>
            <h4>Academics</h4>
            <ul className="footer-links">
              <li><Link to="/courses">Course catalogue</Link></li>
              <li><Link to="/academics">Degree requirements</Link></li>
              <li><Link to="/calendar">Academic calendar</Link></li>
              <li><Link to="/page/grading-standards">Grading standards</Link></li>
            </ul>
          </div>
          <div>
            <h4>Students</h4>
            <ul className="footer-links">
              <li><Link to="/portal">Student portal</Link></li>
              <li><Link to="/portal/work">Submit coursework</Link></li>
              <li><Link to="/portal/grades">Grades</Link></li>
              <li><Link to="/faculty">Office hours</Link></li>
            </ul>
          </div>
          <div>
            <h4>About</h4>
            <ul className="footer-links">
              <li><Link to="/page/university-policies">Policies</Link></li>
              <li><Link to="/faculty">Faculty</Link></li>
              <li><Link to="/about">The Institute</Link></li>
            </ul>
          </div>
        </div>
        <div className="footer-base">
          <span>© {year} Institute of Science &amp; Technology</span>
          <span>Course material is rendered live from the academic vault.</span>
        </div>
      </div>
    </footer>
  );
}

export function Loading({ label = 'Loading' }) {
  return (
    <div className="loading">
      <div className="spinner" />
      <p className="small" style={{ marginTop: '1rem' }}>{label}…</p>
    </div>
  );
}

export function ErrorNote({ error, onRetry }) {
  if (!error) return null;
  return (
    <div className="notice notice-error">
      <strong>{error.status === 403 ? 'Not permitted' : 'Something went wrong'}</strong>
      <p style={{ margin: '0.35rem 0 0' }}>{error.message}</p>
      {onRetry && (
        <button className="btn btn-ghost btn-sm" style={{ marginTop: '0.75rem' }} onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}

export function Empty({ children }) {
  return <div className="empty">{children}</div>;
}

export function Crumbs({ items }) {
  return (
    <nav className="crumbs" aria-label="Breadcrumb">
      {items.map((it, i) => (
        <span key={i} className="row" style={{ gap: '0.5rem' }}>
          {i > 0 && <span className="sep">/</span>}
          {it.to ? <Link to={it.to}>{it.label}</Link> : <span>{it.label}</span>}
        </span>
      ))}
    </nav>
  );
}
