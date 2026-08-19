import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crest } from '../../components/Chrome.jsx';
import { pct, gpa, formatDate } from '../../format.js';

export default function Transcript() {
  const { data, loading, error, reload } = useApi(() => api.grades.transcript(), []);

  if (loading) return <Loading label="Assembling your transcript" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  const { student } = data;

  return (
    <div className="wrap wrap-narrow section">
      <div className="row-between no-print" style={{ marginBottom: '1.5rem' }}>
        <p className="small muted">An unofficial record, generated from the portal gradebook.</p>
        <button className="btn btn-ghost btn-sm" onClick={() => window.print()}>Print</button>
      </div>

      <div className="card" style={{ padding: '2.5rem' }}>
        <header style={{ display: 'flex', gap: '1.25rem', alignItems: 'flex-start', paddingBottom: '1.5rem', borderBottom: '2px solid var(--navy-900)' }}>
          <Crest />
          <div className="grow">
            <h1 style={{ fontSize: 'var(--t-lg)' }}>Institute of Science &amp; Technology</h1>
            <p className="small muted">School of Computer Science &amp; Engineering</p>
          </div>
          <div className="small muted" style={{ textAlign: 'right' }}>
            <div>Unofficial transcript</div>
            <div>{formatDate(new Date().toISOString(), { year: true })}</div>
          </div>
        </header>

        <dl style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '0.4rem 1.5rem', margin: '1.5rem 0 2rem', fontSize: 'var(--t-sm)' }}>
          <dt className="muted">Student</dt><dd style={{ margin: 0, fontWeight: 600 }}>{student.full_name}</dd>
          <dt className="muted">Registry number</dt><dd style={{ margin: 0 }} className="mono">{student.student_id}</dd>
          <dt className="muted">Programme</dt><dd style={{ margin: 0 }}>{student.programme}</dd>
          <dt className="muted">Year</dt><dd style={{ margin: 0 }}>{student.year_level}</dd>
        </dl>

        {data.terms.map((t) => (
          <div key={t.term_id} className="transcript-term">
            <header>
              <h3>{t.term}</h3>
              <span className="small" style={{ color: 'rgba(255,255,255,0.75)' }}>
                {t.gpa === null ? 'In progress' : `Term GPA ${gpa(t.gpa)}`}
              </span>
            </header>
            <table className="table">
              <thead>
                <tr>
                  <th>Code</th><th>Course</th><th className="num">Credits</th>
                  <th className="num">Percent</th><th className="num">Grade</th><th className="num">Points</th>
                </tr>
              </thead>
              <tbody>
                {t.courses.map((c) => (
                  <tr key={c.id}>
                    <td className="mono small">{c.code}</td>
                    <td>{c.title}</td>
                    <td className="num tnum">{c.credits}</td>
                    <td className="num tnum">{c.percent === null ? '—' : pct(c.percent)}</td>
                    <td className="num" style={{ fontWeight: 600 }}>
                      {c.letter || '—'}
                      {c.letter && !c.complete && <span className="tiny muted" style={{ fontWeight: 400 }}> (partial)</span>}
                    </td>
                    <td className="num tnum">{c.complete && c.points !== null ? c.points.toFixed(1) : '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="card-foot muted">
              {t.credits_completed} of {t.credits_enrolled} credits completed
            </div>
          </div>
        ))}

        <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '2px solid var(--navy-900)' }}>
          <div className="row-between">
            <strong style={{ fontFamily: 'var(--serif)', fontSize: 'var(--t-md)' }}>Cumulative</strong>
            <div className="row" style={{ gap: '2.5rem' }}>
              <span><span className="muted small">Credits earned </span><strong className="tnum">{data.credits_earned}</strong><span className="muted small"> / 142</span></span>
              <span><span className="muted small">GPA </span><strong className="tnum">{gpa(data.cumulative)}</strong></span>
            </div>
          </div>
          <div className="meter meter-gold" style={{ marginTop: '1rem' }}>
            <span style={{ width: `${(data.credits_earned / 142) * 100}%` }} />
          </div>
        </div>

        <details style={{ marginTop: '2rem' }} className="no-print">
          <summary className="small" style={{ cursor: 'pointer', color: 'var(--navy-600)' }}>Grading scale</summary>
          <table className="table" style={{ marginTop: '1rem' }}>
            <thead><tr><th>Letter</th><th className="num">Points</th><th>Range</th><th>Descriptor</th></tr></thead>
            <tbody>
              {data.scale.map((b) => (
                <tr key={b.letter}>
                  <td style={{ fontWeight: 600 }}>{b.letter}</td>
                  <td className="num tnum">{b.points.toFixed(1)}</td>
                  <td className="small">{b.low === 0 ? `< ${Math.ceil(b.high)}%` : `${b.low}–${b.high}%`}</td>
                  <td className="small muted">{b.descriptor}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </details>

        <p className="tiny muted" style={{ marginTop: '2rem' }}>
          Course percentages are computed from each course's published component weights.
          A grade shown as “partial” reflects only the work marked so far and does not
          contribute grade points until the course is complete.
        </p>
      </div>
    </div>
  );
}
