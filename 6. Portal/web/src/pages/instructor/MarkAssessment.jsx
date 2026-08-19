import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { StatusBadge } from '../../components/Bits.jsx';
import { formatDateTime, bytes, pct } from '../../format.js';

/** One assessment, every enrolled student, marks entered inline. */
export default function MarkAssessment() {
  const { id } = useParams();
  const { data, loading, error, reload } = useApi(() => api.instructor.submissions(id), [id]);

  if (loading) return <Loading label="Loading submissions" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  const a = data.assessment;
  const marked = data.students.filter((s) => s.score !== null || s.excused).length;

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <Crumbs items={[
            { label: 'Portal', to: '/portal' },
            { label: 'Marking', to: '/portal/marking' },
            { label: `${a.course_code} ${a.label}` },
          ]} />
          <div className="row-between row-wrap" style={{ marginTop: '0.75rem' }}>
            <div>
              <span className="eyebrow">{a.course_code} · {a.course_title}</span>
              <h1 style={{ marginTop: '0.4rem' }}>{a.label}</h1>
              {a.topic && <p className="lede">{a.topic}</p>}
            </div>
            <div className="row" style={{ gap: '0.5rem' }}>
              <span className="badge badge-outline">{a.possible} points</span>
              <span className="badge badge-gold">{marked} of {data.students.length} marked</span>
            </div>
          </div>
        </div>
      </div>

      <div className="wrap section stack-lg">
        {data.students.map((s) => (
          <StudentRow key={s.student_id} student={s} assessment={a} onSaved={reload} />
        ))}
        {!data.students.length && <div className="card"><div className="empty">Nobody is enrolled in this course.</div></div>}
      </div>
    </>
  );
}

function StudentRow({ student: s, assessment: a, onSaved }) {
  const [score, setScore] = useState(s.score ?? '');
  const [feedback, setFeedback] = useState(s.feedback ?? '');
  const [excused, setExcused] = useState(Boolean(s.excused));
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);
  const [saved, setSaved] = useState(false);

  async function save() {
    setBusy(true); setErr(null); setSaved(false);
    try {
      await api.instructor.grade(a.id, {
        student_id: s.student_id,
        score: excused ? null : score,
        excused: excused ? 1 : 0,
        feedback: feedback || null,
      });
      setSaved(true);
      await onSaved();
    } catch (e) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  }

  const percent = !excused && score !== '' && a.possible
    ? pct((Number(score) / a.possible) * 100, 0) : null;

  return (
    <div className="card">
      <div className="card-head">
        <div>
          <h3>{s.full_name}</h3>
          <span className="tiny mono muted">{s.student_number}</span>
        </div>
        <div className="row" style={{ gap: '0.5rem' }}>
          {s.submitted_at && <span className="tiny muted">{formatDateTime(s.submitted_at)}</span>}
          <StatusBadge status={s.status} score={s.score} excused={s.excused} />
        </div>
      </div>

      <div className="card-body">
        {!s.submission_id && (
          <p className="small muted" style={{ marginBottom: '1rem' }}>
            Nothing handed in. You can still record a mark — an exam sat in a hall, for instance.
          </p>
        )}

        {s.files?.length > 0 && (
          <ul className="file-list" style={{ marginBottom: '1rem' }}>
            {s.files.map((f) => (
              <li key={f.id}>
                <a href={api.assessments.fileUrl(f.id)}>
                  <span className="file-ext">{(f.original_name.split('.').pop() || '').slice(0, 4)}</span>
                  <span className="grow">{f.original_name}</span>
                  <span className="tiny muted">{bytes(f.size_bytes)}</span>
                </a>
              </li>
            ))}
          </ul>
        )}

        {s.body_text && (
          <div style={{ marginBottom: '1rem' }}>
            <span className="label">Written answer</span>
            <pre style={{ whiteSpace: 'pre-wrap', fontSize: 'var(--t-sm)', background: 'var(--paper-alt)', padding: '0.85rem', borderRadius: '3px', margin: 0, maxHeight: '18rem', overflow: 'auto' }}>
              {s.body_text}
            </pre>
          </div>
        )}

        {s.comment && (
          <p className="small" style={{ marginBottom: '1rem' }}>
            <span className="label">Their note</span>{s.comment}
          </p>
        )}

        {err && <div className="notice notice-error" style={{ marginBottom: '1rem' }}>{err}</div>}

        <div className="row row-wrap" style={{ alignItems: 'flex-end', gap: '1rem' }}>
          <div className="field" style={{ width: '8rem' }}>
            <label htmlFor={`score-${s.student_id}`}>Score</label>
            <input id={`score-${s.student_id}`} className="input" type="number" min="0" step="0.5"
              value={score} disabled={excused}
              onChange={(e) => { setScore(e.target.value); setSaved(false); }}
              placeholder={`/ ${a.possible}`} />
          </div>
          {percent && <span className="badge badge-outline" style={{ marginBottom: '0.85rem' }}>{percent}</span>}
          <div className="field grow" style={{ minWidth: '16rem' }}>
            <label htmlFor={`fb-${s.student_id}`}>Feedback</label>
            <input id={`fb-${s.student_id}`} className="input" value={feedback}
              onChange={(e) => { setFeedback(e.target.value); setSaved(false); }}
              placeholder="What they did well, what to fix" />
          </div>
          <label className="row small" style={{ marginBottom: '0.85rem', gap: '0.4rem', textTransform: 'none', letterSpacing: 0 }}>
            <input type="checkbox" checked={excused}
              onChange={(e) => { setExcused(e.target.checked); setSaved(false); }} />
            Excused
          </label>
          <button className="btn" style={{ marginBottom: '0.5rem' }} onClick={save} disabled={busy}>
            {busy ? 'Saving…' : saved ? 'Saved ✓' : 'Save mark'}
          </button>
        </div>
      </div>
    </div>
  );
}
