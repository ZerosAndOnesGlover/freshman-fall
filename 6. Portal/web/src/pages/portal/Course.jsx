import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { useAuth } from '../../auth.jsx';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { DueDate, StatusBadge, KindBadge, GradeDial } from '../../components/Bits.jsx';
import { Markdown } from '../../markdown.jsx';
import { pct, formatDate } from '../../format.js';

export default function Course() {
  const { id } = useParams();
  const { isStaff } = useAuth();
  const { data: course, loading, error, reload } = useApi(() => api.courses.one(id), [id]);
  const { data: work } = useApi(() => api.assessments.forCourse(id), [id]);
  const { data: grade } = useApi(() => api.grades.course(id).catch(() => null), [id]);
  const [tab, setTab] = useState('weeks');

  if (loading) return <Loading label="Loading course" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  return (
    <>
      <div className="page-head-navy">
        <div className="wrap">
          <Crumbs items={[{ label: 'Portal', to: '/portal' }, { label: 'Courses', to: '/portal/courses' }, { label: course.code }]} />
          <div className="row-between row-wrap" style={{ marginTop: '1rem', alignItems: 'flex-end' }}>
            <div>
              <span className="eyebrow eyebrow-light">{course.code} · {course.term} · {course.credits} credits</span>
              <h1 style={{ marginTop: '0.5rem' }}>{course.title}</h1>
              {course.subtitle && <p className="lede">{course.subtitle}</p>}
              {course.schedule && <p className="small" style={{ color: 'rgba(255,255,255,0.6)', marginTop: '0.75rem' }}>{course.schedule}</p>}
            </div>
            {grade && grade.percent !== null && (
              <div className="row" style={{ gap: '1rem' }}>
                <GradeDial percent={grade.percent} letter={grade.letter?.letter} />
                <div className="small" style={{ color: 'rgba(255,255,255,0.7)' }}>
                  <div>Running grade</div>
                  <div className="tiny">{grade.graded_weight}% of the course marked</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="subnav">
        <div className="wrap">
          {[['weeks', 'Weeks & lectures'], ['work', 'Coursework'], ['grades', 'Grades'], ['about', 'About']].map(([k, l]) => (
            <a key={k} href="#" className={tab === k ? 'active' : undefined}
              onClick={(e) => { e.preventDefault(); setTab(k); }}>{l}</a>
          ))}
        </div>
      </div>

      <div className="wrap section">
        {tab === 'weeks' && <Weeks course={course} />}
        {tab === 'work' && <Work rows={work} courseId={course.id} isStaff={isStaff} />}
        {tab === 'grades' && <Grades grade={grade} courseId={course.id} />}
        {tab === 'about' && <About course={course} />}
      </div>
    </>
  );
}

function Weeks({ course }) {
  const [open, setOpen] = useState(course.weeks.length ? course.weeks[0].week_num : null);
  if (!course.weeks.length) return <div className="empty">No material has been published for this course yet.</div>;

  return (
    <div className="card">
      {course.weeks.map((w) => (
        <div key={w.id} className="week-item">
          <button className="week-btn" aria-expanded={open === w.week_num}
            onClick={() => setOpen(open === w.week_num ? null : w.week_num)}>
            <span className="week-num">{w.week_num}</span>
            <span className="grow">
              <strong style={{ fontFamily: 'var(--serif)', fontSize: 'var(--t-md)' }}>
                {w.topic || w.title || `Week ${w.week_num}`}
              </strong>
              {w.monday_date && (
                <span className="tiny muted" style={{ display: 'block', marginTop: '0.15rem' }}>
                  {formatDate(w.monday_date)} – {formatDate(w.friday_date)}
                </span>
              )}
            </span>
            <span className="small muted">{w.lecture_count} lectures · {w.material_count} files</span>
            <span aria-hidden="true" className="muted">{open === w.week_num ? '−' : '+'}</span>
          </button>
          {open === w.week_num && <WeekBody courseId={course.id} weekNum={w.week_num} takeaway={w.takeaway} />}
        </div>
      ))}
    </div>
  );
}

function WeekBody({ courseId, weekNum, takeaway }) {
  const { data, loading } = useApi(() => api.courses.week(courseId, weekNum), [courseId, weekNum]);
  if (loading) return <div className="week-body"><Loading /></div>;
  if (!data) return null;

  return (
    <div className="week-body">
      {takeaway && (
        <blockquote style={{ margin: 0, padding: '0.75rem 1rem', background: 'var(--gold-050)', borderLeft: '3px solid var(--gold-500)', fontFamily: 'var(--serif)', fontSize: 'var(--t-sm)' }}>
          {takeaway}
        </blockquote>
      )}

      {data.lectures.length > 0 && (
        <>
          <h5>Lectures</h5>
          <ul className="file-list">
            {data.lectures.map((l) => (
              <li key={l.id}>
                <Link to={`/portal/lectures/${l.id}`}>
                  <span className="file-ext">{l.code || 'L'}</span>
                  <span className="grow">{l.title}</span>
                  {l.date_iso && <span className="tiny muted">{formatDate(l.date_iso)}</span>}
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}

      {data.assessments.length > 0 && (
        <>
          <h5>Assessment set this week</h5>
          <ul className="file-list">
            {data.assessments.map((a) => (
              <li key={a.id}>
                <Link to={`/portal/work/${a.id}`}>
                  <span className="file-ext">{a.kind}</span>
                  <span className="grow">{a.label}{a.topic ? ` — ${a.topic}` : ''}</span>
                  <DueDate date={a.due_date} time={a.due_time} short />
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}

      {data.materials.length > 0 && (
        <>
          <h5>Files</h5>
          <ul className="file-list">
            {data.materials.map((m) => (
              <li key={m.id}>
                <Link to={`/portal/materials/${m.id}`}>
                  <span className="file-ext">{(m.ext || '').replace('.', '') || m.kind}</span>
                  <span className="grow">{m.title}</span>
                  <span className="tiny muted">{m.kind}</span>
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}

      {data.readme && (
        <details style={{ marginTop: '1.5rem' }}>
          <summary className="small" style={{ cursor: 'pointer', color: 'var(--navy-600)' }}>
            Week overview
          </summary>
          <div style={{ marginTop: '1rem' }}>
            <Markdown source={data.readme} className="prose prose-wide" />
          </div>
        </details>
      )}
    </div>
  );
}

function Work({ rows, isStaff }) {
  if (!rows) return <Loading />;
  if (!rows.length) return <div className="empty">No assessments recorded for this course.</div>;

  return (
    <div className="card table-wrap">
      <table className="table">
        <thead>
          <tr>
            <th>Item</th><th>Component</th><th>Type</th><th>Due</th>
            <th className="num">Points</th><th className="num">Mark</th><th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((a) => (
            <tr key={a.id}>
              <td>
                <Link to={isStaff ? `/portal/marking/${a.id}` : `/portal/work/${a.id}`}
                  style={{ fontWeight: 600, textDecoration: 'none' }}>{a.label}</Link>
                {a.topic && <div className="tiny muted" style={{ marginTop: '0.15rem' }}>{a.topic}</div>}
              </td>
              <td className="small muted">{a.component || '—'}</td>
              <td><KindBadge kind={a.kind} /></td>
              <td><DueDate date={a.due_date} time={a.due_time} /></td>
              <td className="num tnum">{a.possible || '—'}</td>
              <td className="num tnum">
                {a.excused ? <span className="muted">EX</span>
                  : a.score !== null && a.score !== undefined
                    ? <strong>{a.score}</strong>
                    : <span className="muted">—</span>}
              </td>
              <td><StatusBadge status={a.submission_status} score={a.score} excused={a.excused} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Grades({ grade, courseId }) {
  if (!grade) return <div className="empty">No gradebook for this course.</div>;
  return (
    <>
      <div className="row" style={{ gap: '2rem', marginBottom: '2rem', alignItems: 'center' }}>
        <GradeDial percent={grade.percent} letter={grade.letter?.letter} size={120} />
        <div>
          <span className="label">Running grade</span>
          <p className="small muted" style={{ maxWidth: '46ch' }}>
            {grade.percent === null
              ? 'Nothing has been marked yet.'
              : grade.complete
                ? 'Every component is complete — this is the final grade.'
                : `Computed from the ${grade.graded_weight}% of the course that has been marked so far. It will move as more work comes back.`}
          </p>
          <Link to="/portal/grades" className="small">All courses →</Link>
        </div>
      </div>

      <div className="stack-lg">
        {grade.components.map((c) => (
          <div key={c.id} className="card">
            <div className="component-head">
              <div>
                <h4>{c.name}</h4>
                <span className="tiny muted">
                  {c.formative ? 'Formative — does not count toward the grade' : `${c.weight}% of the course`}
                  {c.drop_lowest > 0 && ` · lowest ${c.drop_lowest} dropped`}
                </span>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div className="tnum" style={{ fontFamily: 'var(--serif)', fontSize: 'var(--t-lg)' }}>
                  {c.percent === null ? '—' : pct(c.percent)}
                </div>
                <span className="tiny muted">{c.graded_count} of {c.item_count} marked</span>
              </div>
            </div>
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr><th>Item</th><th>Topic</th><th className="num">Score</th><th className="num">Out of</th><th className="num">%</th><th>Feedback</th></tr>
                </thead>
                <tbody>
                  {c.items.map((it) => (
                    <tr key={it.id}>
                      <td><Link to={`/portal/work/${it.id}`} style={{ textDecoration: 'none', fontWeight: 600 }}>{it.label}</Link></td>
                      <td className="small muted">{it.topic || '—'}</td>
                      <td className="num tnum">{it.excused ? 'EX' : it.score ?? '—'}</td>
                      <td className="num tnum muted">{it.possible}</td>
                      <td className="num tnum">
                        {it.score !== null && it.score !== undefined && !it.excused && it.possible
                          ? pct((it.score / it.possible) * 100, 0) : '—'}
                      </td>
                      <td className="small muted">{it.feedback || ''}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

function About({ course }) {
  return (
    <div className="grid grid-sidebar">
      <div className="stack-lg">
        {course.announcements.length > 0 && (
          <div className="card">
            <div className="card-head"><h3>Announcements</h3></div>
            <div className="card-body stack">
              {course.announcements.map((a) => (
                <div key={a.id}>
                  <strong style={{ fontFamily: 'var(--serif)' }}>{a.title}</strong>
                  <p className="small" style={{ marginTop: '0.25rem' }}>{a.body}</p>
                  <span className="tiny muted">{formatDate(a.created_at)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="card">
          <div className="card-head"><h3>How this course is marked</h3></div>
          <table className="table">
            <thead><tr><th>Component</th><th className="num">Weight</th><th>Rule</th></tr></thead>
            <tbody>
              {course.components.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}</td>
                  <td className="num tnum">{c.formative ? '—' : `${c.weight}%`}</td>
                  <td className="small muted">
                    {c.formative ? 'Formative, ungraded' : c.drop_lowest > 0 ? `Lowest ${c.drop_lowest} dropped` : ''}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <aside className="stack-lg">
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
                  <div className="tiny mono muted">{s.email}</div>
                  {s.office_hours && <p className="tiny muted" style={{ marginTop: '0.25rem' }}>{s.office_hours}</p>}
                </div>
              ))}
            </div>
          </div>
        )}
      </aside>
    </div>
  );
}
