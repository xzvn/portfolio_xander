document.addEventListener("DOMContentLoaded", () => {
  const reducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  const coarsePointer = window.matchMedia(
    "(pointer: coarse)"
  ).matches;

  const topbar = document.querySelector(".admin-topbar");

  const interactiveSelectors = [
    ".stat-card",
    ".dashboard-card",
    ".form-card",
    ".message-summary-card",
    ".quick-action",
    ".system-status-item",
    ".activity-item",
    ".experience-item",
    ".project-item",
    ".message-card",
  ];

  const interactiveCards = document.querySelectorAll(
    interactiveSelectors.join(",")
  );

  interactiveCards.forEach((card) => {
    card.classList.add("modern-interactive-card");

    if (reducedMotion || coarsePointer) {
      return;
    }

    card.addEventListener("pointermove", (event) => {
      const bounds = card.getBoundingClientRect();

      const x = event.clientX - bounds.left;
      const y = event.clientY - bounds.top;

      card.style.setProperty("--modern-spot-x", `${x}px`);
      card.style.setProperty("--modern-spot-y", `${y}px`);
    });
  });

  const revealSelectors = [
    ".welcome-section",
    ".statistics-grid",
    ".dashboard-grid",
    ".form-card",
    ".dashboard-card",
    ".message-summary-grid",
  ];

  const revealElements = document.querySelectorAll(
    revealSelectors.join(",")
  );

  if (reducedMotion || !("IntersectionObserver" in window)) {
    revealElements.forEach((element) => {
      element.classList.add("is-visible");
    });
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) {
            return;
          }

          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.08,
        rootMargin: "0px 0px -24px 0px",
      }
    );

    revealElements.forEach((element, index) => {
      element.classList.add("modern-reveal");
      element.style.transitionDelay = `${Math.min(index * 45, 180)}ms`;
      revealObserver.observe(element);
    });
  }

  const updateTopbarShadow = () => {
    if (!topbar) {
      return;
    }

    topbar.classList.toggle(
      "is-scrolled",
      window.scrollY > 12
    );
  };

  updateTopbarShadow();

  window.addEventListener(
    "scroll",
    updateTopbarShadow,
    { passive: true }
  );

  const rippleSelectors = [
    ".primary-button",
    ".secondary-button",
    ".outline-button",
    ".message-delete-button",
    ".table-action",
    ".topbar-icon-button",
    ".menu-toggle",
  ];

  document.querySelectorAll(
    rippleSelectors.join(",")
  ).forEach((button) => {
    button.addEventListener("pointerdown", (event) => {
      if (reducedMotion) {
        return;
      }

      const bounds = button.getBoundingClientRect();
      const diameter = Math.max(
        bounds.width,
        bounds.height
      );

      const ripple = document.createElement("span");

      ripple.className = "modern-button-ripple";
      ripple.style.width = `${diameter}px`;
      ripple.style.height = `${diameter}px`;
      ripple.style.left = `${event.clientX - bounds.left}px`;
      ripple.style.top = `${event.clientY - bounds.top}px`;

      button.querySelector(".modern-button-ripple")?.remove();
      button.appendChild(ripple);

      ripple.addEventListener(
        "animationend",
        () => ripple.remove(),
        { once: true }
      );
    });
  });
});
