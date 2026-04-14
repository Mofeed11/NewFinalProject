import { useEffect, useRef } from "react";

export default function usePolling(fn, intervalMs, deps = []) {
  const savedFn = useRef(fn);

  useEffect(() => {
    savedFn.current = fn;
  }, [fn]);

  useEffect(() => {
    let cancelled = false;

    const run = async () => {
      if (cancelled) return;
      await savedFn.current();
    };

    run();
    const id = setInterval(run, intervalMs);

    return () => {
      cancelled = true;
      clearInterval(id);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [intervalMs, ...deps]);
}
