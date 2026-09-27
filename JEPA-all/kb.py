#!/usr/bin/env python3
"""Offline maintenance for JEPA Atlas. Standard library only; never fetches sources."""
from __future__ import annotations
import argparse
import copy
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'knowledge.json'

def load(path: Path = DATA) -> dict:
    with path.open(encoding='utf-8') as handle:
        return json.load(handle)

def validate(kb: dict) -> None:
    """Check identity, required evidence context and graph referential integrity."""
    errors: list[str] = []
    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)
    require(kb.get('schema_version') == '1.0', 'Unsupported schema_version')
    for k in ('title', 'review_date', 'scope', 'evidence_policy'):
        require(isinstance(kb.get(k), str) and bool(kb[k].strip()), f'Missing metadata: {k}')
    for k in ('papers', 'concepts', 'paths', 'relations'):
        require(isinstance(kb.get(k), list), f'{k} must be a list')
    if errors:
        raise ValueError('\n'.join(errors))
    ids = [p.get('id') for p in kb['papers']]
    cids = [c.get('id') for c in kb['concepts']]
    require(bool(ids), 'No paper records')
    require(len(set(ids)) == len(ids), 'Duplicate paper ID')
    require(len(set(cids)) == len(cids), 'Duplicate concept ID')
    fields = ('name', 'title', 'group', 'problem', 'intuition', 'mechanism', 'objective', 'training', 'deployment', 'experiment')
    for p in kb['papers']:
        pid = p.get('id', '<missing>')
        require(isinstance(pid,str) and bool(re.fullmatch(r'\d{4}\.\d{4,5}',pid)), f'Invalid arXiv ID: {pid}')
        for k in fields:
            require(isinstance(p.get(k), str) and bool(p[k].strip()), f'{pid}: empty {k}')
        for k in ('aliases', 'concepts', 'limitations', 'results'):
            require(isinstance(p.get(k), list), f'{pid}: {k} must be a list')
        require(p.get('review') in ('sections_checked', 'abstract_only'), f'{pid}: invalid review level')
        src = p.get('source', {})
        url = urlparse(src.get('url', ''))
        version = src.get('version', '')
        require(bool(re.fullmatch(r'v\d+',version)), f'{pid}: pin a source version')
        require(url.scheme == 'https' and url.netloc == 'arxiv.org' and url.path in (f'/html/{pid}{version}',f'/abs/{pid}{version}'), f'{pid}: source URL must match its pinned arXiv ID/version')
        require(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', src.get('checked',''))), f'{pid}: invalid checked date')
        require(bool(src.get('locators')), f'{pid}: missing source locators')
        for cid in p.get('concepts', []):
            require(cid in cids, f'{pid}: unknown concept {cid}')
        require(bool(p.get('limitations')), f'{pid}: missing limitations')
        require(bool(p.get('results')), f'{pid}: include a result or an explicit unextracted record')
        for r in p.get('results', []):
            for k in ('task', 'metric', 'unit', 'protocol', 'locator'):
                require(isinstance(r.get(k),str) and bool(r[k].strip()),f'{pid}: result missing {k}')
            require('value' in r, f'{pid}: missing result value; use null when unextracted')
            require('uncertainty' in r, f'{pid}: uncertainty must be explicit, including null')
            require(r.get('direction') in ('higher','lower','descriptive'), f'{pid}: invalid metric direction')
            if r.get('value') is None:
                require(bool(r.get('note')), f'{pid}: explain why a result was not extracted')
            if r.get('baseline') is not None:
                require(r.get('baseline_value') is not None, f'{pid}: missing comparator value')
    for c in kb['concepts']:
        for k in ('id','name','question','plain','technical','caution'):
            require(bool(c.get(k)),f'Concept {c.get("id")}: missing {k}')
        for pid in c.get('papers',[]):
            require(pid in ids,f'Concept {c.get("id")}: unknown paper {pid}')
    for path in kb['paths']:
        for step in path.get('steps',[]):
            require(len(step)==2 and step[0] in ids and bool(step[1]), f'Invalid step in {path.get("id")}')
    for r in kb['relations']:
        require(r.get('source') in ids and r.get('target') in ids,'Relation points to missing paper')
        require(r.get('kind') in ('documented_comparison','curator_comparison','curator_tension'),'Invalid relation kind')
        require(bool(r.get('why')),'Relation missing rationale')
        if r.get('kind')=='documented_comparison':
            require(bool(r.get('source_url')) and bool(r.get('locator')),'Documented relation requires a source and locator')
    if errors:
        raise ValueError('\n'.join(errors))

def value(v: object) -> str:
    return '–'.join(map(str,v)) if isinstance(v,list) else ('Not extracted' if v is None else str(v))

def markdown(p: dict) -> str:
    source=p['source']
    parts=[f"# {p['name']}",p['title'],f"arXiv:{p['id']} · {source['version']} · {p['review']} · checked {source['checked']}",f"Primary source: {source['url']}\nSource locators: {'; '.join(source['locators'])}"]
    for title,key in [('Problem','problem'),('Intuition','intuition'),('Mechanism','mechanism'),('Objective / pipeline','objective'),('Training','training'),('Deployment','deployment')]:
        parts.append(f"## {title}\n{p[key]}")
    parts.append('Equations use normalized notation; consult the primary source for exact definitions.')
    parts.append('## Author-reported evidence')
    for r in p['results']:
        comparator=f"; comparator {r['baseline']}: {value(r['baseline_value'])}" if r['baseline'] is not None else ''
        parts.append(f"### {r['task']}\n{r['metric']}: {value(r['value'])} {r['unit']}{comparator}.\n\nProtocol: {r['protocol']}\n\nUncertainty: {r['uncertainty'] or 'Not extracted; do not infer significance.'}\n\n{r.get('note','')}\n\nEvidence: {source['url']} — {r['locator']}")
    parts.extend(['## Limitations\n'+'\n'.join('- '+s for s in p['limitations']),f"## Next experiment — curator proposal\n{p['experiment']}",'## Concepts\n'+', '.join(p['concepts'])])
    if p.get('audit'):
        parts.append('## Curation audit\n'+p['audit'])
    return '\n\n'.join(parts)+'\n'

def export(kb: dict) -> None:
    out=ROOT/'generated'
    (out/'papers').mkdir(parents=True,exist_ok=True)
    for p in kb['papers']:
        (out/'papers'/f"{p['id']}.md").write_text(markdown(p),encoding='utf-8')
    (out/'papers.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in kb['papers']),encoding='utf-8')
    text=f"# JEPA Atlas — compiled technical review\n\nReview snapshot: {kb['review_date']}\n\n{kb['scope']}\n\n{kb['evidence_policy']}\n\n"
    text+='\n---\n\n'.join(markdown(p) for p in kb['papers'])
    (ROOT/'COMPILATION.md').write_text(text,encoding='utf-8')
    print(f"Exported {len(kb['papers'])} paper records and COMPILATION.md")

def offline(kb: dict) -> None:
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    css=(ROOT/'style.css').read_text(encoding='utf-8')
    js=(ROOT/'app.js').read_text(encoding='utf-8')
    payload=json.dumps(kb,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    html=html.replace('<link rel="stylesheet" href="style.css">',f'<style>{css}</style>')
    html=html.replace('<script defer src="app.js"></script>',f'<script>window.ATLAS_DATA={payload};</script>')
    html=html.replace('</body>',f'<script>{js}</script></body>')
    (ROOT/'JEPA-Atlas-offline.html').write_text(html,encoding='utf-8')
    print('Built JEPA-Atlas-offline.html; core viewer works without network access')

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='command',required=True)
    subs.add_parser('validate');subs.add_parser('export');subs.add_parser('offline')
    search=subs.add_parser('search');search.add_argument('query')
    show=subs.add_parser('show');show.add_argument('id')
    add=subs.add_parser('add');add.add_argument('file',type=Path)
    args=parser.parse_args()
    try:
        kb=load();validate(kb)
        if args.command=='validate':
            print(f"Valid: {len(kb['papers'])} papers, {len(kb['concepts'])} concepts, {sum(len(p['results']) for p in kb['papers'])} results")
        elif args.command=='export':export(kb)
        elif args.command=='offline':offline(kb)
        elif args.command=='search':
            matches=[p for p in kb['papers'] if args.query.casefold() in json.dumps(p,ensure_ascii=False).casefold()]
            for p in matches: print(f"{p['id']} | {p['name']} | {p['problem']}")
            print(f'{len(matches)} matches',file=sys.stderr)
        elif args.command=='show':
            matches=[p for p in kb['papers'] if p['id']==args.id]
            if not matches:raise ValueError(f'Unknown paper ID {args.id}')
            print(markdown(matches[0]))
        elif args.command=='add':
            candidate=load(args.file);updated=copy.deepcopy(kb);updated['papers'].append(candidate);validate(updated)
            tmp=DATA.with_suffix('.json.tmp');tmp.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(DATA)
            print(f"Added {candidate['id']}; review the public diff and regenerate exports")
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
