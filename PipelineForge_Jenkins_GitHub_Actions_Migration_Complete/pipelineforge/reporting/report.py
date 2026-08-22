from pathlib import Path
import csv, json, html

def write_reports(items, summary, outdir):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    (out/'migration_assessment.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
    fields=['jenkins_job','full_name','scm_url','migration_classification','migration_score','migration_readiness','wave','sprint','strategy']
    with (out/'migration_assessment.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); wr.writeheader(); wr.writerows(items)
    counts={k:sum(1 for x in items if x.get('migration_classification')==k) for k in ('SIMPLE','MEDIUM','COMPLEX')}
    rows=''.join(f"<tr><td>{html.escape(str(x.get('jenkins_job') or x.get('full_name')))}</td><td>{x.get('migration_classification')}</td><td>{x.get('wave','')}</td><td>{x.get('sprint','')}</td><td>{html.escape(x.get('strategy',''))}</td></tr>" for x in items)
    page=f"""<!doctype html><meta charset="utf-8"><title>PipelineForge Migration Dashboard</title><style>body{{font-family:Arial;margin:32px;max-width:1200px}}table{{border-collapse:collapse;width:100%}}th,td{{padding:8px;border:1px solid #ddd;text-align:left}}.kpi{{display:inline-block;padding:12px 18px;margin:5px;background:#f3f3f3;border-radius:8px}}</style><h1>Jenkins → GitHub Actions Migration Dashboard</h1><div class="kpi">Total: {len(items)}</div><div class="kpi">Simple: {counts['SIMPLE']}</div><div class="kpi">Medium: {counts['MEDIUM']}</div><div class="kpi">Complex: {counts['COMPLEX']}</div><div class="kpi">Sprints: {summary.get('sprints','')}</div><h2>Migration Plan</h2><table><tr><th>Pipeline</th><th>Complexity</th><th>Wave</th><th>Sprint</th><th>Strategy</th></tr>{rows}</table>"""
    (out/'dashboard.html').write_text(page,encoding='utf-8')
