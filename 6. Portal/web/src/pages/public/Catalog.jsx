import { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';

export default function Catalog() {
  const { data, loading, error, reload } = useApi(() => api.public.catalog(), []);
  const [q, setQ] = useState('');
  const [year, setYear] = useState('all');

  const needle = q.trim().toLowerCase();
  const terms = (data || [])
    .filter((t) => year === 'all' || String(t.year_num) === year)
    .map((t) => ({
      ...t,
      courses: t.courses.filter((c) =>
        !needle
        || c.code.toLowerCase().includes(needle)
        || c.title.toLowerCase().includes(needle)
        || (c.subtitle || '').toLowerCase().includes(needle)),
    }))
    .filter((t) => t.courses.length);

  const total = terms.reduce((a, t) => a + t.courses.length, 0);

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <Crumbs items={[{ label: 'Home', to: '/' }, { label: 'Courses' }]} />
          <h1>Course Catalogue</h1>
          <p className="lede">
            Every course in the four-year B.Sc., with its credits, schedule and the
            material that has been published so far.
          </p>
        </div>
      </div>

      <div className="wrap section">
        <div className="row row-wrap" style={{ marginBottom: '2rem' }}>
          <input
            className="input" style={{ maxWidth: '22rem' }}
            placeholder="Search by code or title…"
            value={q} onChange={(e) => setQ(e.target.value)}
            aria-label="Search courses"
          />
          <select className="select" style={{ maxWidth: '12rem' }} value={year}
            onChange={(e) => setYear(e.target.value)} aria-label="Filter by year">
            <option value="all">All years</option>
            <option value="1">Year 1 · Freshman</option>
            <option value="2">Year 2 · Sophomore</option>
            <option value="3">Year 3 · Junior</option>
            <option value="4">Year 4 · Senior</option>
          </select>
          <span className="small muted">{total} courses</span>
        </div>

        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />

        {terms.map((t) => (
          <section key={t.term_id ?? t.label} style={{ marginBottom: '3rem' }}>
            <div className="term-band">
              <h2>{t.label}</h2>
              <span className="small muted">{t.year_label} · {t.semester}</span>
              {t.is_current === 1 && <span className="badge badge-gold">Current</span>}
              <span className="small muted" style={{ marginLeft: 'auto' }}>
                {t.courses.reduce((a, c) => a + (c.credits || 0), 0)} credits
              </span>
            </div>
            <div className="grid grid-3">
              {t.courses.map((c) => (
                <Link key={c.id} to={`/courses/${c.id}`} className="card card-pad card-link course-card">
                  <span className="code">{c.code}</span>
                  <h3>{c.title}</h3>
                  {c.subtitle && <p className="sub">{c.subtitle}</p>}
                  <div className="meta">
                    <span>{c.credits} cr</span>
                    {c.lecture_count > 0
                      ? <span>{c.lecture_count} lectures</span>
                      : <span className="muted">Not yet published</span>}
                    {c.instructor && <span>{c.instructor}</span>}
                  </div>
                </Link>
              ))}
            </div>
          </section>
        ))}

        {!loading && !terms.length && (
          <div className="empty">Nothing matches “{q}”.</div>
        )}
      </div>
    </>
  );
}
