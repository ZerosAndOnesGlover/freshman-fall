import { useState } from 'react';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { formatDate } from '../../format.js';

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'];

const KIND_TONE = { assessment: 'badge-amber', holiday: 'badge-green', academic: 'badge-outline' };

export default function CalendarPage() {
  const { data: terms } = useApi(() => api.public.institution().then((d) => d.terms), []);
  const [termId, setTermId] = useState('');
  const [kind, setKind] = useState('all');

  const { data, loading, error, reload } = useApi(
    () => api.public.calendar(termId ? `?term=${termId}` : ''),
    [termId],
  );

  const events = (data || []).filter((e) => kind === 'all' || e.kind === kind);
  const today = new Date().toISOString().slice(0, 10);

  // Group by month, preserving the date order the API returned.
  const months = [];
  const seen = new Map();
  for (const e of events) {
    const key = e.date_iso.slice(0, 7);
    if (!seen.has(key)) {
      seen.set(key, { key, label: `${MONTHS[Number(key.slice(5, 7)) - 1]} ${key.slice(0, 4)}`, rows: [] });
      months.push(seen.get(key));
    }
    seen.get(key).rows.push(e);
  }

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <Crumbs items={[{ label: 'Home', to: '/' }, { label: 'Calendar' }]} />
          <h1>Academic Calendar</h1>
          <p className="lede">
            Term dates, assessment deadlines and holidays, drawn from the registry's
            assessment calendar.
          </p>
        </div>
      </div>

      <div className="wrap section">
        <div className="row row-wrap" style={{ marginBottom: '2rem' }}>
          <select className="select" style={{ maxWidth: '14rem' }} value={termId}
            onChange={(e) => setTermId(e.target.value)} aria-label="Filter by term">
            <option value="">All terms</option>
            {(terms || []).map((t) => (
              <option key={t.id} value={t.id}>{t.label}{t.is_current ? ' (current)' : ''}</option>
            ))}
          </select>
          <select className="select" style={{ maxWidth: '12rem' }} value={kind}
            onChange={(e) => setKind(e.target.value)} aria-label="Filter by kind">
            <option value="all">Everything</option>
            <option value="assessment">Assessments</option>
            <option value="academic">Academic dates</option>
            <option value="holiday">Holidays</option>
          </select>
          <span className="small muted">{events.length} entries</span>
        </div>

        {loading && <Loading />}
        <ErrorNote error={error} onRetry={reload} />

        {months.map((m) => (
          <div key={m.key} className="cal-month">
            <h3>{m.label}</h3>
            {m.rows.map((e) => (
              <div key={e.id} className={`cal-row${e.date_iso === today ? ' today' : ''}`}>
                <span className="cal-date">{formatDate(e.date_iso)}</span>
                <div>
                  <span>{e.title}</span>
                  {e.detail && <div className="tiny muted" style={{ marginTop: '0.15rem' }}>{e.detail}</div>}
                </div>
                <div className="row" style={{ gap: '0.4rem' }}>
                  {e.course_code && <span className="pill">{e.course_code}</span>}
                  <span className={`badge ${KIND_TONE[e.kind] || 'badge-outline'}`}>{e.kind}</span>
                </div>
              </div>
            ))}
          </div>
        ))}

        {!loading && !events.length && <div className="empty">No entries for this filter.</div>}
      </div>
    </>
  );
}
