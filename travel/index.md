---
layout: minimal
title: Travel Map
excerpt: Travel Map
---

This page contains a zoomable map of the places we have visited. Rather than marking countries visited, I have used the world map of all first-level administrative divisions. In Canada, that would be provinces and territories, and states in the US.



<div style="width: 1200px; padding: 0; margin: 0px -300px auto;">
<embed type="image/svg+xml" src="{{ '/assets/images/travel-map.svg' | absolute_url }}" id="travel-map">


<script src="{{ '/assets/js/svg-pan-zoom.js' | absolute_url }}"></script>

<script>
document.getElementById('travel-map').addEventListener('load', function(){
  // Will get called after embed element was loaded
  svgPanZoom(document.getElementById('travel-map'), {
    zoomEnabled: true,
    controlIconsEnabled: true
  });
  })
</script>
</div>
