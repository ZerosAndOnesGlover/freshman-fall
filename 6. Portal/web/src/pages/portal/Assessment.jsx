import { useState, useRef, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { StatusBadge, DueDate, KindBadge } from '../../components/Bits.jsx';
import { Markdown } from '../../markdown.jsx';
import { formatDateTime, formatDate, bytes, daysUntil, pct } from '../../format.js';

export default function Assessment() {
  const { id } = useParams();
  const { data, loading, error, reload } = useApi(() => api.assessments.one(id), [id]);

  if (loading) return <Loading label="Loading assessment" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <Crumbs items={[
            { label: 'Portal', to: '/portal' },
            { label: data.course_code, to: `/portal/courses/${data.course_id}` },
            { label: data.label },
          ]} />
          <div className="row-between row-wrap" style={{ marginTop: '0.75rem', alignItems: 'flex-end' }}>
            <div>
              <span className="eyebrow">
                {data.course_code} · {data.component || 'Assessment'}
                {data.week_num !== null && data.week_num !== undefined ? ` · Week ${data.week_num}` : ''}
              </span>
              <h1 style={{ marginTop: '0.4rem' }}>{data.label}</h1>
              {data.topic && <p className="lede">{data.topic}</p>}
            </div>
            <div className="row row-wrap" style={{ gap: '0.5rem' }}>
              <KindBadge kind={data.kind} />
              <DueDate date={data.due_date} time={data.due_time} />
              <span className="badge badge-outline">{data.possible} points</span>
              {data.component_weight > 0 && (
                <span className="badge badge-outline">{data.component} · {data.component_weight}%</span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="wrap section">
        <div className="grid grid-sidebar">
          <div>
            {data.brief_md
              ? <Markdown source={data.brief_md} dropFirstHeading links={data.brief_links} />
              : (
                <div className="card">
                  <div className="empty">
                    No brief has been published for this assessment.
                    {data.room && <div className="small" style={{ marginTop: '1rem' }}>Sat in {data.room}.</div>}
                  </div>
                </div>
              )}
          </div>

          <aside className="stack-lg">
            <GradePanel grade={data.grade} possible={data.possible} />
            {data.accepts_upload
              ? <SubmitPanel assessment={data} onChange={reload} />
              : <NotSubmittable assessment={data} />}
          </aside>
        </div>
      </div>
    </>
  );
}

function GradePanel({ grade, possible }) {
  if (!grade || (grade.score === null && !grade.excused)) return null;
  return (
    <div className="card">
      <div className="card-head"><h3>Your mark</h3></div>
      <div className="card-body">
        {grade.excused ? (
          <p><span className="badge badge-grey">Excused</span></p>
        ) : (
          <>
            <div className="row" style={{ alignItems: 'baseline', gap: '0.5rem' }}>
              <span style={{ fontFamily: 'var(--serif)', fontSize: 'var(--t-2xl)' }} className="tnum">{grade.score}</span>
              <span className="muted">/ {possible}</span>
              <span className="badge badge-green" style={{ marginLeft: 'auto' }}>
                {pct((grade.score / possible) * 100, 0)}
              </span>
            </div>
            <div className="meter meter-gold" style={{ marginTop: '0.85rem' }}>
              <span style={{ width: `${Math.min(100, (grade.score / possible) * 100)}%` }} />
            </div>
          </>
        )}
        {grade.feedback && (
          <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid var(--rule-soft)' }}>
            <span className="label">Feedback</span>
            <p className="small">{grade.feedback}</p>
          </div>
        )}
        <p className="tiny muted" style={{ marginTop: '1rem' }}>
          {grade.source === 'registry'
            ? 'Recorded by the registry.'
            : `Marked by ${grade.graded_by_name || 'staff'}${grade.graded_at ? ` on ${formatDate(grade.graded_at)}` : ''}.`}
        </p>
      </div>
    </div>
  );
}

function NotSubmittable({ assessment }) {
  return (
    <div className="card card-pad">
      <span className="label">Submission</span>
      <p className="small muted">
        This assessment is not handed in through the portal.
        {assessment.room ? ` It is sat in ${assessment.room}.` : ' It is marked by your instructor directly.'}
      </p>
      {assessment.due_date && (
        <p className="small" style={{ marginTop: '0.75rem' }}>
          <strong>{formatDate(assessment.due_date, { weekday: true })}</strong>
          {assessment.due_time && ` at ${assessment.due_time}`}
        </p>
      )}
    </div>
  );
}

function SubmitPanel({ assessment, onChange }) {
  const sub = assessment.submission;
  const locked = sub && sub.status !== 'draft';
  const marked = assessment.grade && (assessment.grade.score !== null || assessment.grade.excused);

  const [text, setText] = useState(sub?.body_text || '');
  const [comment, setComment] = useState(sub?.comment || '');
  const [busy, setBusy] = useState(null);
  const [err, setErr] = useState(null);
  const [note, setNote] = useState(null);
  const [over, setOver] = useState(false);
  const fileRef = useRef(null);

  useEffect(() => {
    setText(sub?.body_text || '');
    setComment(sub?.comment || '');
  }, [sub?.id, sub?.status]);

  const days = daysUntil(assessment.due_date);
  const willBeLate = days !== null && days < 0;

  async function run(what, fn) {
    setBusy(what); setErr(null); setNote(null);
    try {
      await fn();
      await onChange();
    } catch (e) {
      setErr(e.message);
    } finally {
      setBusy(null);
    }
  }

  const saveDraft = () => run('save', async () => {
    await api.assessments.saveDraft(assessment.id, { body_text: text, comment });
    setNote('Draft saved.');
  });

  const submit = () => run('submit', () => api.assessments.submit(assessment.id, { body_text: text, comment }));
  const unsubmit = () => run('unsubmit', () => api.assessments.unsubmit(assessment.id));

  const addFiles = (files) => {
    if (!files?.length) return;
    run('upload', () => api.assessments.uploadFiles(assessment.id, Array.from(files)));
  };

  return (
    <div className="card">
      <div className="card-head">
        <h3>Your submission</h3>
        <StatusBadge status={sub?.status} score={assessment.grade?.score} excused={assessment.grade?.excused} />
      </div>
      <div className="card-body">
        {err && <div className="notice notice-error" style={{ marginBottom: '1rem' }}>{err}</div>}
        {note && <div className="notice notice-ok" style={{ marginBottom: '1rem' }}>{note}</div>}

        {locked ? (
          <>
            <p className="small">
              Handed in {sub.submitted_at ? formatDateTime(sub.submitted_at) : ''}
              {sub.status === 'late' && <span className="badge badge-amber" style={{ marginLeft: '0.5rem' }}>Late</span>}
            </p>

            {sub.files?.length > 0 && (
              <ul className="file-list" style={{ marginTop: '1rem' }}>
                {sub.files.map((f) => (
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

            {sub.body_text && (
              <div style={{ marginTop: '1rem' }}>
                <span className="label">What you wrote</span>
                <pre style={{ whiteSpace: 'pre-wrap', fontSize: 'var(--t-sm)', background: 'var(--paper-alt)', padding: '0.75rem', borderRadius: '3px', margin: 0 }}>
                  {sub.body_text}
                </pre>
              </div>
            )}

            {!marked && (
              <button className="btn btn-danger btn-block" style={{ marginTop: '1.25rem' }}
                onClick={unsubmit} disabled={busy}>
                {busy === 'unsubmit' ? 'Withdrawing…' : 'Withdraw and edit'}
              </button>
            )}
            {marked && (
              <p className="tiny muted" style={{ marginTop: '1rem' }}>
                This has been marked, so it can no longer be withdrawn.
              </p>
            )}
          </>
        ) : (
          <>
            {willBeLate && (
              <div className="notice notice-warn" style={{ marginBottom: '1rem' }}>
                The deadline has passed. This will be recorded as a late submission.
              </div>
            )}

            <div
              className={`dropzone${over ? ' over' : ''}`}
              onClick={() => fileRef.current?.click()}
              onDragOver={(e) => { e.preventDefault(); setOver(true); }}
              onDragLeave={() => setOver(false)}
              onDrop={(e) => { e.preventDefault(); setOver(false); addFiles(e.dataTransfer.files); }}
            >
              <input ref={fileRef} type="file" multiple
                onChange={(e) => { addFiles(e.target.files); e.target.value = ''; }} />
              <strong style={{ fontFamily: 'var(--serif)' }}>
                {busy === 'upload' ? 'Uploading…' : 'Drop files here'}
              </strong>
              <p className="tiny muted" style={{ marginTop: '0.35rem' }}>
                or click to choose · up to 25 MB each
              </p>
            </div>

            {sub?.files?.length > 0 && (
              <div style={{ marginTop: '1rem' }}>
                {sub.files.map((f) => (
                  <div key={f.id} className="upload-row">
                    <span className="file-ext">{(f.original_name.split('.').pop() || '').slice(0, 4)}</span>
                    <span className="grow">{f.original_name}</span>
                    <span className="tiny muted">{bytes(f.size_bytes)}</span>
                    <button className="btn-quiet btn btn-sm" title="Remove"
                      onClick={() => run('delete', () => api.assessments.deleteFile(f.id))}>×</button>
                  </div>
                ))}
              </div>
            )}

            <div className="field" style={{ marginTop: '1.5rem' }}>
              <label htmlFor="body">Written answer <span className="muted" style={{ textTransform: 'none', letterSpacing: 0 }}>(optional)</span></label>
              <textarea id="body" className="textarea" value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste code or write your answer here…" />
            </div>

            <div className="field">
              <label htmlFor="comment">Note to your instructor</label>
              <input id="comment" className="input" value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Anything they should know" />
            </div>

            <div className="row" style={{ marginTop: '1.5rem', gap: '0.5rem' }}>
              <button className="btn btn-ghost grow" onClick={saveDraft} disabled={busy}>
                {busy === 'save' ? 'Saving…' : 'Save draft'}
              </button>
              <button className="btn grow" onClick={submit} disabled={busy}>
                {busy === 'submit' ? 'Submitting…' : 'Hand in'}
              </button>
            </div>
            <p className="hint">
              You can withdraw and edit any time before it is marked.
            </p>
          </>
        )}
      </div>
    </div>
  );
}
