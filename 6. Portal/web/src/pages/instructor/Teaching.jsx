import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';

export default function Teaching() {
  const { data, loading, error, reload } = useApi(() => api.instructor.courses(), []);
  const rows = data || [];

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <h1>Teaching</h1>
          <p className="lede">The courses you teach or assist on.</p>
        </div>
      </div>
      <div className="wrap section">
        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />
        <div className="grid grid-3">
          {rows.map((c) => (
            <Link key={c.id} to={`/portal/courses/${c.id}`} className="card card-pad card-link course-card">
              <div className="row-between">
                <span className="code">{c.code}</span>
                {c.staff_role === 'ta' && <span className="badge badge-grey">TA</span>}
              </div>
              <h3>{c.title}</h3>
              <div className="meta">
                <span>{c.term}</span>
                <span>{c.students} students</span>
                {c.awaiting > 0 && <span className="badge badge-amber">{c.awaiting} to mark</span>}
              </div>
            </Link>
          ))}
        </div>
        {!loading && !rows.length && <div className="empty">You are not assigned to any courses.</div>}
      </div>
    </>
  );
}
