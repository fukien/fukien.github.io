"""Build static blog pages from blog/posts.json. Run from any directory."""
import json
import html
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / 'blog'
esc = html.escape


def layout(title, body, prefix='../', description='Research notes on databases, systems, and the practice of research.'):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Wentao Huang</title><meta name="description" content="{esc(description, quote=True)}">
<link rel="icon" href="{prefix}assets/img/nus-favicon.jpg"><link rel="stylesheet" href="{prefix}assets/css/blog.css"></head>
<body><div class="blog-shell"><header class="blog-nav"><a class="brand" href="{prefix}index.html">Wentao Huang</a><nav aria-label="Main navigation"><a href="{prefix}index.html">Homepage</a><a href="{prefix}blog/" aria-current="{'page' if title == 'Blog' else 'false'}">Blog</a></nav></header>
{body}<footer>Wentao Huang · Research notes &amp; ideas <a href="{prefix}blog/">Blog archive ↑</a></footer></div></body></html>'''


def card(post, prefix=''):
    return f'''<article class="post-card"><div class="post-meta"><time datetime="{post['date']}">{post['date']}</time><span>{esc(post['topic'])}</span><span>Sample post</span></div><h2><a href="{prefix}{post['slug']}/">{esc(post['title'])}</a></h2><p>{esc(post['description'])}</p></article>'''


def build():
    posts = json.loads((BLOG / 'posts.json').read_text())
    posts.sort(key=lambda p: p['date'], reverse=True)
    assert len({p['slug'] for p in posts}) == len(posts)
    for post in posts:
        assert post['slug'] and all(c.isalnum() or c == '-' for c in post['slug'])
        folder = BLOG / post['slug']
        folder.mkdir(exist_ok=True)
        toc = ''.join(f'<li><a href="#section-{i}">{esc(s["heading"])}</a></li>' for i, s in enumerate(post['sections']))
        sections = ''.join(f'<section id="section-{i}"><h2>{esc(s["heading"])}</h2>' + ''.join(f'<p>{esc(p)}</p>' for p in s['paragraphs']) + '</section>' for i, s in enumerate(post['sections']))
        index = posts.index(post)
        adjacent = ''.join(f'<a href="../{posts[n]["slug"]}/">{label}<br><strong>{esc(posts[n]["title"])}</strong></a>' for n, label in [(index-1, '← Newer post'), (index+1, 'Older post →')] if 0 <= n < len(posts))
        body = f'''<main><a class="back-link" href="../">← All posts</a><div class="demo-note">Sample content · Generated to test the blog layout; this is not an actual article by Wentao Huang.</div><article class="reading"><div class="post-meta"><time datetime="{post['date']}">{post['date']}</time><a href="../?topic={post['topic'].replace(' ', '%20')}">{esc(post['topic'])}</a></div><h1>{esc(post['title'])}</h1><p class="lede">{esc(post['description'])}</p><aside class="toc"><strong>On this page</strong><ol>{toc}</ol></aside>{sections}</article><nav class="adjacent" aria-label="Adjacent posts">{adjacent}</nav></main>'''
        (folder / 'index.html').write_text(layout(post['title'], body, '../../', post['description']))
    topics = sorted({p['topic'] for p in posts})
    years = sorted({p['date'][:4] for p in posts}, reverse=True)
    options = lambda values: ''.join(f'<option>{esc(v)}</option>' for v in values)
    data = [{k: p[k] for k in ('slug', 'title', 'date', 'topic', 'description')} for p in posts]
    body = f'''<main><div class="eyebrow">NOTES FROM THE WORKBENCH</div><h1>Blog</h1><p class="lede">Exploring data systems, modern hardware, and the everyday work of research.</p><div class="demo-note">Demo archive · {len(posts)} generated sample posts for testing.</div>
<form id="filters" class="filters" role="search"><label class="search-label">Search posts<input id="search" type="search" placeholder="Search titles, topics, or descriptions…" autocomplete="off"></label><label>Topic<select id="topic"><option value="">All topics</option>{options(topics)}</select></label><label>Year<select id="year"><option value="">All years</option>{options(years)}</select></label><button type="reset" class="reset">Reset</button></form>
<div class="results-heading"><p id="result-count" role="status" aria-live="polite">{len(posts)} posts · newest first</p></div><div id="posts">{''.join(card(p) for p in posts)}</div><nav id="pagination" class="pager" aria-label="Blog pages"></nav><noscript><p>All posts are shown. Enable JavaScript to search and filter.</p></noscript></main>
<script id="post-data" type="application/json">{json.dumps(data).replace('<', chr(92)+'u003c')}</script><script src="../assets/js/blog.js"></script>'''
    (BLOG / 'index.html').write_text(layout('Blog', body))
    home = ROOT / 'index.html'
    source = home.read_text()
    start, end = '<!-- BLOG PREVIEW START -->', '<!-- BLOG PREVIEW END -->'
    preview = start + '''
<h2 class="accordion"><span onclick="expandAccordion(this)" style="cursor: pointer;" tabindex="0" role="button" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();expandAccordion(this)}">Blogs</span></h2>
<div class="panel overflow-hidden"><p>Research notes on data systems, modern hardware, and research.</p><p><small>Demo: generated sample posts for testing.</small></p>'''
    preview += ''.join(f'<p><small>{p["date"]} · {esc(p["topic"])}</small><br><a href="./blog/{p["slug"]}/">{esc(p["title"])}</a></p>' for p in posts[:3])
    preview += '<p><a href="./blog/">All ' + str(len(posts)) + ' posts →</a></p></div>\n' + end
    if start in source:
        before, rest = source.split(start, 1)
        _, after = rest.split(end, 1)
        home.write_text(before + preview + after)
    print(f'Built {len(posts)} post pages and blog archive; refreshed homepage preview.')


if __name__ == '__main__':
    build()
