import { useParams, Link } from 'react-router-dom';
import { api } from '../../api.js';
import { useApi } from '../../useApi.js';
import { Loading, ErrorNote, Crumbs } from '../../components/Chrome.jsx';
import { Markdown, renderMarkdown } from '../../markdown.jsx';

/** Renders an institution document (policies, degree requirements) from the vault. */
export default function DocPage({ slug: fixedSlug }) {
  const params = useParams();
  const slug = fixedSlug || params.slug;
  const { data, loading, error, reload } = useApi(() => api.public.page(slug), [slug]);
  const { data: pages } = useApi(() => api.public.pages(), []);

  if (loading) return <Loading />;
  if (error) return <div className="wrap section"><ErrorNote error={error} onRetry={reload} /></div>;

  const headings = renderMarkdown(data.body_md).headings.filter((h) => h.level === 2);

  return (
    <>
      <div className="page-head">
        <div className="wrap">
          <Crumbs items={[{ label: 'Home', to: '/' }, { label: data.title }]} />
          <h1>{data.title}</h1>
          {data.summary && <p className="lede">{data.summary}</p>}
        </div>
      </div>

      <div className="wrap section">
        <div className="reader">
          <article>
            <Markdown source={data.body_md} dropFirstHeading />
          </article>
          <aside className="toc">
            {headings.length > 0 && (
              <>
                <h4>On this page</h4>
                {headings.map((h) => (
                  <a key={h.id} href={`#${h.id}`}>{h.text}</a>
                ))}
              </>
            )}
            {pages && pages.length > 1 && (
              <>
                <h4 style={{ marginTop: '2rem' }}>Other documents</h4>
                {pages.filter((p) => p.slug !== slug).map((p) => (
                  <Link key={p.slug} to={`/page/${p.slug}`}>{p.title}</Link>
                ))}
              </>
            )}
          </aside>
        </div>
      </div>
    </>
  );
}
