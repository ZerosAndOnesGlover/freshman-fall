import { useState } from 'react';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';
import { StatTile } from '../../components/Bits.jsx';
import { formatDate } from '../../format.js';

/**
 * The registry: academic sessions, intakes and student records.
 *
 * A session is a calendar academic year. Admitting a student to a session sets
 * their cohort, which is what allows a new intake to start Year 1 while an
 * earlier intake carries on in a later year.
 */
export default function Registry() {
  const [tab, setTab] = useState('overview');
  const overview = useApi(() => api.admin.overview(), []);
  const sessions = useApi(() => api.admin.sessions(), []);

  const refreshAll = () => { overview.reload(); sessions.reload(); };

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <span className="eyebrow">Office of the Registrar</span>
          <h1 style={{ marginTop: '0.5rem' }}>Registry</h1>
          <p className="lede">Academic sessions, intakes and student records.</p>
        </div>
      </div>

      <div className="subnav">
        <div className="wrap">
          {[['overview', 'Overview'], ['sessions', 'Sessions'], ['students', 'Students']].map(([k, l]) => (
            <a key={k} href="#" className={tab === k ? 'active' : undefined}
              onClick={(e) => { e.preventDefault(); setTab(k); }}>{l}</a>
          ))}
        </div>
      </div>

      <div className="wrap section">
        {tab === 'overview' && <Overview state={overview} />}
        {tab === 'sessions' && <Sessions state={sessions} onChange={refreshAll} />}
        {tab === 'students' && <Students sessions={sessions.data || []} onChange={refreshAll} />}
      </div>
    </>
  );
}

