import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { initials } from '../../format.js';

export default function Faculty() {
  const { data, loading, error, reload } = useApi(() => api.public.faculty(), []);
  const staff = data || [];
  const professors = staff.filter((s) => s.staff_role === 'instructor');
  const tas = staff.filter((s) => s.staff_role === 'ta');

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <Crumbs items={[{ label: 'Home', to: '/' }, { label: 'Faculty' }]} />
          <h1>Faculty &amp; Teaching Assistants</h1>
          <p className="lede">Who teaches what, and when they hold office hours.</p>
        </div>
      </div>

      <div className="wrap section">
        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />

        {professors.length > 0 && (
          <>
            <h2 className="rule-gold">Faculty</h2>
            <div className="grid grid-3" style={{ marginTop: '1.75rem', marginBottom: '3rem' }}>
              {professors.map((p) => <Person key={`${p.id}-i`} p={p} />)}
            </div>
          </>
        )}

        {tas.length > 0 && (
          <>
            <h2 className="rule-gold">Teaching Assistants</h2>
            <div className="grid grid-3" style={{ marginTop: '1.75rem' }}>
              {tas.map((p) => <Person key={`${p.id}-t`} p={p} />)}
            </div>
          </>
        )}

        {!loading && !staff.length && <div className="empty">No staff have been published yet.</div>}
      </div>
    </>
  );
}

function Person({ p }) {
  return (
    <div className="card card-pad">
      <div className="row" style={{ gap: '0.85rem', alignItems: 'flex-start' }}>
        <span className="avatar" style={{ background: 'var(--navy-900)', width: '2.75rem', height: '2.75rem', fontSize: '0.8rem' }}>
          {initials(p.full_name)}
        </span>
        <div className="grow">
          <h3 style={{ fontSize: 'var(--t-md)' }}>{p.title ? `${p.title} ` : ''}{p.full_name}</h3>
          <p className="small muted" style={{ marginTop: '0.15rem' }}>{p.courses}</p>
        </div>
      </div>
      {p.office_hours && (
        <p className="small" style={{ marginTop: '1rem', paddingTop: '0.85rem', borderTop: '1px solid var(--rule-soft)' }}>
          <span className="label" style={{ marginBottom: '0.25rem' }}>Office hours</span>
          {p.office_hours}
        </p>
      )}
      <p className="tiny mono muted" style={{ marginTop: '0.75rem' }}>{p.email}</p>
    </div>
  );
}
