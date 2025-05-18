---
layout: page
title: About me
excerpt: "A somewhat intelligent person with limited social skills."
---

Hi! I am an HPC developer and systems administrator at the Governement of Canada. My background is in physics, specifically in modeling quantum electrodynamical effects in the presence of strong laser fields. See my [publications]({{ site.baseurl }}/articles) list for details.

I have authored and deployed high-performance computing scientific applications on multiple large computational clusters. I have mostly worked with MPI, but I have done some OpenMP as well. 

Most of the content on this site is on the  [blog]({{ site.baseurl }}/blog). The content is categorized, which should allow you to subscribe to only some of the topics I write on. Here's the list:

<ul>
{% for category in site.categories -%}
{% capture category_name %}{{ category | first }}{% endcapture -%}
    <li><a href="{{site.baseurl}}/{{category_name}}">{{category_name}}</a></li>
 {% endfor -%}
</ul>