function Overview({ state }) {
  const { data, loading, error, reload } = state;
  if (loading) return <Loading />;
  if (error) return <ErrorNote error={error} onRetry={reload} />;

  return (
    <>
      <div className="grid grid-4" style={{ marginBottom: '2.5rem' }}>
        <StatTile label="Current session" value={data.current_session?.label || '—'}
          foot={data.current_session?.starts_on ? `from ${formatDate(data.current_session.starts_on)}` : 'none set'} />
        <StatTile label="Active students" value={data.students} foot={`${data.enrolments} enrolments`} />
        <StatTile label="Staff" value={data.staff} foot="instructors and registry" />
        <StatTile label="Courses" value={data.courses} foot="across the whole degree" />
      </div>

      <h2 className="rule-gold" style={{ fontSize: 'var(--t-lg)', marginBottom: '1.25rem' }}>Intakes</h2>
      <div className="card table-wrap">
        <table className="table">
          <thead><tr><th>Session</th><th className="num">Students</th><th>Status</th></tr></thead>
          <tbody>
            {data.intakes.map((i) => (
              <tr key={i.id}>
                <td style={{ fontWeight: 600 }}>{i.label}</td>
                <td className="num tnum">{i.students}</td>
                <td>{i.is_current ? <span className="badge badge-gold">Current</span>
                  : <span className="badge badge-outline">—</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

function Sessions({ state, onChange }) {
  const { data, loading, error, reload } = state;
  const [year, setYear] = useState(() => new Date().getFullYear() + 1);
  const [startsOn, setStartsOn] = useState('');
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState(null);
  const [err, setErr] = useState(null);

  async function run(fn, okMessage) {
    setBusy(true); setErr(null); setMsg(null);
    try { await fn(); setMsg(okMessage); reload(); onChange(); }
    catch (e) { setErr(e.message); }
    finally { setBusy(false); }
  }

  const create = () => run(
    () => api.admin.createSession({ start_year: Number(year), starts_on: startsOn || null, note: note || null }),
    `Session ${year}/${Number(year) + 1} created.`,
  );

  return (
    <div className="grid grid-sidebar">
      <div>
        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />
        {data && (
          <div className="card table-wrap">
            <table className="table">
              <thead>
                <tr><th>Session</th><th>Starts</th><th className="num">Students</th><th>Note</th><th /></tr>
              </thead>
              <tbody>
                {data.map((s) => (
                  <tr key={s.id}>
                    <td>
                      <strong>{s.label}</strong>
                      {s.is_current === 1 && <span className="badge badge-gold" style={{ marginLeft: '0.5rem' }}>Current</span>}
                    </td>
                    <td className="small muted">{s.starts_on ? formatDate(s.starts_on, { year: true }) : '—'}</td>
                    <td className="num tnum">{s.students}</td>
                    <td className="small muted">{s.note || ''}</td>
                    <td>
                      <div className="row" style={{ gap: '0.35rem', justifyContent: 'flex-end' }}>
                        {!s.is_current && (
                          <button className="btn btn-ghost btn-sm" disabled={busy}
                            onClick={() => run(() => api.admin.updateSession(s.id, { is_current: true }), `${s.label} is now the current session.`)}>
                            Make current
                          </button>
                        )}
                        {!s.is_current && s.students === 0 && (
                          <button className="btn btn-danger btn-sm" disabled={busy}
                            onClick={() => run(() => api.admin.deleteSession(s.id), `${s.label} removed.`)}>
                            Remove
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <aside>
        <div className="card">
          <div className="card-head"><h3>New session</h3></div>
          <div className="card-body">
            {err && <div className="notice notice-error" style={{ marginBottom: '1rem' }}>{err}</div>}
            {msg && <div className="notice notice-ok" style={{ marginBottom: '1rem' }}>{msg}</div>}

            <div className="field">
              <label htmlFor="year">Starting year</label>
              <input id="year" className="input" type="number" min="2000" max="2100"
                value={year} onChange={(e) => setYear(e.target.value)} />
              <p className="hint">This will be the {year}/{Number(year) + 1} session.</p>
            </div>
            <div className="field">
              <label htmlFor="starts">First day of term</label>
              <input id="starts" className="input" type="date"
                value={startsOn} onChange={(e) => setStartsOn(e.target.value)} />
            </div>
            <div className="field">
              <label htmlFor="note">Note</label>
              <input id="note" className="input" value={note}
                onChange={(e) => setNote(e.target.value)} placeholder="Optional" />
            </div>
            <button className="btn btn-block" style={{ marginTop: '1.25rem' }} onClick={create} disabled={busy}>
              {busy ? 'Working…' : 'Create session'}
            </button>
          </div>
        </div>
      </aside>
    </div>
  );
}

function Students({ sessions, onChange }) {
  const [q, setQ] = useState('');
  const [cohort, setCohort] = useState('');
  const query = `${cohort ? `?cohort=${cohort}` : ''}${q ? `${cohort ? '&' : '?'}q=${encodeURIComponent(q)}` : ''}`;
  const { data, loading, error, reload } = useApi(() => api.admin.students(query), [query]);
  const [issued, setIssued] = useState(null);   // {name, password}
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  const current = sessions.find((s) => s.is_current) || sessions[sessions.length - 1];
  const [form, setForm] = useState({ full_name: '', email: '', cohort_id: '', year_level: 1 });

  async function admit() {
    setBusy(true); setErr(null); setIssued(null);
    try {
      const r = await api.admin.admitStudent({
        ...form,
        cohort_id: Number(form.cohort_id || current?.id),
        year_level: Number(form.year_level),
      });
      setIssued({ name: r.student.full_name, id: r.student.student_id, password: r.temporary_password });
      setForm({ full_name: '', email: '', cohort_id: form.cohort_id, year_level: form.year_level });
      reload(); onChange();
    } catch (e) { setErr(e.message); }
    finally { setBusy(false); }
  }

  async function act(fn) {
    setBusy(true); setErr(null);
    try { await fn(); reload(); onChange(); }
    catch (e) { setErr(e.message); }
    finally { setBusy(false); }
  }

  return (
    <div className="grid grid-sidebar">
      <div>
        <div className="row row-wrap" style={{ marginBottom: '1.25rem' }}>
          <input className="input" style={{ maxWidth: '18rem' }} placeholder="Search name, email or number…"
            value={q} onChange={(e) => setQ(e.target.value)} />
          <select className="select" style={{ maxWidth: '12rem' }} value={cohort}
            onChange={(e) => setCohort(e.target.value)} aria-label="Filter by intake">
            <option value="">All intakes</option>
            {sessions.map((s) => <option key={s.id} value={s.id}>{s.label}</option>)}
          </select>
        </div>

        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />
        {err && <div className="notice notice-error" style={{ marginBottom: '1rem' }}>{err}</div>}

        {data && (
          <div className="card table-wrap">
            <table className="table">
              <thead>
                <tr><th>Student</th><th>Intake</th><th className="num">Year</th>
                  <th className="num">Courses</th><th>Status</th><th /></tr>
              </thead>
              <tbody>
                {data.map((s) => (
                  <tr key={s.id}>
                    <td>
                      <strong>{s.full_name}</strong>
                      <div className="tiny mono muted">{s.student_id} · {s.email}</div>
                    </td>
                    <td className="small">{s.cohort || '—'}</td>
                    <td className="num tnum">{s.year_level}</td>
                    <td className="num tnum">{s.courses}</td>
                    <td>{s.status === 'active'
                      ? <span className="badge badge-green">Active</span>
                      : <span className="badge badge-grey">Inactive</span>}</td>
                    <td>
                      <div className="row" style={{ gap: '0.35rem', justifyContent: 'flex-end' }}>
                        <button className="btn btn-ghost btn-sm" disabled={busy}
                          title={`Enrol in every Year ${s.year_level} course`}
                          onClick={() => act(() => api.admin.enrol(s.id, { year_num: s.year_level }))}>
                          Enrol Y{s.year_level}
                        </button>
                        <button className="btn btn-ghost btn-sm" disabled={busy}
                          onClick={() => act(async () => {
                            const r = await api.admin.resetPassword(s.id);
                            setIssued({ name: s.full_name, id: s.student_id, password: r.temporary_password });
                          })}>
                          Reset password
                        </button>
                        <button className="btn btn-quiet btn-sm" disabled={busy}
                          onClick={() => act(() => api.admin.updateStudent(s.id,
                            { status: s.status === 'active' ? 'inactive' : 'active' }))}>
                          {s.status === 'active' ? 'Deactivate' : 'Reactivate'}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!data.length && <div className="empty">No students match.</div>}
          </div>
        )}
      </div>

      <aside className="stack-lg">
        {issued && (
          <div className="card" style={{ borderColor: 'var(--gold-500)' }}>
            <div className="card-head" style={{ background: 'var(--gold-050)' }}>
              <h3>Temporary password</h3>
            </div>
            <div className="card-body">
              <p className="small">For <strong>{issued.name}</strong> ({issued.id}):</p>
              <p className="mono" style={{ fontSize: 'var(--t-md)', padding: '0.6rem', background: 'var(--paper-alt)', borderRadius: '3px', wordBreak: 'break-all' }}>
                {issued.password}
              </p>
              <p className="hint">
                Shown once. They will be asked to change it when they first sign in.
              </p>
              <button className="btn btn-ghost btn-sm btn-block" style={{ marginTop: '0.75rem' }}
                onClick={() => setIssued(null)}>Done</button>
            </div>
          </div>
        )}

        <div className="card">
          <div className="card-head"><h3>Admit a student</h3></div>
          <div className="card-body">
            <div className="field">
              <label htmlFor="nm">Full name</label>
              <input id="nm" className="input" value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
            </div>
            <div className="field">
              <label htmlFor="em">Email address</label>
              <input id="em" className="input" type="email" value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </div>
            <div className="field">
              <label htmlFor="co">Intake session</label>
              <select id="co" className="select" value={form.cohort_id || current?.id || ''}
                onChange={(e) => setForm({ ...form, cohort_id: e.target.value })}>
                {sessions.map((s) => (
                  <option key={s.id} value={s.id}>{s.label}{s.is_current ? ' (current)' : ''}</option>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="yl">Starting year of the degree</label>
              <select id="yl" className="select" value={form.year_level}
                onChange={(e) => setForm({ ...form, year_level: e.target.value })}>
                {[1, 2, 3, 4].map((y) => <option key={y} value={y}>Year {y}</option>)}
              </select>
            </div>
            <button className="btn btn-block" style={{ marginTop: '1.25rem' }}
              onClick={admit} disabled={busy || !form.full_name || !form.email}>
              {busy ? 'Working…' : 'Admit'}
            </button>
            <p className="hint">
              A registry number is issued automatically, and a temporary password
              is shown once for you to pass on.
            </p>
          </div>
        </div>
      </aside>
    </div>
  );
}
