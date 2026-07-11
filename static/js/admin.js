document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  const sidebar = document.getElementById("adminSidebar");
  const menuToggle = document.getElementById("menuToggle");
  const sidebarClose = document.getElementById("sidebarClose");
  const sidebarOverlay = document.getElementById("sidebarOverlay");

  if (!sidebar || !menuToggle || !sidebarClose || !sidebarOverlay) {
    return;
  }

  const openSidebar = () => {
    sidebar.classList.add("open");
    sidebarOverlay.classList.add("visible");
    document.body.classList.add("sidebar-open");

    sidebar.setAttribute("aria-hidden", "false");
    sidebarOverlay.setAttribute("aria-hidden", "false");

    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Tutup menu admin");

    window.setTimeout(() => {
      sidebarClose.focus();
    }, 150);
  };

  const closeSidebar = () => {
    sidebar.classList.remove("open");
    sidebarOverlay.classList.remove("visible");
    document.body.classList.remove("sidebar-open");

    sidebar.setAttribute("aria-hidden", "true");
    sidebarOverlay.setAttribute("aria-hidden", "true");

    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Buka menu admin");
  };

  const toggleSidebar = () => {
    const sidebarIsOpen = sidebar.classList.contains("open");

    if (sidebarIsOpen) {
      closeSidebar();
    } else {
      openSidebar();
    }
  };

  menuToggle.addEventListener("click", toggleSidebar);
  sidebarClose.addEventListener("click", closeSidebar);
  sidebarOverlay.addEventListener("click", closeSidebar);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && sidebar.classList.contains("open")) {
      closeSidebar();
      menuToggle.focus();
    }
  });

  document
    .querySelectorAll(".sidebar-link:not(.placeholder-link)")
    .forEach((link) => {
      link.addEventListener("click", () => {
        closeSidebar();
      });
    });

  document.querySelectorAll(".placeholder-link").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
    });
  });
});
