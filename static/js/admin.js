document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  const sidebar = document.getElementById("adminSidebar");
  const menuToggle = document.getElementById("menuToggle");
  const sidebarClose = document.getElementById("sidebarClose");
  const sidebarOverlay = document.getElementById("sidebarOverlay");

  if (!sidebar || !menuToggle || !sidebarClose || !sidebarOverlay) {
    return;
  }

  let lockedScrollPosition = 0;

  const lockPageScroll = () => {
    lockedScrollPosition = window.scrollY;
    document.body.style.top = `-${lockedScrollPosition}px`;
    document.body.classList.add("sidebar-open");
  };

  const unlockPageScroll = () => {
    document.body.classList.remove("sidebar-open");
    document.body.style.top = "";
    window.scrollTo(0, lockedScrollPosition);
  };

  const openSidebar = () => {
    sidebar.classList.add("open");
    sidebarOverlay.classList.add("visible");
    lockPageScroll();

    sidebar.setAttribute("aria-hidden", "false");
    sidebarOverlay.setAttribute("aria-hidden", "false");
    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Tutup menu admin");

    window.setTimeout(() => sidebarClose.focus(), 120);
  };

  const closeSidebar = ({ restoreFocus = false } = {}) => {
    const wasOpen = sidebar.classList.contains("open");

    sidebar.classList.remove("open");
    sidebarOverlay.classList.remove("visible");

    if (wasOpen) {
      unlockPageScroll();
    }

    sidebar.setAttribute("aria-hidden", "true");
    sidebarOverlay.setAttribute("aria-hidden", "true");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Buka menu admin");

    if (restoreFocus) {
      menuToggle.focus();
    }
  };

  menuToggle.addEventListener("click", () => {
    if (sidebar.classList.contains("open")) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });

  sidebarClose.addEventListener("click", () => {
    closeSidebar({ restoreFocus: true });
  });

  sidebarOverlay.addEventListener("click", () => {
    closeSidebar({ restoreFocus: true });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && sidebar.classList.contains("open")) {
      closeSidebar({ restoreFocus: true });
    }
  });

  sidebar.querySelectorAll("a.sidebar-link").forEach((link) => {
    link.addEventListener("click", () => closeSidebar());
  });

  closeSidebar();
});
