document.addEventListener("DOMContentLoaded", () => {
  const themeTogglers = document.querySelectorAll(".theme-toggler");
  const menuIcon = document.querySelector(".menu-icon img");
  const closeIcon = document.querySelector(".close-icon");
  const mobileMenu = document.querySelector(".mobile-menu .container");
  const closeIconImg = document.querySelector(".close-icon img");

  const setIcons = (isDark) => {
    themeTogglers.forEach((toggler) => {
      const img = toggler.querySelector("img");
      img.src = isDark ? urls.sun : urls.moon;
    });

    if (closeIconImg) {
      closeIconImg.src = isDark ? urls.closeDark : urls.closeLight;
    }

    if (menuIcon) {
      menuIcon.src = isDark ? urls.menuDark : urls.menuLight;
    }
  };

  // Open mobile Menu
  menuIcon.addEventListener("click", () => {
    mobileMenu.style.display = "flex";
  });
  // Close mobile menu
  closeIcon.addEventListener("click", () => {
    mobileMenu.style.display = "none";
  });
  // Initial setup
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  document.documentElement.classList.toggle("dark", prefersDark);
  setIcons(prefersDark);

  // Toggle theme
  themeTogglers.forEach((toggler) => {
    toggler.addEventListener("click", () => {
      const root = document.documentElement;
      root.classList.toggle("dark");
      const isDark = root.classList.contains("dark");
      setIcons(isDark);
    });
  });
});
