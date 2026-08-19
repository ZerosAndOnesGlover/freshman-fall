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
