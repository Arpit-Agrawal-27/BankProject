document.addEventListener("DOMContentLoaded", () => {
    const themeSwitch = document.getElementById("theme-switch")
    const toggleText = document.querySelector(".toggle-text")
    const toggleIcon = document.querySelector(".toggle-icon")
  
    // Check for saved theme preference or use device preference
    const savedTheme = localStorage.getItem("theme")
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
  
    // Set initial theme based on saved preference or device preference
    if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
      document.documentElement.setAttribute("data-theme", "dark")
      themeSwitch.checked = true
      toggleText.textContent = "Dark"
      toggleIcon.textContent = "🌙"
    }
  
    // Handle theme toggle with smooth transition
    themeSwitch.addEventListener("change", function () {
      // Add transition class to body for smoother theme change
      document.body.style.transition = "background-color 0.5s ease, color 0.5s ease"
  
      if (this.checked) {
        document.documentElement.setAttribute("data-theme", "dark")
        localStorage.setItem("theme", "dark")
        toggleText.textContent = "Dark"
        toggleIcon.textContent = "🌙"
      } else {
        document.documentElement.setAttribute("data-theme", "light")
        localStorage.setItem("theme", "light")
        toggleText.textContent = "Light"
        toggleIcon.textContent = "☀️"
      }
  
      // Remove transition after theme change is complete
      setTimeout(() => {
        document.body.style.transition = ""
      }, 500)
    })
  })
  
  