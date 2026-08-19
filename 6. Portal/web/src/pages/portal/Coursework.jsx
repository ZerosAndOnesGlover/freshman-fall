import { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';
import { WorkRow } from '../../components/Bits.jsx';

export default function Coursework() {
  const [days, setDays] = useState(60);
  const { data: upcoming, loading, error, reload } = useApi(() => api.assessments.upcoming(days), [days]);
  const { data: outstanding } = useApi(() => api.assessments.outstanding(), []);

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <h1>Coursework</h1>
          <p className="lede">Everything due across your courses, soonest first.</p>
        </div>
      </div>

      <div className="wrap section stack-lg">
        {outstanding?.length > 0 && (
          <section className="card" style={{ borderColor: 'var(--amber-600)' }}>
            <div className="card-head" style={{ background: 'var(--amber-050)' }}>
              <h3>Past due and not handed in</h3>
              <span className="badge badge-amber">{outstanding.length}</span>
            </div>
            <div className="table-wrap">
              <table className="table">
                <thead><tr><th>Assessment</th><th>Course</th><th>Was due</th><th className="num">Points</th></tr></thead>
                <tbody>
                  {outstanding.map((o) => (
                    <tr key={o.id}>
                      <td><Link to={`/portal/work/${o.id}`} style={{ fontWeight: 600, textDecoration: 'none' }}>{o.label}</Link></td>
                      <td className="mono small">{o.course_code}</td>
                      <td className="small muted">{o.due_date}</td>
                      <td className="num tnum">{o.possible}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="card-foot muted">
              Late work is still accepted — it is recorded as late rather than refused.
            </div>
          </section>
        )}

        <section className="card">
          <div className="card-head">
            <h3>Upcoming</h3>
            <select className="select" style={{ width: 'auto' }} value={days}
              onChange={(e) => setDays(Number(e.target.value))} aria-label="Time range">
              <option value={14}>Next 2 weeks</option>
              <option value={30}>Next month</option>
              <option value={60}>Next 2 months</option>
              <option value={365}>Rest of the year</option>
            </select>
          </div>
          {loading && <Loading />}
          <ErrorNote error={error} onRetry={reload} />
          {upcoming?.length ? (
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr><th>Assessment</th><th>Course</th><th>Type</th><th>Due</th><th className="num">Points</th><th>Status</th></tr>
                </thead>
                <tbody>
                  {upcoming.map((u) => <WorkRow key={u.id} item={u} />)}
                </tbody>
              </table>
            </div>
          ) : !loading && <div className="empty">Nothing due in this window.</div>}
        </section>
      </div>
    </>
  );
}
