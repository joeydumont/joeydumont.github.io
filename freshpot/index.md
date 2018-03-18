---
layout: minimal
title: FRESH POOOOTS
excerpt: FRESH POTS
---

<audio id="fp1" src="{{ site.url }}/assets/sounds/freshpots1.ogg" preload="auto"></audio>
<audio id="fp2" src="{{ site.url }}/assets/sounds/freshpots2.ogg" preload="auto"></audio>
<audio id="fp3" src="{{ site.url }}/assets/sounds/freshpots3.ogg" preload="auto"></audio>
<audio id="fp4" src="{{ site.url }}/assets/sounds/freshpots4.ogg" preload="auto"></audio>
<audio id="fp5" src="{{ site.url }}/assets/sounds/freshpots5.ogg" preload="auto"></audio>
<audio id="fp6" src="{{ site.url }}/assets/sounds/freshpots6.ogg" preload="auto"></audio>
<audio id="fp7" src="{{ site.url }}/assets/sounds/freshpots7.ogg" preload="auto"></audio>
<p style="text-align: center;"><button class="btn" onclick="play_random_sound();">JUSTIN, FRESH POT!!!</button></p>

<iframe width="560" height="315" src="http://www.youtube.com/embed/fhdCslFcKFU" frameborder="0"> </iframe>

<script>
  function play_random_sound()
  {
    var textArray = [
          'fp1',
          'fp2',
          'fp3',
          'fp4',
          'fp5',
          'fp6',
          'fp7'
          ]

    var randomElement = Math.floor(Math.random()*textArray.length)
    document.getElementById(textArray[randomElement]).play();
  }
</script>