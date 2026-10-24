# Blog

This demo contains 120 generated sample articles, clearly labeled on the homepage, archive, and individual pages. No fabricated experimental results are presented as real research.

## Editing

The source is `posts.json`: a list of posts with `slug`, `title`, ISO `date`, `topic`, `description`, and `sections`. Each section has a `heading` and a list of plain-text `paragraphs`. Slugs must be unique and contain only letters, digits, or hyphens; keep them stable after publishing.

After editing, run from the repository root:

```sh
python3 scripts/build_blog.py
```

The dependency-free builder generates the archive, individual HTML pages, and the three latest homepage links. Commit the generated files along with the source; GitHub Pages serves them directly. Search matches titles, topics, and descriptions. Topic/year filters and pagination can be shared using URL query parameters. All articles remain accessible without JavaScript.

To replace the demo with real posts, replace the JSON records, remove the demo notices in the builder, and remove obsolete generated post directories. Rebuilding does not delete existing directories, to avoid accidental content loss. This initial version uses structured plain text rather than Markdown, and does not yet include RSS or syntax highlighting.

Local preview: `python3 -m http.server 8000`, then visit `http://localhost:8000/blog/`.
