#!/usr/bin/env python3
"""Build provider-neutral model input from local files or authorized GitHub raw content."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def read(path, repo=None, ref='main'):
    if not repo:
        return (ROOT / path).read_text(encoding='utf-8')
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid owner/repository.')
    url = f'https://api.github.com/repos/{repo}/contents/{quote(path, safe="/")}?ref={quote(ref, safe="")}'
    headers = {'Accept': 'application/vnd.github.raw+json', 'User-Agent': 'ENS202-context-loader'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return response.read().decode('utf-8')


def tokens(text):
    text = text.lower().translate(str.maketrans('çğıöşü', 'cgiosu'))
    aliases = {'r-134a':'r134a', 'sogut':'cool', 'buhar':'vapor', 'su':'water', 'hava':'air', 'elektrik':'electrical', 'basinc':'pressure', 'hacim':'volume', 'durdurucu':'stops', 'yay':'spring', 'isit':'heat', 'tablo':'table', 'karisim':'mixture', 'sicaklik':'temperature'}
    for a, b in aliases.items():
        text = re.sub(r'\b'+re.escape(a)+r'\b', b, text)
    return set(re.findall(r'[a-z0-9]+', text)) - {'the','a','an','and','of','to','in','at','is','for','with','determine','find','q','kg','kpa','c','m','degc'}


def build(args):
    load = lambda path: read(path, args.repo, args.ref)
    examples = json.loads(load('data/past_exams.json'))['questions']
    states = json.loads(load('tables/verified_states.json'))
    source = json.loads(load('tables/source.json'))
    qtokens = tokens(args.question)
    ranked = sorted(examples, key=lambda x: len(qtokens & tokens(json.dumps(x))), reverse=True)
    if args.example:
        selected = [q for q in examples if q['id'] in args.example]
        if len(selected) != len(set(args.example)):
            raise ValueError('Unknown example ID.')
    else:
        selected = [q for q in ranked if qtokens & tokens(json.dumps(q))][:3]
    guide = load('course_reference.md')
    sections = re.split(r'(?=^## )', guide, flags=re.M)
    methods = sorted(sections, key=lambda s: len(qtokens & tokens(s)), reverse=True)
    selected_methods = [s for s in methods if qtokens & tokens(s)][:2]
    ids = {state for q in selected for state in q.get('verified_state_ids', [])}
    tables = set(args.table or []) | {t for q in selected for t in q.get('tables', [])}
    unknown = tables - set(source['table_pages'])
    if unknown:
        raise ValueError('Unknown table IDs: '+', '.join(sorted(unknown)))
    facts = [s for s in states['states'] if s['id'] in ids or (args.table and s['table'] in args.table)]
    return {
        'system_prompt': load('system_prompt.txt'),
        'question': args.question,
        'course_context': {
            'examples': selected,
            'methods': selected_methods,
            'verified_cengel_states': facts,
            'property_coverage': states['coverage'],
            'table_source': source,
            'required_table_pages': {t: source['table_pages'][t] for t in sorted(tables)},
            'retrieval_note': 'Simple lexical selection, not semantic search. Verify relevance. Original table URLs are provenance, not proof the model has read those pages. Use scripts/fetch_cengel.py to retrieve/render missing properties and attach the actual pages through your model provider.'
        }
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--question', required=True)
    p.add_argument('--repo', help='owner/repository; omitted means local files')
    p.add_argument('--ref', default='main', help='branch, tag or commit SHA')
    p.add_argument('--example', action='append', help='exact example ID; repeatable')
    p.add_argument('--table', action='append', help='e.g. A-13; repeatable')
    args = p.parse_args()
    try:
        print(json.dumps(build(args), ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f'Context build failed ({type(exc).__name__}): {exc}', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
