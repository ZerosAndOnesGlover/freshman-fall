import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote } from '../../components/Chrome.jsx';
import { DueDate, KindBadge, StatusBadge } from '../../components/Bits.jsx';
import { DatePicker } from '../../components/DatePicker.jsx';
import {
  todayIso, addDays, startOfWeek, weekdayName, minutesOf, formatDate,
} from '../../format.js';

/**
 * The timetable runs off the browser's clock, not the server's: the student's
 * own device decides what "today" is.
 */
export default function Timetable() {
  const [today, setToday] = useState(() => todayIso());
  const [date, setDate] = useState(() => todayIso());
  const [now, setNow] = useState(() => new Date());

  // Keep "today" honest if the page is left open across midnight.
  useEffect(() => {
    const tick = setInterval(() => {
      setNow(new Date());
      const t = todayIso();
      setToday((prev) => (prev === t ? prev : t));
    }, 60_000);
    return () => clearInterval(tick);
  }, []);

  const { data, loading, error, reload } = useApi(() => api.timetable.day(date), [date]);

  const weekStart = startOfWeek(date);
  const week = Array.from({ length: 7 }, (_, i) => addDays(weekStart, i));
  const { data: range } = useApi(
    () => api.timetable.range(week[0], week[6]),
    [week[0], week[6]],
  );

  const [monthMarks, setMonthMarks] = useState({});
  const loadMonth = useCallback((from, to) => {
    api.timetable.range(from, to)
      .then((r) => setMonthMarks(r.days || {}))
      .catch(() => setMonthMarks({}));
  }, []);

  const isToday = date === today;
  const minutesNow = isToday ? now.getHours() * 60 + now.getMinutes() : null;

  return (
    <>
      <div className="page-head">
        <div className="wrap row-between row-wrap">
          <div>
            <span className="eyebrow">{weekdayName(date)} · {formatDate(date, { year: true })}</span>
            <h1 style={{ marginTop: '0.5rem' }}>
              {isToday ? 'Today' : date === addDays(today, 1) ? 'Tomorrow'
                : date === addDays(today, -1) ? 'Yesterday' : 'Timetable'}
            </h1>
          </div>
          <div className="row row-wrap" style={{ gap: '0.5rem' }}>
            <DatePicker
              value={date}
              onChange={setDate}
              marks={monthMarks}
              onMonthChange={loadMonth}
              align="right"
              label="Show a different date"
            />
            {!isToday && (
              <button className="btn btn-ghost btn-sm" onClick={() => setDate(today)}>Today</button>
            )}
          </div>
        </div>
      </div>

      <div className="wrap section">
        <WeekStrip week={week} date={date} today={today} counts={range?.days || {}}
          onPick={setDate}
          onShift={(d) => setDate(addDays(date, d))} />

        {loading && <Loading label="Loading your day" />}
        <ErrorNote error={error} onRetry={reload} />

        {data && (
          <div className="grid grid-sidebar" style={{ marginTop: '2rem' }}>
            <div>
              <h2 className="rule-gold" style={{ fontSize: 'var(--t-lg)', marginBottom: '1.5rem' }}>
                {data.lectures.length
                  ? `${data.lectures.length} ${data.lectures.length === 1 ? 'lecture' : 'lectures'}`
                  : 'Lectures'}
              </h2>

              {data.lectures.length ? (
                <ol className="day-list">
                  {data.lectures.map((l) => {
                    const start = minutesOf(l.start_time);
                    const end = minutesOf(l.end_time) ?? (start !== null ? start + 50 : null);
                    const state = minutesNow === null || start === null ? null
                      : minutesNow >= start && minutesNow <= end ? 'now'
                      : minutesNow > end ? 'past' : 'soon';
                    return (
                      <li key={l.id} className={`day-item${state ? ` is-${state}` : ''}`}>
                        <div className="day-time">
                          <span className="mono">{l.start_time || '—'}</span>
                          {l.end_time && <span className="tiny muted">{l.end_time}</span>}
                        </div>
                        <div className="day-body">
                          <div className="row row-wrap" style={{ gap: '0.5rem' }}>
                            <Link to={`/portal/courses/${l.course_id}`} className="pill"
                              style={{ textDecoration: 'none' }}>{l.course_code}</Link>
                            {l.code && <span className="badge badge-outline">{l.code}</span>}
                            {state === 'now' && <span className="badge badge-gold">On now</span>}
                            {l.week_num !== null && <span className="tiny muted">Week {l.week_num}</span>}
                          </div>
                          <h3 style={{ fontSize: 'var(--t-md)', marginTop: '0.4rem' }}>
                            <Link to={`/portal/lectures/${l.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                              {l.title}
                            </Link>
                          </h3>
                          {l.instructor && <p className="tiny muted" style={{ marginTop: '0.25rem' }}>{l.instructor}</p>}
                        </div>
                      </li>
                    );
                  })}
                </ol>
              ) : (
                <div className="card"><div className="empty">
                  No lectures on {weekdayName(date)}.
                </div></div>
              )}
            </div>

            <aside className="stack-lg">
              <div className="card">
                <div className="card-head"><h3>Due this day</h3></div>
                {data.due.length ? (
                  <div className="card-body stack">
                    {data.due.map((d) => (
                      <div key={d.id}>
                        <div className="row" style={{ gap: '0.5rem' }}>
                          <span className="pill">{d.course_code}</span>
                          <KindBadge kind={d.kind} />
                        </div>
                        <Link to={`/portal/work/${d.id}`}
                          style={{ display: 'block', marginTop: '0.35rem', fontWeight: 600, textDecoration: 'none' }}>
                          {d.label}
                        </Link>
                        <div className="row" style={{ gap: '0.5rem', marginTop: '0.3rem' }}>
                          {d.due_time && <span className="tiny muted">{d.due_time}</span>}
                          <StatusBadge status={d.submission_status} score={d.score} />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : <div className="empty" style={{ padding: '1.5rem' }}>Nothing due.</div>}
              </div>

              {data.events.length > 0 && (
                <div className="card">
                  <div className="card-head"><h3>On the calendar</h3></div>
                  <div className="card-body stack-sm">
                    {data.events.map((e) => (
                      <div key={e.id}>
                        <strong className="small">{e.title}</strong>
                        {e.detail && <div className="tiny muted">{e.detail}</div>}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </aside>
          </div>
        )}
      </div>
    </>
  );
}

function WeekStrip({ week, date, today, counts, onPick, onShift }) {
  return (
    <div className="week-strip">
      <button className="btn btn-quiet" onClick={() => onShift(-7)} aria-label="Previous week">‹</button>
      <div className="week-days">
        {week.map((d) => {
          const c = counts[d] || {};
          const classes = ['week-day'];
          if (d === date) classes.push('is-selected');
          if (d === today) classes.push('is-today');
          return (
            <button key={d} className={classes.join(' ')} onClick={() => onPick(d)}>
              <span className="wd">{weekdayName(d, true)}</span>
              <span className="dd">{Number(d.slice(8, 10))}</span>
              <span className="dots">
                {c.lectures ? <i className="dot dot-lecture" title={`${c.lectures} lectures`} /> : null}
                {c.due ? <i className="dot dot-due" title={`${c.due} due`} /> : null}
              </span>
            </button>
          );
        })}
      </div>
      <button className="btn btn-quiet" onClick={() => onShift(7)} aria-label="Next week">›</button>
    </div>
  );
}
