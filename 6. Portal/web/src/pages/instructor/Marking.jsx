import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';
import { StatTile } from '../../components/Bits.jsx';
import { formatDateTime } from '../../format.js';

export default function Marking() {
  const { data, loading, error, reload } = useApi(() => api.instructor.queue(), []);
  const rows = data || [];

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <h1>Marking Queue</h1>
          <p className="lede">Work handed in across your courses and not yet marked.</p>
        </div>
      </div>

      <div className="wrap section">
        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />

        {rows.length > 0 ? (
          <div className="card table-wrap">
            <table className="table">
              <thead>
                <tr><th>Student</th><th>Course</th><th>Assessment</th><th>Handed in</th><th>Files</th><th className="num">Out of</th><th /></tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.submission_id}>
                    <td>
                      <strong>{r.student_name}</strong>
                      <div className="tiny mono muted">{r.student_number}</div>
                    </td>
                    <td className="mono small">{r.course_code}</td>
                    <td>{r.label}</td>
                    <td className="small">
                      {formatDateTime(r.submitted_at)}
                      {r.status === 'late' && <span className="badge badge-amber" style={{ marginLeft: '0.4rem' }}>Late</span>}
                    </td>
                    <td className="small muted">{r.file_count || '—'}</td>
                    <td className="num tnum">{r.possible}</td>
                    <td>
                      <Link to={`/portal/marking/${r.assessment_id}`} className="btn btn-sm btn-ghost">Mark</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : !loading && (
          <div className="card"><div className="empty">Nothing waiting. The queue is clear.</div></div>
        )}
      </div>
    </>
  );
}
