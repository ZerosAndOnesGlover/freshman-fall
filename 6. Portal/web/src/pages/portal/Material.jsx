import { useParams, Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { Markdown, useHeadings } from '../../markdown.jsx';

/** A lab sheet, handout, starter file or resource, read from the vault. */
export default function Material() {
  const { id } = useParams();
  const { data, loading, error, reload } = useApi(() => api.material(id), [id]);
  const headings = useHeadings(data?.body_md);

  if (loading) return <Loading />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  const isCode = data.ext && !['.md', '.markdown', '.txt'].includes(data.ext);
  const source = isCode
    ? `\`\`\`${(data.ext || '').replace('.', '')}\n${data.body_md}\n\`\`\``
    : data.body_md;

  return (
    <>
      <div className="page-head">
        <div className="wrap wrap-reader">
          <Crumbs items={[
            { label: 'Portal', to: '/portal' },
            { label: data.course_code, to: `/portal/courses/${data.course_id}` },
            { label: data.title },
          ]} />
          <div className="row-between row-wrap" style={{ marginTop: '0.75rem' }}>
            <div>
              <span className="eyebrow">{data.kind}</span>
              <h1 style={{ marginTop: '0.4rem' }}>{data.title}</h1>
              <p className="small mono muted" style={{ marginTop: '0.4rem' }}>{data.filename}</p>
            </div>
            <a className="btn btn-ghost" href={api.materialDownload(data.id)} download>
              Download
            </a>
          </div>
        </div>
      </div>

      <div className="wrap wrap-reader section">
        <div className="reader">
          <article>
            <Markdown source={source} dropFirstHeading={!isCode} links={data.links} />
          </article>
          {headings.length > 0 && (
            <aside className="toc">
              <h4>On this page</h4>
              {headings.map((h) => (
                <a key={h.id} href={`#${h.id}`} className={h.level === 3 ? 'lvl-3' : undefined}>{h.text}</a>
              ))}
            </aside>
          )}
        </div>
      </div>
    </>
  );
}
