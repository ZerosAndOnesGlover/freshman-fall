/**
 * Thin fetch wrapper. Every call is same-origin (Vite proxies /api in dev), so
 * the session cookie rides along without any token juggling in the client.
 */
const BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(BASE + path, {
    credentials: 'same-origin',
    ...options,
    headers: options.body instanceof FormData
      ? options.headers
      : { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });

  const type = res.headers.get('content-type') || '';
  const payload = type.includes('application/json') ? await res.json() : await res.text();

  if (!res.ok) {
    const err = new Error(payload?.error || `Request failed (${res.status})`);
    err.status = res.status;
    err.payload = payload;
    throw err;
  }
  return payload;
}

const get = (p) => request(p);
const post = (p, body) => request(p, { method: 'POST', body: JSON.stringify(body ?? {}) });
const put = (p, body) => request(p, { method: 'PUT', body: JSON.stringify(body ?? {}) });
const del = (p) => request(p, { method: 'DELETE' });

export const api = {
  health: () => get('/health'),

  auth: {
    me: () => get('/auth/me'),
    login: (email, password) => post('/auth/login', { email, password }),
    logout: () => post('/auth/logout'),
  },

  public: {
    institution: () => get('/public/institution'),
    pages: () => get('/public/pages'),
    page: (slug) => get(`/public/pages/${slug}`),
    catalog: () => get('/public/catalog'),
    calendar: (q = '') => get(`/public/calendar${q}`),
    announcements: () => get('/public/announcements'),
    faculty: () => get('/public/faculty'),
    gradeScale: () => get('/public/grade-scale'),
  },

  dashboard: () => get('/dashboard'),

  courses: {
    mine: () => get('/courses/mine'),
    one: (id) => get(`/courses/${id}`),
    week: (id, num) => get(`/courses/${id}/weeks/${num}`),
  },

  lecture: (id) => get(`/lectures/${id}`),
  material: (id) => get(`/materials/${id}`),
  materialDownload: (id) => `${BASE}/materials/${id}?download=1`,

  assessments: {
    upcoming: (days) => get(`/assessments/upcoming${days ? `?days=${days}` : ''}`),
    outstanding: () => get('/assessments/outstanding'),
    forCourse: (courseId) => get(`/assessments/course/${courseId}`),
    one: (id) => get(`/assessments/${id}`),
    saveDraft: (id, body) => put(`/assessments/${id}/submission`, body),
    submit: (id, body) => post(`/assessments/${id}/submit`, body),
    unsubmit: (id) => post(`/assessments/${id}/unsubmit`),
    uploadFiles: (id, files) => {
      const fd = new FormData();
      for (const f of files) fd.append('files', f);
      return request(`/assessments/${id}/files`, { method: 'POST', body: fd });
    },
    deleteFile: (fileId) => del(`/assessments/files/${fileId}`),
    fileUrl: (fileId) => `${BASE}/assessments/files/${fileId}`,
  },

  grades: {
    summary: () => get('/grades/summary'),
    transcript: () => get('/grades/transcript'),
    course: (courseId, studentId) =>
      get(`/grades/course/${courseId}${studentId ? `?student=${studentId}` : ''}`),
  },

  instructor: {
    courses: () => get('/instructor/courses'),
    queue: () => get('/instructor/queue'),
    submissions: (assessmentId) => get(`/instructor/assessments/${assessmentId}/submissions`),
    grade: (assessmentId, body) => post(`/instructor/assessments/${assessmentId}/grade`, body),
    announce: (courseId, body) => post(`/instructor/courses/${courseId}/announcements`, body),
  },
};
