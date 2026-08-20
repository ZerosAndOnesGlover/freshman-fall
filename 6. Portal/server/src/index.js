/**
 * Institute of Science & Technology — portal API.
 *
 * The database is rebuilt from the vault by `npm run import`; this server only
 * reads it, plus the submissions and grades it writes itself. It never writes
 * to the vault markdown.
 */
import express from 'express';
import cookieParser from 'cookie-parser';
import { db } from './db.js';
import { attachUser, purgeExpiredSessions } from './auth.js';
import { VAULT_ROOT, DB_PATH } from './paths.js';

import authRoutes from './routes/auth.js';
import publicRoutes from './routes/public.js';
import courseRoutes, { lectureRouter, materialRouter } from './routes/courses.js';
import assessmentRoutes from './routes/assessments.js';
import gradeRoutes from './routes/grades.js';
import instructorRoutes from './routes/instructor.js';
import adminRoutes from './routes/admin.js';
import dashboardRoutes from './routes/dashboard.js';
import timetableRoutes from './routes/timetable.js';

const PORT = Number(process.env.PORT) || 4000;
const app = express();

app.set('trust proxy', 1);
app.use(express.json({ limit: '2mb' }));
app.use(cookieParser());
app.use(attachUser);

app.get('/api/health', (_req, res) => {
  res.json({
    ok: true,
    courses: db.prepare('SELECT COUNT(*) AS n FROM courses').get().n,
    lectures: db.prepare('SELECT COUNT(*) AS n FROM lectures').get().n,
    vault: VAULT_ROOT,
  });
});

app.use('/api/auth', authRoutes);
app.use('/api/public', publicRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/timetable', timetableRoutes);
app.use('/api/courses', courseRoutes);
app.use('/api/lectures', lectureRouter);
app.use('/api/materials', materialRouter);
app.use('/api/assessments', assessmentRoutes);
app.use('/api/grades', gradeRoutes);
app.use('/api/instructor', instructorRoutes);
app.use('/api/admin', adminRoutes);

app.use('/api', (_req, res) => res.status(404).json({ error: 'No such endpoint' }));

// Multer and better-sqlite3 both throw synchronously; without this the client
// gets an HTML stack trace instead of JSON it can render.
app.use((err, _req, res, _next) => {
  if (err?.code === 'LIMIT_FILE_SIZE') return res.status(413).json({ error: 'That file is larger than 25 MB' });
  console.error(err);
  res.status(500).json({ error: 'Something went wrong on the server' });
});

purgeExpiredSessions();
setInterval(purgeExpiredSessions, 6 * 3600 * 1000).unref();

app.listen(PORT, () => {
  console.log(`  IST portal API  http://localhost:${PORT}`);
  console.log(`  database        ${DB_PATH}`);
  console.log(`  vault           ${VAULT_ROOT}`);
});
