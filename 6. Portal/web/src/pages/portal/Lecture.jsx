import { useParams, Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { Markdown, useHeadings } from '../../markdown.jsx';

export default function Lecture() {
  const { id } = useParams();
  const { data, loading, error, reload } = useApi(() => api.lecture(id), [id]);
  const headings = useHeadings(data?.body_md, data?.title);

  if (loading) return <Loading label="Loading lecture" />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  return (
    <>
      <div className="page-head">
        <div className="wrap wrap-reader">
          <Crumbs items={[
            { label: 'Portal', to: '/portal' },
            { label: data.course_code, to: `/portal/courses/${data.course_id}` },
            { label: data.week_num !== null ? `Week ${data.week_num}` : 'Lectures' },
          ]} />
          <span className="eyebrow" style={{ display: 'block', marginTop: '0.75rem' }}>
            {data.code ? `${data.code} · ` : ''}{data.course_code}
          </span>
          <h1 style={{ marginTop: '0.4rem' }}>{data.title}</h1>
          {data.subtitle && <p className="lede">{data.subtitle}</p>}
          {data.date_text && <p className="small muted" style={{ marginTop: '0.75rem' }}>{data.date_text}</p>}
        </div>
      </div>

      <div className="wrap wrap-reader section">
        <div className="reader">
          <article>
            <Markdown source={data.body_md} dropFirstHeading dropTitle={data.title} links={data.links} />

            <nav className="reader-nav">
              {data.prev ? (
                <Link to={`/portal/lectures/${data.prev.id}`}>
                  <div className="dir">← Previous</div>
                  <div className="ttl">{data.prev.title}</div>
                </Link>
              ) : <span />}
              {data.next && (
                <Link to={`/portal/lectures/${data.next.id}`} className="next">
                  <div className="dir">Next →</div>
                  <div className="ttl">{data.next.title}</div>
                </Link>
              )}
            </nav>
          </article>

          <aside className="toc">
            <h4>On this page</h4>
            {headings.map((h) => (
              <a key={h.id} href={`#${h.id}`} className={h.level === 3 ? 'lvl-3' : undefined}>{h.text}</a>
            ))}
            <p className="tiny muted" style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--rule)' }}>
              Rendered live from the course vault.
            </p>
          </aside>
        </div>
      </div>
    </>
  );
}
