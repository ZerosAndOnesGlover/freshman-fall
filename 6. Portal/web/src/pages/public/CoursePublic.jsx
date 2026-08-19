import { useParams, Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { useAuth } from '../../auth.jsx';

export default function CoursePublic() {
  const { id } = useParams();
  const { user } = useAuth();
  const { data: course, loading, error, reload } = useApi(() => api.courses.one(id), [id]);

  if (loading) return <Loading label="Loading course" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  const weights = course.components.filter((c) => !c.formative);

  return (
    <>
      <div className="page-head-navy">
        <div className="wrap">
          <Crumbs items={[{ label: 'Home', to: '/' }, { label: 'Courses', to: '/courses' }, { label: course.code }]} />
          <span className="eyebrow eyebrow-light" style={{ display: 'block', marginTop: '1rem' }}>
            {course.code} · {course.term} · {course.credits} credits
          </span>
          <h1 style={{ marginTop: '0.5rem' }}>{course.title}</h1>
          {course.subtitle && <p className="lede">{course.subtitle}</p>}
          {user && (
            <Link to={`/portal/courses/${course.id}`} className="btn btn-gold" style={{ marginTop: '1.5rem' }}>
              Open in the portal
            </Link>
          )}
        </div>
      </div>

      <div className="wrap section">
        <div className="grid grid-sidebar">
          <div className="stack-lg">
            {course.weeks.length > 0 ? (
              <div className="card">
                <div className="card-head">
                  <h3>Syllabus</h3>
                  <span className="small muted">{course.weeks.length} weeks</span>
                </div>
                <div>
                  {course.weeks.map((w) => (
                    <div key={w.id} style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--rule-soft)' }}>
                      <div className="row" style={{ alignItems: 'baseline', gap: '1rem' }}>
                        <span className="mono small" style={{ color: 'var(--gold-700)', minWidth: '3.6rem' }}>
                          Week {w.week_num}
                        </span>
                        <div className="grow">
                          <strong style={{ fontFamily: 'var(--serif)' }}>{w.topic || w.title || '—'}</strong>
                          {w.takeaway && <p className="small muted" style={{ marginTop: '0.3rem' }}>{w.takeaway}</p>}
                        </div>
                        <span className="tiny muted">{w.lecture_count} lectures</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="card"><div className="empty">Material for this course has not been published yet.</div></div>
            )}
          </div>

          <aside className="stack-lg">
            {course.schedule && (
              <div className="card card-pad">
                <span className="label">Meets</span>
                <p style={{ fontFamily: 'var(--serif)' }}>{course.schedule}</p>
              </div>
            )}

            {course.staff.length > 0 && (
              <div className="card">
                <div className="card-head"><h3>Teaching</h3></div>
                <div className="card-body stack">
                  {course.staff.map((s) => (
                    <div key={s.id}>
                      <div className="row" style={{ gap: '0.5rem' }}>
                        <strong>{s.title ? `${s.title} ` : ''}{s.full_name}</strong>
                        {s.staff_role === 'ta' && <span className="badge badge-grey">TA</span>}
                      </div>
                      {s.office_hours && <p className="tiny muted" style={{ marginTop: '0.2rem' }}>{s.office_hours}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {weights.length > 0 && (
              <div className="card">
                <div className="card-head"><h3>Assessment</h3></div>
                <table className="table table-plain">
                  <tbody>
                    {weights.map((c) => (
                      <tr key={c.id}>
                        <td>
                          {c.name}
                          {c.drop_lowest > 0 && (
                            <div className="tiny muted">lowest {c.drop_lowest} dropped</div>
                          )}
                        </td>
                        <td className="num tnum" style={{ fontWeight: 600 }}>{c.weight}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </aside>
        </div>
      </div>
    </>
  );
}
