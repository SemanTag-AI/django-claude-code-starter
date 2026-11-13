// The theme switch and the menus on small screens. No library, on purpose.
(function () {
  "use strict";

  var root = document.documentElement;

  function showTheme() {
    var dark = root.classList.contains("dark");
    // The name of the switch stays "Dark mode". Only its pressed state changes, so that a
    // screen reader never has to announce "Light mode, pressed".
    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(dark));
      var state = button.querySelector("[data-theme-state]");
      if (state) {
        state.textContent = dark ? "On" : "Off";
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
  function opener(menu) {
    return document.querySelector('[data-menu-toggle][aria-expanded][aria-controls="' + menu.id + '"]');
  }

  // Closing always hands the focus back to the button that opens the menu. Otherwise the
  // focus would stay on something that has just gone out of sight.
  function setOpen(menu, open) {
    menu.toggleAttribute("data-open", open);
    var button = opener(menu);
    if (button) {
      button.setAttribute("aria-expanded", String(open));
      if (!open) {
        button.focus();
      }
    }
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
    });
  });

  showTheme();
})();
