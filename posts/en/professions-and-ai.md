---
title: "TODO: title"
date: 2026-03-01
excerpt: TODO
draft: true
---

TODO: post content

<div class="graph-embed">
  <iframe src="/static/embeds/professions-graph-en.html?embed" title="Professions adjacency graph"></iframe>
</div>
<script>
// Sync theme changes with embedded graph
(function() {
  var iframe = document.querySelector('.graph-embed iframe');
  var observer = new MutationObserver(function() {
    var theme = document.documentElement.getAttribute('data-theme');
    if (iframe.contentWindow) {
      iframe.contentWindow.postMessage({ type: 'theme-change', theme: theme }, '*');
    }
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
</script>

TODO: post continuation
