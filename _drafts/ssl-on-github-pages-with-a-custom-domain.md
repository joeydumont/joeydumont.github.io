---
layout: post
title: SSL on GitHub pages with a custom domain.
author: jayd
tags:
 - SSL
 - CloudFlare
 - GitHub Pages custom domains
---



<audio id="sound1" src="{{ site.url }}/assets/sounds/fish.mp3" preload="auto"></audio>
<audio id="sound2" src="{{ site.url }}/assets/sounds/sparta.wav" preload="auto"></audio>
<button class="btn" onclick="play_random_sound();">FRESH POT</button>

<script>
  function play_random_sound()
  {
    var textArray = [
          'sound1',
          'sound2'
          ]

    var randomElement = Math.floor(Math.random()*textArray.length)
    document.getElementById(textArray[randomElement]).play();
  }
</script>