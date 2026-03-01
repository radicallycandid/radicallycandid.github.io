---
title: "TODO: título"
date: 2026-03-01
excerpt: TODO
---

TODO: conteúdo do post

<div class="graph-embed">
  <iframe src="/static/embeds/professions-graph-pt.html?embed" title="Grafo de adjacência de profissões"></iframe>
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

TODO: continuação do post
