// The theme switch and the menus on small screens. No library, on purpose.
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

  // A menu button names the element it opens in aria-controls. This script only sets
  // data-open on that element. What "open" looks like is up to the stylesheet.
  function setOpen(menu, open) {
    menu.toggleAttribute("data-open", open);
    document.querySelectorAll('[data-menu-toggle][aria-expanded][aria-controls="' + menu.id + '"]').forEach(function (button) {
      button.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll("[data-menu-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      var menu = document.getElementById(button.getAttribute("aria-controls"));
      setOpen(menu, !menu.hasAttribute("data-open"));
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") {
      return;
    }
    document.querySelectorAll("[data-open]").forEach(function (menu) {
      setOpen(menu, false);
      var opener = document.querySelector('[data-menu-toggle][aria-expanded][aria-controls="' + menu.id + '"]');
      if (opener) {
        opener.focus();
      }
    });
  });

  showTheme();
})();
