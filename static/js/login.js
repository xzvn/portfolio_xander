document.addEventListener("DOMContentLoaded", () => {
    if (window.lucide) {
        lucide.createIcons();
    }

    const passwordInput = document.getElementById("password");
    const toggleButton = document.getElementById("togglePassword");
    const loginForm = document.querySelector(".login-form");
    const loginButton = document.querySelector(".login-button");

    if (passwordInput && toggleButton) {
        toggleButton.addEventListener("click", () => {
            const passwordHidden =
                passwordInput.type === "password";

            passwordInput.type = passwordHidden
                ? "text"
                : "password";

            toggleButton.innerHTML = passwordHidden
                ? '<i data-lucide="eye-off"></i>'
                : '<i data-lucide="eye"></i>';

            toggleButton.setAttribute(
                "aria-label",
                passwordHidden
                    ? "Sembunyikan password"
                    : "Tampilkan password"
            );

            if (window.lucide) {
                lucide.createIcons();
            }

            passwordInput.focus();
        });
    }

    if (loginForm && loginButton) {
        loginForm.addEventListener("submit", () => {
            loginButton.disabled = true;

            loginButton.innerHTML = `
                <span class="loading-spinner"></span>
                <span>Sedang masuk...</span>
            `;
        });
    }
});