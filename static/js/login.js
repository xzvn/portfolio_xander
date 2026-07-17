document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector("[data-access-page]");
  const card = document.querySelector("[data-access-card]");
  const sculpture = document.querySelector("[data-sculpture]");
  const sculptureX = document.querySelector("[data-sculpture-x]");
  const passwordInput = document.getElementById("password");
  const toggleButton = document.getElementById("togglePassword");
  const capsLockWarning = document.getElementById("capsLockWarning");
  const loginForm = document.querySelector(".access-form");
  const loginButton = document.querySelector(".access-submit");

  const reducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  const coarsePointer = window.matchMedia(
    "(pointer: coarse)"
  ).matches;

  const renderLucideIcons = () => {
    let attempt = 0;
    const maximumAttempts = 24;

    const render = () => {
      if (
        window.lucide
        && typeof window.lucide.createIcons === "function"
      ) {
        window.lucide.createIcons();
        return;
      }

      attempt += 1;

      if (attempt <= maximumAttempts) {
        window.setTimeout(render, 100);
      }
    };

    render();
  };

  const updateInputState = (input) => {
    const wrapper = input.closest("[data-input-wrapper]");

    if (!wrapper) {
      return;
    }

    wrapper.classList.toggle(
      "is-filled",
      input.value.trim().length > 0
    );
  };

  renderLucideIcons();

  document.querySelectorAll("[data-input-wrapper] input").forEach(
    (input) => {
      updateInputState(input);

      input.addEventListener("focus", () => {
        input.closest("[data-input-wrapper]")?.classList.add(
          "is-focused"
        );
      });

      input.addEventListener("blur", () => {
        input.closest("[data-input-wrapper]")?.classList.remove(
          "is-focused"
        );
      });

      input.addEventListener("input", () => {
        updateInputState(input);
      });
    }
  );

  if (passwordInput && toggleButton) {
    toggleButton.addEventListener("click", () => {
      const isHidden = passwordInput.type === "password";

      passwordInput.type = isHidden ? "text" : "password";

      toggleButton.setAttribute(
        "aria-label",
        isHidden
          ? "Sembunyikan password"
          : "Tampilkan password"
      );

      toggleButton.setAttribute(
        "aria-pressed",
        String(isHidden)
      );

      toggleButton.innerHTML = isHidden
        ? '<i data-lucide="eye-off"></i>'
        : '<i data-lucide="eye"></i>';

      renderLucideIcons();
      passwordInput.focus();
    });

    const updateCapsLock = (event) => {
      if (!capsLockWarning) {
        return;
      }

      const isActive = event.getModifierState
        ? event.getModifierState("CapsLock")
        : false;

      capsLockWarning.hidden = !isActive;
    };

    passwordInput.addEventListener("keydown", updateCapsLock);
    passwordInput.addEventListener("keyup", updateCapsLock);

    passwordInput.addEventListener("blur", () => {
      if (capsLockWarning) {
        capsLockWarning.hidden = true;
      }
    });
  }

  if (
    page
    && !reducedMotion
    && !coarsePointer
  ) {
    page.addEventListener("pointermove", (event) => {
      const xPercent = (
        event.clientX / window.innerWidth
      ) * 100;

      const yPercent = (
        event.clientY / window.innerHeight
      ) * 100;

      page.style.setProperty(
        "--pointer-x",
        `${xPercent}%`
      );

      page.style.setProperty(
        "--pointer-y",
        `${yPercent}%`
      );

      if (sculpture) {
        const moveX = (
          event.clientX / window.innerWidth - 0.5
        ) * 13;

        const moveY = (
          event.clientY / window.innerHeight - 0.5
        ) * 9;

        sculpture.style.transform = `
          translate3d(${moveX}px, ${moveY}px, 0)
        `;
      }

      if (sculptureX) {
        const rotateY = (
          event.clientX / window.innerWidth - 0.5
        ) * 5;

        const rotateX = (
          0.5 - event.clientY / window.innerHeight
        ) * 4;

        sculptureX.style.transform = `
          perspective(920px)
          rotateX(${8 + rotateX}deg)
          rotateY(${-14 + rotateY}deg)
          rotateZ(-2deg)
        `;
      }
    });

    page.addEventListener("pointerleave", () => {
      if (sculpture) {
        sculpture.style.transform = "";
      }

      if (sculptureX) {
        sculptureX.style.transform = "";
      }
    });
  }

  if (
    card
    && !reducedMotion
    && !coarsePointer
  ) {
    card.addEventListener("pointermove", (event) => {
      const bounds = card.getBoundingClientRect();

      const xPercent = (
        (event.clientX - bounds.left) / bounds.width
      ) * 100;

      const yPercent = (
        (event.clientY - bounds.top) / bounds.height
      ) * 100;

      card.style.setProperty(
        "--card-pointer-x",
        `${xPercent}%`
      );

      card.style.setProperty(
        "--card-pointer-y",
        `${yPercent}%`
      );
    });
  }

  document.querySelectorAll("[data-ripple-button]").forEach(
    (button) => {
      button.addEventListener("pointerdown", (event) => {
        const bounds = button.getBoundingClientRect();

        const diameter = Math.max(
          bounds.width,
          bounds.height
        );

        const ripple = document.createElement("span");

        ripple.className = "access-ripple";
        ripple.style.width = `${diameter}px`;
        ripple.style.height = `${diameter}px`;
        ripple.style.left = `${event.clientX - bounds.left}px`;
        ripple.style.top = `${event.clientY - bounds.top}px`;

        button.querySelector(".access-ripple")?.remove();
        button.appendChild(ripple);

        ripple.addEventListener(
          "animationend",
          () => ripple.remove(),
          { once: true }
        );
      });
    }
  );

  document.querySelectorAll(".access-flash").forEach(
    (flashMessage) => {
      window.setTimeout(() => {
        flashMessage.classList.add("is-hiding");

        window.setTimeout(() => {
          flashMessage.remove();
        }, 320);
      }, 6500);
    }
  );

  if (loginForm && loginButton) {
    loginForm.addEventListener("submit", (event) => {
      if (!loginForm.checkValidity()) {
        event.preventDefault();

        loginForm.classList.remove("is-invalid");
        void loginForm.offsetWidth;
        loginForm.classList.add("is-invalid");
        loginForm.reportValidity();
        return;
      }

      loginButton.disabled = true;
      loginButton.setAttribute("aria-busy", "true");

      loginButton.innerHTML = `
        <span
          class="access-loading-spinner"
          aria-hidden="true"
        ></span>
        <span>Memverifikasi akses...</span>
      `;
    });
  }
});
