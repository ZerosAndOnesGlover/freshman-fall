import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { useAuth } from '../../auth.jsx';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';
import { StatTile, DueDate, StatusBadge, KindBadge, GradeDial } from '../../components/Bits.jsx';
import { gpa, pct, formatDate, formatDateShort, daysUntil } from '../../format.js';

export default function Dashboard() {
  const { user } = useAuth();
  const { data, loading, error, reload } = useApi(() => api.dashboard(), []);

  if (loading) return <Loading label="Loading your dashboard" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  if (data.role !== 'student') return <StaffDashboard data={data} user={user} />;

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';
  const first = user.full_name.split(' ')[0];

  return (
    <>
      <div className="page-head">
        <div className="wrap row-between row-wrap">
          <div>
            <span className="eyebrow">{data.term?.label} · {formatDate(new Date().toISOString(), { weekday: true })}</span>
            <h1 style={{ marginTop: '0.5rem' }}>{greeting}, {first}.</h1>
          </div>
          <div className="small muted" style={{ textAlign: 'right' }}>
            <div className="mono">{user.student_id}</div>
            <div>{user.programme}</div>
          </div>
        </div>
      </div>

      <div className="wrap section">
        <div className="grid grid-4" style={{ marginBottom: '2.5rem' }}>
          <StatTile label="Cumulative GPA" value={gpa(data.standing.cumulative_gpa)}
            foot={data.standing.cumulative_gpa === null ? 'No course fully marked yet' : `${data.standing.credits_earned} credits earned`} />
          <StatTile label="This term" value={data.courses.length} unit="courses"
            foot={`${data.courses.reduce((a, c) => a + (c.credits || 0), 0)} credits`} />
          <StatTile label="Due in 7 days"
            value={data.upcoming.filter((u) => { const d = daysUntil(u.due_date); return d >= 0 && d <= 7; }).length}
            foot="assessments" />
          <StatTile label="In progress" value={data.standing.courses_in_progress} unit="marked"
            foot="courses with marks so far" />
        </div>

        <div className="grid grid-sidebar">
          <div className="stack-lg">
            <section className="card">
              <div className="card-head">
                <h3>Coming up</h3>
                <Link to="/portal/work" className="small">All coursework →</Link>
              </div>
              {data.upcoming.length ? (
                <div className="table-wrap">
                  <table className="table">
                    <thead>
                      <tr><th>Assessment</th><th>Course</th><th>Type</th><th>Due</th><th className="num">Points</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                      {data.upcoming.map((u) => (
                        <tr key={u.id}>
                          <td>
                            <Link to={`/portal/work/${u.id}`} style={{ fontWeight: 600, textDecoration: 'none' }}>
                              {u.label}
                            </Link>
                          </td>
                          <td><Link to={`/portal/courses/${u.course_id}`} className="mono small" style={{ textDecoration: 'none' }}>{u.course_code}</Link></td>
                          <td><KindBadge kind={u.kind} /></td>
                          <td><DueDate date={u.due_date} time={u.due_time} /></td>
                          <td className="num tnum">{u.possible || '—'}</td>
                          <td><StatusBadge status={u.submission_status} /></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : <div className="empty">Nothing due. Enjoy it while it lasts.</div>}
            </section>

            <section>
              <div className="row-between" style={{ marginBottom: '1.25rem' }}>
                <h2 className="rule-gold" style={{ fontSize: 'var(--t-lg)' }}>Your courses</h2>
                {data.other_course_count > 0 && (
                  <Link to="/portal/courses" className="small">
                    {data.other_course_count} more on record →
                  </Link>
                )}
              </div>
              <div className="grid grid-2">
                {data.courses.map((c) => (
                  <Link key={c.id} to={`/portal/courses/${c.id}`} className="card card-pad card-link course-card">
                    <span className="code">{c.code}</span>
                    <h3>{c.title}</h3>
                    {c.subtitle && <p className="sub">{c.subtitle}</p>}
                    <div className="meta">
                      <span>{c.credits} cr</span>
                      {c.instructor && <span>{c.instructor}</span>}
                      {c.schedule && <span className="tiny">{c.schedule}</span>}
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          </div>

          <aside className="stack-lg">
            {data.recent_grades.length > 0 && (
              <div className="card">
                <div className="card-head">
                  <h3>Recent marks</h3>
                  <Link to="/portal/grades" className="small">All →</Link>
                </div>
                <div className="card-body stack">
                  {data.recent_grades.map((g, i) => (
                    <div key={i} className="row-between">
                      <div>
                        <Link to={`/portal/courses/${g.course_id}`} className="mono tiny" style={{ textDecoration: 'none', color: 'var(--gold-700)' }}>
                          {g.course_code}
                        </Link>
                        <div className="small" style={{ fontWeight: 600 }}>{g.label}</div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <span className="tnum" style={{ fontFamily: 'var(--serif)', fontSize: 'var(--t-md)' }}>
                          {g.score}<span className="muted small">/{g.possible}</span>
                        </span>
                        <div className="tiny muted">{pct((g.score / g.possible) * 100, 0)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {data.announcements.length > 0 && (
              <div className="card">
                <div className="card-head"><h3>Notices</h3></div>
                <div className="card-body stack">
                  {data.announcements.map((a) => (
                    <div key={a.id}>
                      <div className="row" style={{ gap: '0.5rem' }}>
                        {a.course_code && <span className="pill">{a.course_code}</span>}
                        {a.pinned === 1 && <span className="badge badge-gold">Pinned</span>}
                      </div>
                      <strong style={{ display: 'block', marginTop: '0.35rem', fontFamily: 'var(--serif)' }}>{a.title}</strong>
                      <p className="small muted" style={{ marginTop: '0.25rem' }}>{a.body}</p>
                      <span className="tiny muted">{formatDateShort(a.created_at)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </aside>
        </div>
      </div>
    </>
  );
}

function StaffDashboard({ data, user }) {
  const waiting = data.courses.reduce((a, c) => a + c.awaiting, 0);
  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <span className="eyebrow">{data.term?.label}</span>
          <h1 style={{ marginTop: '0.5rem' }}>{user.title ? `${user.title} ` : ''}{user.full_name}</h1>
        </div>
      </div>
      <div className="wrap section">
        <div className="grid grid-3" style={{ marginBottom: '2.5rem' }}>
          <StatTile label="Courses" value={data.courses.length} foot="you teach or assist" />
          <StatTile label="Students" value={data.courses.reduce((a, c) => a + c.students, 0)} foot="enrolled across your courses" />
          <StatTile label="Awaiting marks" value={waiting}
            foot={waiting ? 'submissions in the queue' : 'nothing waiting'} />
        </div>

        <h2 className="rule-gold" style={{ fontSize: 'var(--t-lg)', marginBottom: '1.25rem' }}>Your courses</h2>
        <div className="grid grid-3">
          {data.courses.map((c) => (
            <Link key={c.id} to={`/portal/courses/${c.id}`} className="card card-pad card-link course-card">
              <span className="code">{c.code}</span>
              <h3>{c.title}</h3>
              <div className="meta">
                <span>{c.students} students</span>
                {c.awaiting > 0 && <span className="badge badge-amber">{c.awaiting} to mark</span>}
              </div>
            </Link>
          ))}
        </div>
        {waiting > 0 && (
          <p style={{ marginTop: '2rem' }}>
            <Link to="/portal/marking" className="btn btn-gold">Open the marking queue</Link>
          </p>
        )}
      </div>
    </>
  );
}
