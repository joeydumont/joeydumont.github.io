---
layout: minimal
title: Travel Map
excerpt: Travel Map
---

This page contains a zoomable map of the places we have visited. Rather than marking countries visited, I have used the world map of all first-level administrative divisions. In Canada, that would be provinces and territories, and states in the US.

<embed type="image/svg+xml" src="{{ site.url }}/assets/images/travel-map.svg" id="travel-map-2"/>

<script src="{{ site.url }}/assets/js/svg-pan-zoom.js"></script>

<script>
document.getElementById('travel-map-2').addEventListener('load', function(){
  // Will get called after embed element was loaded
  svgPanZoom(document.getElementById('travel-map-2'), {
    zoomEnabled: true,
    controlIconsEnabled: true
  });
  })
</script>
