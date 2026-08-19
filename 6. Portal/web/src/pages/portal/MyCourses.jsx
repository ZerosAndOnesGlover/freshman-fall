import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';

export default function MyCourses() {
  const { data, loading, error, reload } = useApi(() => api.courses.mine(), []);
  const courses = data || [];

  const terms = [];
  const seen = new Map();
  for (const c of courses) {
    const key = c.term || 'Other';
    if (!seen.has(key)) { seen.set(key, { label: key, is_current: c.is_current, rows: [] }); terms.push(seen.get(key)); }
    seen.get(key).rows.push(c);
  }

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <h1>My Courses</h1>
          <p className="lede">Everything on your record, current term first.</p>
        </div>
      </div>

      <div className="wrap section">
        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />

        {terms.map((t) => (
          <section key={t.label} style={{ marginBottom: '3rem' }}>
            <div className="term-band">
              <h2>{t.label}</h2>
              {t.is_current === 1 && <span className="badge badge-gold">Current</span>}
              <span className="small muted" style={{ marginLeft: 'auto' }}>{t.rows.length} courses</span>
            </div>
            <div className="grid grid-3">
              {t.rows.map((c) => (
                <Link key={c.id} to={`/portal/courses/${c.id}`} className="card card-pad card-link course-card">
                  <div className="row-between">
                    <span className="code">{c.code}</span>
                    {c.my_role !== 'student' && <span className="badge badge-grey">{c.my_role}</span>}
                  </div>
                  <h3>{c.title}</h3>
                  {c.subtitle && <p className="sub">{c.subtitle}</p>}
                  <div className="meta">
                    <span>{c.credits} cr</span>
                    {c.lecture_count > 0
                      ? <span>{c.lecture_count} lectures</span>
                      : <span className="muted">no material yet</span>}
                    {c.assessment_count > 0 && <span>{c.assessment_count} assessments</span>}
                  </div>
                </Link>
              ))}
            </div>
          </section>
        ))}

        {!loading && !courses.length && <div className="empty">You are not enrolled in anything yet.</div>}
      </div>
    </>
  );
}
