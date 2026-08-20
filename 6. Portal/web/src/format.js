/** Display helpers. Dates in this vault are ISO strings or "YYYY-MM-DD HH:MM:SS". */

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'];
const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

function parse(value) {
  if (!value) return null;
  const iso = String(value).includes('T') ? value : String(value).replace(' ', 'T');
  const d = new Date(iso.length === 10 ? `${iso}T12:00:00` : iso);
  return Number.isNaN(d.getTime()) ? null : d;
}

export function formatDate(value, { weekday = false, year = false } = {}) {
  const d = parse(value);
  if (!d) return '—';
  const base = `${d.getDate()} ${MONTHS[d.getMonth()]}`;
  const parts = [];
  if (weekday) parts.push(DAYS[d.getDay()]);
  parts.push(year ? `${base} ${d.getFullYear()}` : base);
  return parts.join(' ');
}

export function formatDateShort(value) {
  const d = parse(value);
  if (!d) return '—';
  return `${d.getDate()} ${MONTHS[d.getMonth()].slice(0, 3)}`;
}

export function formatDateTime(value) {
  const d = parse(value);
  if (!d) return '—';
  const hh = String(d.getHours()).padStart(2, '0');
  const mm = String(d.getMinutes()).padStart(2, '0');
  return `${formatDate(value)} at ${hh}:${mm}`;
}

/** "in 3 days", "today", "2 days ago" — relative to local midnight. */
export function relativeDays(value) {
  const d = parse(value);
  if (!d) return null;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const then = new Date(d);
  then.setHours(0, 0, 0, 0);
  const days = Math.round((then - today) / 86400000);
  if (days === 0) return 'today';
  if (days === 1) return 'tomorrow';
  if (days === -1) return 'yesterday';
  if (days > 0) return `in ${days} days`;
  return `${Math.abs(days)} days ago`;
}

export function daysUntil(value) {
  const d = parse(value);
  if (!d) return null;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const then = new Date(d);
  then.setHours(0, 0, 0, 0);
  return Math.round((then - today) / 86400000);
}

export const pct = (v, digits = 1) => (v === null || v === undefined ? '—' : `${v.toFixed(digits)}%`);
export const gpa = (v) => (v === null || v === undefined ? '—' : v.toFixed(2));

export function initials(name) {
  if (!name) return '?';
  return name.trim().split(/\s+/).slice(0, 2).map((w) => w[0]).join('').toUpperCase();
}

export function bytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

/** The vault's assessment kinds, as human labels. */
export const KIND_LABEL = {
  ps: 'Problem Set', lab: 'Lab', quiz: 'Quiz', midterm: 'Midterm',
  final: 'Final Exam', project: 'Project', paper: 'Paper', prep: 'Prep',
  peer: 'Peer Review', participation: 'Participation',
  presentation: 'Presentation', other: 'Assessment',
};

export const kindLabel = (k) => KIND_LABEL[k] || 'Assessment';

/**
 * The local calendar date as YYYY-MM-DD.
 *
 * Deliberately not `toISOString().slice(0,10)`: that converts to UTC first, so
 * anyone west of Greenwich would see "today" flip a day early in the evening.
 * The timetable is driven by the student's own clock, so it must use local
 * date parts.
 */
export function todayIso(date = new Date()) {
  const p = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${p(date.getMonth() + 1)}-${p(date.getDate())}`;
}

export function addDays(iso, days) {
  const [y, m, d] = iso.split('-').map(Number);
  const dt = new Date(y, m - 1, d);
  dt.setDate(dt.getDate() + days);
  return todayIso(dt);
}

/** Monday of the week containing `iso`. */
export function startOfWeek(iso) {
  const [y, m, d] = iso.split('-').map(Number);
  const dt = new Date(y, m - 1, d);
  const shift = (dt.getDay() + 6) % 7;   // Sunday = 0 -> 6
  dt.setDate(dt.getDate() - shift);
  return todayIso(dt);
}

export function weekdayName(iso, short = false) {
  const [y, m, d] = iso.split('-').map(Number);
  const names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const n = names[new Date(y, m - 1, d).getDay()];
  return short ? n.slice(0, 3) : n;
}

/** "09:00" -> minutes since midnight, for ordering and "now" comparisons. */
export function minutesOf(hhmm) {
  if (!hhmm) return null;
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m;
}
