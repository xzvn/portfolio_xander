document.addEventListener("DOMContentLoaded", () => {
  const clampPercentage = (value) => {
    const parsedValue = Number.parseInt(value, 10);
    if (Number.isNaN(parsedValue)) return 0;
    return Math.min(100, Math.max(0, parsedValue));
  };

  document.querySelectorAll("[data-skill-percentage-editor]").forEach((editor) => {
    const numberInput = editor.querySelector("[data-percentage-number]");
    const rangeInput = editor.querySelector("[data-percentage-range]");
    const output = editor.querySelector("[data-percentage-output]");
    const previewFill = editor.querySelector("[data-percentage-fill]");
    if (!numberInput || !rangeInput) return;

    const render = (value) => {
      const safeValue = clampPercentage(value);
      numberInput.value = String(safeValue);
      rangeInput.value = String(safeValue);
      if (output) output.textContent = `${safeValue}%`;
      if (previewFill) previewFill.style.width = `${safeValue}%`;
      rangeInput.style.setProperty("--skill-percentage", `${safeValue}%`);
    };

    numberInput.addEventListener("input", () => render(numberInput.value));
    numberInput.addEventListener("blur", () => render(numberInput.value));
    rangeInput.addEventListener("input", () => render(rangeInput.value));
    render(numberInput.value);
  });
});
