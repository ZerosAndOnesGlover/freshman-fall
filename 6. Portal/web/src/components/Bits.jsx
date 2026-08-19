import { Link } from 'react-router-dom';
import { formatDateShort, daysUntil, kindLabel, pct } from '../format.js';

/** Where a piece of work stands, from the student's point of view. */
export function StatusBadge({ status, score, excused }) {
  if (excused) return <span className="badge badge-grey">Excused</span>;
  if (score !== null && score !== undefined) return <span className="badge badge-green">Marked</span>;
  switch (status) {
    case 'submitted': return <span className="badge badge-gold">Submitted</span>;
    case 'late':      return <span className="badge badge-amber">Submitted late</span>;
    case 'graded':    return <span className="badge badge-green">Marked</span>;
    case 'returned':  return <span className="badge badge-green">Returned</span>;
    case 'draft':     return <span className="badge badge-outline">Draft</span>;
    default:          return <span className="badge badge-outline">Not started</span>;
  }
}

/** A due date, coloured by how close it is. */
export function DueDate({ date, time, short = false }) {
  if (!date) return <span className="muted small">No set date</span>;
  const days = daysUntil(date);
  const tone = days < 0 ? 'badge-grey' : days <= 2 ? 'badge-red' : days <= 7 ? 'badge-amber' : 'badge-outline';
  const label = short ? formatDateShort(date) : `${formatDateShort(date)}${time ? ` · ${time}` : ''}`;
  return (
    <span className={`badge ${tone}`} title={days < 0 ? 'Past' : `In ${days} days`}>
      {label}
    </span>
  );
}

export function KindBadge({ kind }) {
  return <span className="badge badge-outline">{kindLabel(kind)}</span>;
}

/** The circular mark used on the grades pages. */
export function GradeDial({ percent, letter, size = 96 }) {
  const has = percent !== null && percent !== undefined;
  const r = (size - 10) / 2;
  const c = 2 * Math.PI * r;
  const filled = has ? Math.max(0, Math.min(100, percent)) / 100 : 0;

  return (
    <div style={{ position: 'relative', width: size, height: size, flexShrink: 0 }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }} aria-hidden="true">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--rule-soft)" strokeWidth="5" />
        {has && (
          <circle
            cx={size / 2} cy={size / 2} r={r} fill="none"
            stroke="var(--gold-500)" strokeWidth="5" strokeLinecap="round"
            strokeDasharray={c} strokeDashoffset={c * (1 - filled)}
          />
        )}
      </svg>
      <div style={{
        position: 'absolute', inset: 0, display: 'grid', placeItems: 'center',
        fontFamily: 'var(--serif)', lineHeight: 1.05, textAlign: 'center',
      }}>
        <div>
          <div style={{ fontSize: size > 80 ? '1.5rem' : '1.1rem', color: 'var(--navy-900)' }}>
            {letter || (has ? pct(percent, 0) : '—')}
          </div>
          {letter && has && (
            <div className="tiny muted" style={{ fontFamily: 'var(--sans)' }}>{pct(percent)}</div>
          )}
        </div>
      </div>
    </div>
  );
}

/** One line of coursework, used on the dashboard and the coursework list. */
export function WorkRow({ item, courseLink = true }) {
  return (
    <tr>
      <td>
        <Link to={`/portal/work/${item.id}`} style={{ fontWeight: 600, textDecoration: 'none' }}>
          {item.label}
        </Link>
        {item.topic && <div className="tiny muted" style={{ marginTop: '0.15rem' }}>{item.topic}</div>}
      </td>
      <td>
        {courseLink ? (
          <Link to={`/portal/courses/${item.course_id}`} className="mono small" style={{ textDecoration: 'none' }}>
            {item.course_code}
          </Link>
        ) : <span className="mono small">{item.course_code}</span>}
      </td>
      <td><KindBadge kind={item.kind} /></td>
      <td><DueDate date={item.due_date} time={item.due_time} /></td>
      <td className="num tnum">{item.possible || '—'}</td>
      <td><StatusBadge status={item.submission_status} score={item.score} excused={item.excused} /></td>
    </tr>
  );
}

export function StatTile({ label, value, unit, foot }) {
  return (
    <div className="card stat">
      <div className="label">{label}</div>
      <div className="value">
        {value}{unit && <small> {unit}</small>}
      </div>
      {foot && <div className="foot">{foot}</div>}
    </div>
  );
}
