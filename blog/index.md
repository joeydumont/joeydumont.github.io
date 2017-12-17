---
layout: page
title: Blog
excerpt: "An archive of blog posts sorted by date."
search_omit: true
---

Here you will find ramblings on technology, science, math and pretty much anything
that comes to mind. The only saving grace for this chaotic mess is that I tend
to use tags to salvage a little organization out of this.

<ul class="post-list">
{% for post in site.posts %}
  <li><article><a href="{{ site.url }}{{ post.url }}">{{ post.title }} <span class="entry-date"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time></span></a></article></li>
{% endfor %}
</ul>
