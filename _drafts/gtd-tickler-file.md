---
layout: post
title: "GTD: a tickler file in Obsidian and DataviewJS"
author: jayd
tags:
    - gtd
    - productivity
categories:
    - writing
---

<!-- Should be a short article talking about GTD, and how the tickler file is meant to remind you of things at specific dates. -->

I've recently read David Allen's [Getting Things Done](https://openlibrary.org/works/OL271504W/Getting_Things_Done?edition=ia:gettingthingsdon0000alle_g8s9) {%cite allenGettingThingsDone2015 --file tickler-file %}, more commonly known as GTD. I've taken to the approach, especially the concept of the next action list and the six level model for categorizing work. I've even [integrated](https://forum.obsidian.md/t/gtd-with-obsidian-a-ready-to-go-gtd-system-with-task-sequencing-quick-add-template-waiting-on-someday-maybe-and-more/65502) {% cite alangGTDObsidianReadytogo2023 --file tickler-file %} my next action list into Obsidian, after years of avoiding the latter for task tracking.

One other tool that Allen swears by in GTD is the tickler file, or suspense file {% cite corydoctorowKeepingSuspenseFile2024 --file tickler-file %}. It is nothing more than a technique to ensuring that you are reminded of tasks/projects/notes at a particular time. You could implement this with physical files and folders (see Fig.&nbsp;1 below for the GTD version), a To-do app that supports reminders, post-it notes, etc. I spend the majority of my time working in front my computer, and a lot of in Obsidian, so having my suspense right there is valuable.

I've written a short DataviewJS implementation of a tickler file that I use in my *Daily Note* template. Below, I go over the additional metadata that I put in the frontmatter of my notes, and show the JS implementation, as well as how it gets used in my templates.

<br/>

{:style="text-align:center;"}
<figure>
    <img src="{{ "assets/posts/tickler-file/physical-tickler.png" | absolute_url }}" width=600/>
    <figcaption><b>Figure 1</b>: Physical tickler file. Original in GTD.</figcaption>
</figure>

<br/>

## Implementation

I find it best to work through an example of what I want to achieve to understand the tickler file. I use `tickler` and `tickled` fields in my frontmatter to add reminders to my notes.
```yaml
---
tickler: [2025-09-11, 2026-03-01]
tickled: [2025-09-11]
---
```
In the example aboeve, I set a reminder for September 11th, and I have marked it as reviewed (through the `tickled` field) on the same date. I would then expect this note to only appear in my March 1st, 2026 daily note. If `tickled` had been empty, I would expect the note to appear in my daily note template starting from September 11th onwards (i.e. before March 1st, 2026).

My initial, simpler, query did not produce the expected behaviour:
```sql
TABLE aliases as Title, file.etags as Tags, tickler as Date
WHERE tickler AND max(tickler) <= date(2025-10-04) AND max(tickled) < max(tickler)
```
The use of `max` broke the ability to mark notes to be tickled at multiple future dates, as this query would only show the later date. I had to switch to a still simple DataviewJS implementation that allowed more complex logic around matching time periods. Here is the script in its entirety below:

```javascript
// Match up time periods for the tickler file and
// show items that haven't been tickled yet.
//
// My tickler notes have two properties set up:
//   - tickler: [YYYY-MM-DD, YYYY-MM-DD,...]
//   - tickled: [YYYY-MM-DD, ...]
//
// I want a note to appear in my tickler file whenever
// the current date is larger than the largest element
// in tickler smaller than the largest element in tickled.
// That will allow me to have multiple tickler
// dates in the future.
// @param { dv.page } page - page fed through a dv.page query.
// @param { string } date - date passed as YYYY-MM-DD string.
function tickler_file(page, date) {

  // Get date objects out of the given date, and the tickler object.
  const date_moment = new Date(date);
  const tickler_dates = (Array.isArray(page.tickler) ? page.tickler :
    [page.tickler]);

  // If it hasn't been tickled yet, find the minimum date
  // in the tickler array.
  if (!page.tickled) {
    // Find the min (ideally these should be sorted, but don't assume it)
    const min_tickler_date = tickler_dates.reduce((latest, current) =>
      latest < current ? latest : current);
    return min_tickler_date <= date_moment;
  }

  // If it has been tickled in the past, check whether
  // the next tickler date is the same or before
  // the current date.
  const tickled_dates = (Array.isArray(page.tickled) ? page.tickled :
    [page.tickled]);
  const latest_tickled = tickled_dates.reduce((a, b) => b > a ? b :
  a);
  const remaining_ticklers = tickler_dates.filter(d => d >
    latest_tickled);

  // If there are no remaining ticklers, we are done.
  if (remaining_ticklers.length === 0) return false;

  const next_tickler = remaining_ticklers.reduce((a, b) => a <= b ?
    a : b);

  return next_tickler <= date_moment;
}
exports.tickler_file = tickler_file;
```
The script assumes that the `tickler` field is populated. We do this in the query, although we should probably do it in both. We then check whether `tickled` is populated. If it not, we just need to check the minimal value of `tickler` against the current date.

If both fields are populated, we find the the latest date in `tickled`, and check whether there are any fields in `tickler` that are later than that. If there are, we check that against the current date. And that's about the size of it.

This function gets called in my *Daily note* template as:
```javascript
var utils = await dv.io.load("/Utils/dataviewjs_utils.js", "text");
eval(utils);
let pages = dv.pages().where(p => p.tickler).where(p => exports.tickler_file(p, "2025-11-10"));
dv.table(
  ["File", "Tags", "Date", "Date tickled"],
  pages.map(p => [p.file.link, p.file.etags, p.tickler, p.tickled])
);
```



<!-- Add examples of files in the tickler area in a rendered daily note. -->

## Like & subscribe

The easiest way to consume this site is through [RSS]({% link feed.xml %}). There are even feed categories for selected viewing: {% for category in site.feed.categories -%}
[{{ category }}]({% link feed/{{ category }}.xml %}){% unless forloop.last %},{% else %}.{% endunless %}
{% endfor -%}
I love RSS, and I think you [should](https://pluralistic.net/2024/10/16/keep-it-really-simple-stupid/) {% cite corydoctorowYouShouldBe2024 --file tickler-file %} too!

## Resources

{% bibliography --file tickler-file --cited_in_order %}
