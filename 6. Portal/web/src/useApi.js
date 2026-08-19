import { useEffect, useState, useCallback, useRef } from 'react';

/**
 * Runs an async loader and tracks its state. `deps` behaves like useEffect's.
 * A stale response from a superseded call is discarded rather than rendered.
 */
export function useApi(loader, deps = []) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const runId = useRef(0);

  const reload = useCallback(() => {
    const id = ++runId.current;
    setLoading(true);
    Promise.resolve()
      .then(loader)
      .then((d) => { if (id === runId.current) { setData(d); setError(null); } })
      .catch((e) => { if (id === runId.current) { setError(e); setData(null); } })
      .finally(() => { if (id === runId.current) setLoading(false); });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => { reload(); }, [reload]);

  return { data, error, loading, reload, setData };
}
