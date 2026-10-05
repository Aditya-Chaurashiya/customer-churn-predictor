import { useState, useEffect, useCallback } from 'react';

export function useApi<T>(apiFunc: (...args: any[]) => Promise<T>, ...args: any[]) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);
  const [responseTime, setResponseTime] = useState<number | null>(null);

  const execute = useCallback(async () => {
    setLoading(true);
    setError(null);
    const start = performance.now();
    try {
      const result = await apiFunc(...args);
      setData(result);
    } catch (err: any) {
      setError(err);
    } finally {
      const end = performance.now();
      setResponseTime(end - start);
      setLoading(false);
    }
  }, [apiFunc, ...args]);

  useEffect(() => {
    execute();
  }, [execute]);

  return { data, loading, error, execute, responseTime };
}
