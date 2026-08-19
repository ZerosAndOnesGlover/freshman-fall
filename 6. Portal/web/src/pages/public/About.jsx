import { Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Crumbs } from '../../components/Chrome.jsx';

export default function About() {
  const { data: inst } = useApi(() => api.public.institution(), []);

  return (
    <>
      <div className="page-head-navy">
        <div className="wrap">
          <Crumbs items={[{ label: 'Home', to: '/' }, { label: 'About' }]} />
          <h1 style={{ marginTop: '1rem' }}>The Institute</h1>
          <p className="lede">
            A school built around one idea: that a computer science degree should leave
            you able to build things that work, and to explain why they work.
          </p>
        </div>
      </div>

      <div className="wrap section">
        <div className="grid grid-sidebar">
          <div className="prose">
            <p className="lede">
              The Institute of Science &amp; Technology teaches a single undergraduate
              programme — the B.Sc. in Computer Science &amp; Engineering — and teaches it
              in full public view.
            </p>
            <h2>Everything is published</h2>
            <p>
              Lecture notes, problem sets, lab handouts, rubrics and grading standards are
              all available here before, during and after the semester. A student who wants
              to read ahead can. A student who missed a lecture can catch up from the same
              notes the lecturer worked from.
            </p>
            <h2>Marks follow a stated rubric</h2>
            <p>
              Every course publishes its component weights up front — what fraction of the
              grade comes from problem sets, labs, midterms and the final. The portal
              computes a running grade from exactly those weights, using the same
              calculation the registry uses, so there are no surprises at the end of term.
            </p>
            <h2>Work is submitted, marked and returned in one place</h2>
            <p>
              Coursework goes through the portal. Feedback comes back attached to the
              submission it belongs to, next to the brief it was set against.
            </p>
          </div>

          <aside className="stack-lg">
            <div className="card card-pad">
              <span className="label">The programme</span>
              <p style={{ fontFamily: 'var(--serif)', fontSize: 'var(--t-md)' }}>
                B.Sc. Computer Science &amp; Engineering
              </p>
              <p className="small muted">Four years · eight semesters · 142 credits</p>
            </div>
            {inst && (
              <div className="card card-pad">
                <span className="label">Published so far</span>
                <table className="table table-plain">
                  <tbody>
                    <tr><td>Courses</td><td className="num tnum">{inst.stats.courses}</td></tr>
                    <tr><td>Lectures</td><td className="num tnum">{inst.stats.lectures}</td></tr>
                    <tr><td>Materials</td><td className="num tnum">{inst.stats.materials}</td></tr>
                    <tr><td>Faculty</td><td className="num tnum">{inst.stats.faculty}</td></tr>
                  </tbody>
                </table>
              </div>
            )}
            <div className="card card-pad">
              <span className="label">Read next</span>
              <ul className="footer-links" style={{ marginTop: '0.5rem' }}>
                <li><Link to="/page/university-policies">University policies</Link></li>
                <li><Link to="/page/grading-standards">Grading standards</Link></li>
                <li><Link to="/academics">Degree requirements</Link></li>
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </>
  );
}
