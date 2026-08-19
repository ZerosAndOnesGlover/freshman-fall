import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';
import { GradeDial, StatTile } from '../../components/Bits.jsx';
import { pct, gpa } from '../../format.js';

export default function Grades() {
  const { data, loading, error, reload } = useApi(() => api.grades.summary(), []);

  if (loading) return <Loading label="Working out your grades" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  const current = data.terms.find((t) => t.is_current);
  const active = data.terms.filter((t) => t.courses.some((c) => c.percent !== null));

  return (
    <>
      <div className="page-head">
        <div className="wrap row-between row-wrap">
          <div>
            <h1>Grades</h1>
            <p className="lede">A running mark for every course, computed from its published weights.</p>
          </div>
          <Link to="/portal/transcript" className="btn btn-ghost">View transcript</Link>
        </div>
      </div>

      <div className="wrap section">
        <div className="grid grid-4" style={{ marginBottom: '2.5rem' }}>
          <StatTile label="Cumulative GPA" value={gpa(data.cumulative)}
            foot={data.cumulative === null ? 'No course fully marked yet' : 'across completed courses'} />
          <StatTile label="Credits earned" value={data.credits_earned}
            foot={`of ${data.credits_enrolled} enrolled`} />
          <StatTile label="Courses with marks" value={data.courses_in_progress} foot="in progress" />
          <StatTile label="This term" value={current ? current.courses.length : '—'} unit="courses"
            foot={current?.term} />
        </div>

        {!active.length && (
          <div className="card"><div className="empty">Nothing has been marked yet.</div></div>
        )}

        {active.map((t) => (
          <section key={t.term_id} style={{ marginBottom: '3rem' }}>
            <div className="term-band">
              <h2>{t.term}</h2>
              {t.is_current === 1 && <span className="badge badge-gold">Current</span>}
              <span className="small muted" style={{ marginLeft: 'auto' }}>
                {t.gpa === null ? 'GPA pending — no course fully marked' : `Term GPA ${gpa(t.gpa)}`}
              </span>
            </div>
            <div className="grid grid-3">
              {t.courses.filter((c) => c.percent !== null).map((c) => (
                <Link key={c.id} to={`/portal/courses/${c.id}`} className="card card-pad card-link">
                  <div className="row" style={{ gap: '1rem', alignItems: 'center' }}>
                    <GradeDial percent={c.percent} letter={c.letter} size={76} />
                    <div className="grow">
                      <span className="code mono tiny" style={{ color: 'var(--gold-700)', fontWeight: 600 }}>{c.code}</span>
                      <h3 style={{ fontSize: 'var(--t-base)', marginTop: '0.2rem' }}>{c.title}</h3>
                      <p className="tiny muted" style={{ marginTop: '0.35rem' }}>
                        {c.complete
                          ? 'Final'
                          : `${c.graded_weight}% of ${c.total_weight}% marked`}
                      </p>
                    </div>
                  </div>
                  <div className="meter" style={{ marginTop: '1rem' }}>
                    <span style={{ width: `${(c.graded_weight / (c.total_weight || 100)) * 100}%` }} />
                  </div>
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>
    </>
  );
}
