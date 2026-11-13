// The theme switch and the menu on small screens. No library, on purpose.
(function () {
  "use strict";

  var root = document.documentElement;

  function showTheme() {
    var dark = root.classList.contains("dark");
    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(dark));
      var label = button.querySelector("[data-theme-label]");
      if (label) {
        label.textContent = dark ? "Light mode" : "Dark mode";
      }
    });
  }

  document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      var dark = root.classList.toggle("dark");
      try {
        window.localStorage.setItem("theme", dark ? "dark" : "light");
      } catch (error) {
        // Storage is closed. The choice holds for this page and the next one follows the system.
      }
      showTheme();
    });
  });

  document.querySelectorAll("[data-menu-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      var sidebar = document.querySelector("[data-sidebar]");
      var open = !sidebar.classList.toggle("-translate-x-full");
      document.querySelectorAll("[data-menu-toggle][aria-expanded]").forEach(function (toggle) {
        toggle.setAttribute("aria-expanded", String(open));
      });
    });
  });

  showTheme();
})();
