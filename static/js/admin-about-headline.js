document.addEventListener("DOMContentLoaded", () => {
  const editor = document.querySelector("[data-headline-editor]");

  if (!editor) {
    return;
  }

  const input = editor.querySelector("[data-headline-input]");
  const preview = editor.querySelector("[data-headline-preview]");
  const counter = editor.querySelector("[data-headline-counter]");
  const saveState = editor.querySelector(
    "[data-headline-save-state]"
  );

  if (!input || !preview || !counter) {
    return;
  }

  const initialValue = input.value.trim();
  const maximumLength = Number.parseInt(
    input.getAttribute("maxlength"),
    10
  ) || 180;

  const render = () => {
    const value = input.value;
    const normalizedValue = value.trim();

    preview.textContent = normalizedValue
      || "Headline halaman About";

    counter.textContent = `${value.length}/${maximumLength}`;

    if (saveState) {
      saveState.textContent = normalizedValue === initialValue
        ? "Tidak ada perubahan baru"
        : "Perubahan siap disimpan";
    }
  };

  input.addEventListener("input", render);

  editor
    .querySelectorAll("[data-headline-preset]")
    .forEach((button) => {
      button.addEventListener("click", () => {
        input.value = button.dataset.headlinePreset || "";
        input.dispatchEvent(
          new Event("input", { bubbles: true })
        );
        input.focus();
      });
    });

  editor.addEventListener("submit", () => {
    if (saveState) {
      saveState.textContent = "Menyimpan headline...";
    }
  });

  render();
});
