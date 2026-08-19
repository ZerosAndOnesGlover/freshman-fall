import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading } from '../../components/Chrome.jsx';
import { formatDate, formatDateShort, daysUntil } from '../../format.js';

export default function Home() {
  const { data: inst } = useApi(() => api.public.institution(), []);
  const { data: events } = useApi(() => api.public.calendar('?limit=6'), []);
  const { data: catalog } = useApi(() => api.public.catalog(), []);

  const current = catalog?.find((t) => t.is_current);

  return (
    <>
      <section className="hero">
        <div className="wrap">
          <span className="eyebrow eyebrow-light">School of Computer Science &amp; Engineering</span>
          <h1 className="display">A rigorous four-year degree, taught in the open.</h1>
          <p className="lede">
            Every lecture, problem set, lab and rubric that makes up the B.Sc. is published
            here — the same material students read, the same standards they are marked
            against. Nothing is behind a curtain.
          </p>
          <div className="hero-actions">
            <Link to="/courses" className="btn btn-gold">Browse the catalogue</Link>
            <Link to="/portal" className="btn btn-ghost" style={{ color: '#fff', borderColor: 'rgba(255,255,255,0.28)' }}>
              Student portal
            </Link>
          </div>

          {inst && (
            <div className="hero-figures">
              <div><div className="n">{inst.stats.courses}</div><div className="l">Courses</div></div>
              <div><div className="n">{inst.stats.lectures}</div><div className="l">Lectures</div></div>
              <div><div className="n">{inst.stats.materials}</div><div className="l">Materials</div></div>
              <div><div className="n">8</div><div className="l">Semesters</div></div>
            </div>
          )}
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <div className="grid grid-sidebar">
            <div>
              <span className="eyebrow">This semester</span>
              <h2 className="rule-gold" style={{ marginTop: '0.5rem' }}>
                {current ? current.label : 'Current courses'}
              </h2>
              {!catalog && <Loading />}
              {current && (
                <div className="grid grid-2" style={{ marginTop: '1.75rem' }}>
                  {current.courses.map((c) => (
                    <Link key={c.id} to={`/courses/${c.id}`} className="card card-pad card-link course-card">
                      <span className="code">{c.code}</span>
                      <h3>{c.title}</h3>
                      {c.subtitle && <p className="sub">{c.subtitle}</p>}
                      <div className="meta">
                        <span>{c.credits} credits</span>
                        {c.instructor && <span>{c.instructor}</span>}
                        {c.lecture_count > 0 && <span>{c.lecture_count} lectures</span>}
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>

            <aside className="stack-lg">
              <div className="card">
                <div className="card-head"><h3>Upcoming dates</h3></div>
                <div style={{ padding: '0.5rem 1.5rem 1rem' }}>
                  {!events && <Loading />}
                  {events?.map((e) => {
                    const d = daysUntil(e.date_iso);
                    return (
                      <div key={e.id} style={{ padding: '0.6rem 0', borderBottom: '1px solid var(--rule-soft)' }}>
                        <div className="row" style={{ gap: '0.75rem', alignItems: 'baseline' }}>
                          <span className="mono tiny" style={{ color: 'var(--gold-700)', minWidth: '3.4rem' }}>
                            {formatDateShort(e.date_iso)}
                          </span>
                          <span className="small grow">{e.title}</span>
                        </div>
                        {d >= 0 && d <= 14 && (
                          <span className="tiny muted" style={{ marginLeft: '4.15rem' }}>
                            {d === 0 ? 'today' : `in ${d} days`}
                          </span>
                        )}
                      </div>
                    );
                  })}
                  <Link to="/calendar" className="small" style={{ display: 'inline-block', marginTop: '0.9rem' }}>
                    Full academic calendar →
                  </Link>
                </div>
              </div>

              <div className="card card-pad" style={{ background: 'var(--navy-900)', color: '#fff', borderColor: 'transparent' }}>
                <span className="eyebrow eyebrow-light">For students</span>
                <h3 style={{ color: '#fff', marginTop: '0.5rem' }}>Hand in your work</h3>
                <p className="small" style={{ color: 'rgba(255,255,255,0.72)', marginTop: '0.5rem' }}>
                  Problem sets, labs and projects are submitted through the portal, and
                  marks appear against the same rubric published in the catalogue.
                </p>
                <Link to="/portal" className="btn btn-gold btn-block" style={{ marginTop: '1.25rem' }}>
                  Go to the portal
                </Link>
              </div>
            </aside>
          </div>
        </div>
      </section>

      <section className="section" style={{ background: 'var(--paper-alt)', borderTop: '1px solid var(--rule)' }}>
        <div className="wrap">
          <span className="eyebrow">How the degree is built</span>
          <h2 className="rule-gold" style={{ marginTop: '0.5rem' }}>Foundations first, then systems, then depth</h2>
          <div className="grid grid-3" style={{ marginTop: '2rem' }}>
            {[
              { y: 'Years 1', t: 'Foundations', d: 'Programming, discrete mathematics, calculus and physics — the vocabulary everything later is written in.' },
              { y: 'Year 2', t: 'Systems', d: 'Data structures, computer architecture, compilers and programming languages. How machines actually run your code.' },
              { y: 'Years 3–4', t: 'Depth &amp; practice', d: 'Algorithms, networks, distributed systems, security, and a two-semester capstone that has to work.' },
            ].map((s) => (
              <div key={s.t} className="card card-pad">
                <span className="eyebrow">{s.y}</span>
                <h3 style={{ marginTop: '0.5rem' }} dangerouslySetInnerHTML={{ __html: s.t }} />
                <p className="small muted" style={{ marginTop: '0.6rem' }}>{s.d}</p>
              </div>
            ))}
          </div>
          <p style={{ marginTop: '2rem' }}>
            <Link to="/academics" className="btn btn-ghost">Degree requirements</Link>
          </p>
        </div>
      </section>
    </>
  );
}
