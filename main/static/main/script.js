document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const themeSwitch = document.getElementById("theme-switch");

  if (!themeSwitch) {
    return;
  }

  const toggleText = document.querySelector(".toggle-text");
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  function applyTheme(theme) {
    const isDark = theme === "dark";
    root.setAttribute("data-theme", theme);
    themeSwitch.checked = isDark;
    themeSwitch.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");

    if (toggleText) {
      toggleText.textContent = isDark ? "Dark" : "Light";
    }
  }

  applyTheme(savedTheme || (prefersDark ? "dark" : "light"));

  themeSwitch.addEventListener("change", () => {
    const nextTheme = themeSwitch.checked ? "dark" : "light";
    localStorage.setItem("theme", nextTheme);
    applyTheme(nextTheme);
  });
});
