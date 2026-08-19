import { Routes, Route, Navigate, useLocation, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth.jsx';
import { Masthead, Footer, Loading } from './components/Chrome.jsx';

import Home from './pages/public/Home.jsx';
import Catalog from './pages/public/Catalog.jsx';
import CoursePublic from './pages/public/CoursePublic.jsx';
import CalendarPage from './pages/public/Calendar.jsx';
import Faculty from './pages/public/Faculty.jsx';
import DocPage from './pages/public/DocPage.jsx';
import About from './pages/public/About.jsx';
import Login from './pages/Login.jsx';

import Dashboard from './pages/portal/Dashboard.jsx';
import MyCourses from './pages/portal/MyCourses.jsx';
import Course from './pages/portal/Course.jsx';
import Lecture from './pages/portal/Lecture.jsx';
import Material from './pages/portal/Material.jsx';
import Coursework from './pages/portal/Coursework.jsx';
import Assessment from './pages/portal/Assessment.jsx';
import Grades from './pages/portal/Grades.jsx';
import Transcript from './pages/portal/Transcript.jsx';
import Profile from './pages/portal/Profile.jsx';

import Teaching from './pages/instructor/Teaching.jsx';
import Marking from './pages/instructor/Marking.jsx';
import MarkAssessment from './pages/instructor/MarkAssessment.jsx';

/** Signed-in only. Sends you to the sign-in page and back again afterwards. */
function Protected() {
  const { user, ready } = useAuth();
  const loc = useLocation();
  if (!ready) return <Loading label="Checking your session" />;
  if (!user) return <Navigate to="/login" replace state={{ from: loc.pathname }} />;
  return <Outlet />;
}

function StaffOnly() {
  const { user, ready } = useAuth();
  if (!ready) return <Loading />;
  if (!user) return <Navigate to="/login" replace />;
  if (user.role === 'student') return <Navigate to="/portal" replace />;
  return <Outlet />;
}

function SiteLayout() {
  return (
    <div className="shell">
      <a href="#main" className="skip-link">Skip to content</a>
      <Masthead />
      <main id="main"><Outlet /></main>
      <Footer />
    </div>
  );
}

function NotFound() {
  return (
    <div className="wrap section" style={{ textAlign: 'center', padding: '6rem 0' }}>
      <span className="eyebrow">404</span>
      <h1 style={{ marginTop: '0.75rem' }}>That page is not here.</h1>
      <p className="lede" style={{ margin: '1rem auto 2rem', maxWidth: '40ch' }}>
        The link may be out of date, or the material may not have been published yet.
      </p>
      <a href="/" className="btn">Back to the Institute</a>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* The sign-in page has its own full-bleed layout. */}
        <Route path="/login" element={<Login />} />

        <Route element={<SiteLayout />}>
          {/* Public */}
          <Route index element={<Home />} />
          <Route path="courses" element={<Catalog />} />
          <Route path="courses/:id" element={<CoursePublic />} />
          <Route path="calendar" element={<CalendarPage />} />
          <Route path="faculty" element={<Faculty />} />
          <Route path="about" element={<About />} />
          <Route path="academics" element={<DocPage slug="degree-requirements" />} />
          <Route path="page/:slug" element={<DocPage />} />

          {/* Portal */}
          <Route path="portal" element={<Protected />}>
            <Route index element={<Dashboard />} />
            <Route path="courses" element={<MyCourses />} />
            <Route path="courses/:id" element={<Course />} />
            <Route path="lectures/:id" element={<Lecture />} />
            <Route path="materials/:id" element={<Material />} />
            <Route path="work" element={<Coursework />} />
            <Route path="work/:id" element={<Assessment />} />
            <Route path="grades" element={<Grades />} />
            <Route path="transcript" element={<Transcript />} />
            <Route path="profile" element={<Profile />} />

            <Route element={<StaffOnly />}>
              <Route path="teaching" element={<Teaching />} />
              <Route path="marking" element={<Marking />} />
              <Route path="marking/:id" element={<MarkAssessment />} />
            </Route>
          </Route>

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}
