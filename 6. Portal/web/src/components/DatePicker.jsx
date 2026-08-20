import { useState, useRef, useEffect, useCallback, useId } from 'react';
import { todayIso, addDays, formatDate, weekdayName } from '../format.js';

/**
 * A calendar in the portal's own design.
 *
 * `<input type="date">` hands the whole interaction to the browser, which
 * renders its own widget in its own typography — and gives no way to show
 * which days actually have anything on them. This draws the month itself, so
 * it can mark the days that carry lectures or deadlines.
 *
 * Props
 *   value    ISO date string, or ''
 *   onChange (iso) => void
 *   marks    { "2026-08-20": { lectures: 3, due: 1 } } — optional activity dots
 *   onMonthChange (firstIso, lastIso) => void — to load marks for a month
 *   min/max  ISO bounds, optional
 *   clearable  show a "Clear" action
 */
export function DatePicker({
  value = '',
  onChange,
  marks = null,
  onMonthChange = null,
  min = null,
  max = null,
  clearable = false,
  placeholder = 'Choose a date',
  label = 'Choose a date',
  align = 'left',
}) {
  const [open, setOpen] = useState(false);
  const [cursor, setCursor] = useState(() => firstOfMonth(value || todayIso()));
  const [focused, setFocused] = useState(value || todayIso());

  const rootRef = useRef(null);
  const triggerRef = useRef(null);
  const gridRef = useRef(null);
  const panelId = useId();

  const today = todayIso();

  // Reopening should land on the month of the current value.
  useEffect(() => {
    if (open) {
      const start = value || today;
      setCursor(firstOfMonth(start));
      setFocused(start);
    }
  }, [open]);   // eslint-disable-line react-hooks/exhaustive-deps

  // Let the caller load activity for whatever month is on screen.
  useEffect(() => {
    if (!open || !onMonthChange) return;
    const days = monthGrid(cursor);
    onMonthChange(days[0], days[days.length - 1]);
  }, [open, cursor, onMonthChange]);

  const close = useCallback((returnFocus = true) => {
    setOpen(false);
    if (returnFocus) triggerRef.current?.focus();
  }, []);

  // Clicking elsewhere, or pressing Escape, dismisses the panel.
  useEffect(() => {
    if (!open) return;
    const onDown = (e) => { if (!rootRef.current?.contains(e.target)) setOpen(false); };
    const onKey = (e) => { if (e.key === 'Escape') { e.stopPropagation(); close(); } };
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey, true);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey, true);
    };
  }, [open, close]);

  // Roving focus inside the grid.
  useEffect(() => {
    if (!open) return;
    const el = gridRef.current?.querySelector(`[data-iso="${focused}"]`);
    el?.focus();
  }, [open, focused]);

  const blocked = (iso) => (min && iso < min) || (max && iso > max);

  function pick(iso) {
    if (blocked(iso)) return;
    onChange?.(iso);
    close();
  }

  function onGridKey(e) {
    const moves = {
      ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7,
      PageUp: -28, PageDown: 28,
    };
    if (e.key in moves) {
      e.preventDefault();
      const next = addDays(focused, moves[e.key]);
      setFocused(next);
      if (next.slice(0, 7) !== cursor.slice(0, 7)) setCursor(firstOfMonth(next));
      return;
    }
    if (e.key === 'Home' || e.key === 'End') {
      e.preventDefault();
      const days = monthDays(cursor);
      setFocused(e.key === 'Home' ? days[0] : days[days.length - 1]);
      return;
    }
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      pick(focused);
    }
  }

  const grid = monthGrid(cursor);
  const monthLabel = new Date(`${cursor}T12:00:00`)
    .toLocaleString('en-GB', { month: 'long', year: 'numeric' });

  return (
    <div className="datepicker" ref={rootRef}>
      <button
        type="button"
        ref={triggerRef}
        className={`datepicker-trigger${open ? ' is-open' : ''}`}
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="dialog"
        aria-expanded={open}
        aria-controls={open ? panelId : undefined}
        aria-label={label}
      >
        <CalendarGlyph />
        <span className={value ? '' : 'muted'}>
          {value ? formatDate(value, { year: true }) : placeholder}
        </span>
        <span className="datepicker-caret" aria-hidden="true">▾</span>
      </button>

      {open && (
        <div className={`datepicker-panel align-${align}`} id={panelId} role="dialog" aria-label={label}>
          <div className="datepicker-head">
            <button type="button" className="datepicker-nav"
              onClick={() => setCursor(shiftMonth(cursor, -1))} aria-label="Previous month">‹</button>
            <strong>{monthLabel}</strong>
            <button type="button" className="datepicker-nav"
              onClick={() => setCursor(shiftMonth(cursor, 1))} aria-label="Next month">›</button>
          </div>

          <div className="datepicker-weekdays" aria-hidden="true">
            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((d) => <span key={d}>{d.slice(0, 2)}</span>)}
          </div>

          <div className="datepicker-grid" ref={gridRef} role="grid" onKeyDown={onGridKey}>
            {grid.map((iso) => {
              const outside = iso.slice(0, 7) !== cursor.slice(0, 7);
              const mark = marks?.[iso];
              const classes = ['datepicker-day'];
              if (outside) classes.push('is-outside');
              if (iso === value) classes.push('is-selected');
              if (iso === today) classes.push('is-today');
              if (blocked(iso)) classes.push('is-blocked');
              return (
                <button
                  key={iso}
                  type="button"
                  data-iso={iso}
                  className={classes.join(' ')}
                  tabIndex={iso === focused ? 0 : -1}
                  disabled={blocked(iso)}
                  aria-selected={iso === value}
                  aria-label={`${weekdayName(iso)} ${formatDate(iso, { year: true })}`}
                  onClick={() => pick(iso)}
                  onFocus={() => setFocused(iso)}
                >
                  <span>{Number(iso.slice(8, 10))}</span>
                  {mark && (
                    <span className="datepicker-dots" aria-hidden="true">
                      {mark.lectures ? <i className="dot dot-lecture" /> : null}
                      {mark.due ? <i className="dot dot-due" /> : null}
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          <div className="datepicker-foot">
            <button type="button" className="btn btn-quiet btn-sm" onClick={() => pick(today)}>
              Today
            </button>
            {clearable && value && (
              <button type="button" className="btn btn-quiet btn-sm"
                onClick={() => { onChange?.(''); close(); }}>
                Clear
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function CalendarGlyph() {
  return (
    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"
      stroke="currentColor" strokeWidth="1.4" strokeLinecap="round">
      <rect x="2" y="3" width="12" height="11" rx="1.5" />
      <path d="M2 6.5h12M5.5 1.8v2.4M10.5 1.8v2.4" />
    </svg>
  );
}

// ─── date helpers, all on local calendar parts ─────────────────────────

function firstOfMonth(iso) {
  return `${iso.slice(0, 7)}-01`;
}

function shiftMonth(iso, by) {
  const [y, m] = iso.split('-').map(Number);
  const d = new Date(y, m - 1 + by, 1);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-01`;
}

function monthDays(cursorIso) {
  const [y, m] = cursorIso.split('-').map(Number);
  const count = new Date(y, m, 0).getDate();
  return Array.from({ length: count }, (_, i) =>
    `${y}-${String(m).padStart(2, '0')}-${String(i + 1).padStart(2, '0')}`);
}

/** Six weeks, Monday first, so the panel never changes height. */
function monthGrid(cursorIso) {
  const days = monthDays(cursorIso);
  const first = days[0];
  const [y, m] = first.split('-').map(Number);
  const lead = (new Date(y, m - 1, 1).getDay() + 6) % 7;   // Sunday = 0 -> 6
  const start = addDays(first, -lead);
  return Array.from({ length: 42 }, (_, i) => addDays(start, i));
}
