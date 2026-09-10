#!/usr/bin/env python3
import json, os, urllib.request
from pathlib import Path
ORG=os.environ.get('ORG','BitHaven-Buffalo')
OUT=Path('.github/profile/assets/stats.svg')
def api(path):
    req=urllib.request.Request('https://api.github.com'+path,headers={'Accept':'application/vnd.github+json','User-Agent':'BitHaven-Profile','Authorization':f"Bearer {os.environ['GITHUB_TOKEN']}",'X-GitHub-Api-Version':'2022-11-28'})
    with urllib.request.urlopen(req,timeout=20) as r:return json.load(r)
repos=[]; page=1
while True:
    data=api(f'/orgs/{ORG}/repos?type=all&per_page=100&page={page}')
    if not data: break
    repos.extend(data)
    if len(data)<100: break
    page+=1
public=[r for r in repos if not r.get('private')]
stars=sum(r.get('stargazers_count',0) for r in public)
forks=sum(r.get('forks_count',0) for r in public)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 190" role="img" aria-label="Bit Haven GitHub statistics"><rect width="1000" height="190" rx="18" fill="#080b0c" stroke="#39f5d0" stroke-opacity=".22"/><text x="40" y="48" fill="#39f5d0" font-family="ui-monospace,monospace" font-size="15">BIT HAVEN // GITHUB STATUS</text><text x="40" y="104" fill="#f2f7f5" font-family="ui-monospace,monospace" font-size="30" font-weight="700">{len(public)}</text><text x="40" y="135" fill="#70807c" font-family="ui-monospace,monospace" font-size="13">PUBLIC REPOSITORIES</text><text x="340" y="104" fill="#f2f7f5" font-family="ui-monospace,monospace" font-size="30" font-weight="700">{stars}</text><text x="340" y="135" fill="#70807c" font-family="ui-monospace,monospace" font-size="13">TOTAL STARS</text><text x="640" y="104" fill="#f2f7f5" font-family="ui-monospace,monospace" font-size="30" font-weight="700">{forks}</text><text x="640" y="135" fill="#70807c" font-family="ui-monospace,monospace" font-size="13">TOTAL FORKS</text><text x="40" y="166" fill="#4e5d59" font-family="ui-monospace,monospace" font-size="11">AUTOMATICALLY UPDATED BY GITHUB ACTIONS · {ORG}</text></svg>'''
OUT.write_text(svg,encoding='utf-8')
