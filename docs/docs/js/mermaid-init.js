// Initialize Mermaid on code blocks rendered by pymdownx.superfences
// This script finds <code class="language-mermaid"> elements and replaces
// them with <div class="mermaid"> so mermaid.js renders them.
document.addEventListener("DOMContentLoaded", function () {
  mermaid.initialize({startOnLoad: false, theme: "default"});

  document.querySelectorAll("code.language-mermaid").forEach(function (el) {
    const div = document.createElement("div");
    div.className = "mermaid";
    div.textContent = el.textContent;
    el.parentElement.replaceWith(div);
  });

  mermaid.run({querySelector: ".mermaid"});
});
