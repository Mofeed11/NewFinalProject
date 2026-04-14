export default function Panel({ title, subtitle, children }) {
  return (
    <section className="panel">
      <header className="panel-header">
        <h2>{title}</h2>
        {subtitle ? <p>{subtitle}</p> : null}
      </header>
      <div className="panel-body">{children}</div>
    </section>
  );
}
