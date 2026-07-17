document.addEventListener("DOMContentLoaded", () => {
  const editors = [
    {
      cardSelector: ".experience-form-card",
      formSelector: ".experience-create-form",
      type: "experience",
      stages: [
        {
          number: "01",
          label: "Identitas",
          targetId: "posisi",
        },
        {
          number: "02",
          label: "Organisasi",
          targetId: "perusahaan",
        },
        {
          number: "03",
          label: "Cerita",
          targetId: "deskripsi",
        },
      ],
    },
    {
      cardSelector: ".project-form-card",
      formSelector: ".project-create-form",
      type: "project",
      stages: [
        {
          number: "01",
          label: "Informasi",
          targetId: "judul",
        },
        {
          number: "02",
          label: "Visual",
          targetId: "gambar_file",
        },
        {
          number: "03",
          label: "Publikasi",
          targetId: "link_project",
        },
      ],
    },
  ];

  const renderIcons = () => {
    if (
      window.lucide
      && typeof window.lucide.createIcons === "function"
    ) {
      window.lucide.createIcons();
    }
  };

  const createToolbar = (config) => {
    const toolbar = document.createElement("div");
    toolbar.className = "editor-studio-toolbar";

    const stageList = document.createElement("div");
    stageList.className = "editor-stage-list";

    config.stages.forEach((stage, index) => {
      const button = document.createElement("button");

      button.type = "button";
      button.className = "editor-stage-button";
      button.dataset.editorTarget = stage.targetId;

      if (index === 0) {
        button.classList.add("is-active");
      }

      button.innerHTML = `
        <span>${stage.number}</span>
        <strong>${stage.label}</strong>
      `;

      stageList.appendChild(button);
    });

    const completion = document.createElement("div");
    completion.className = "editor-completion-box";
    completion.innerHTML = `
      <div class="editor-completion-ring">
        <strong data-studio-progress-value>0%</strong>
      </div>

      <div class="editor-completion-copy">
        <strong>Kelengkapan</strong>
        <small data-studio-progress-label>
          Mulai isi formulir
        </small>
      </div>
    `;

    toolbar.append(stageList, completion);

    return toolbar;
  };

  const createExperiencePreview = () => {
    const preview = document.createElement("aside");
    preview.className = "editor-live-preview";
    preview.innerHTML = `
      <header class="editor-live-preview-header">
        <span>
          <i data-lucide="scan-eye"></i>
          Preview langsung
        </span>

        <span class="editor-live-badge">
          <i data-lucide="radio"></i>
          Live
        </span>
      </header>

      <div class="editor-preview-canvas">
        <article class="editor-preview-card editor-experience-preview">
          <span class="editor-preview-marker">
            <i data-lucide="briefcase-business"></i>
          </span>

          <div class="editor-preview-content">
            <p class="editor-preview-eyebrow">
              PENGALAMAN
            </p>

            <h3 data-preview-value="posisi">
              Posisi Anda
            </h3>

            <p
              class="editor-preview-company"
              data-preview-value="perusahaan"
            >
              Nama organisasi
            </p>

            <span class="editor-preview-duration">
              <i data-lucide="calendar-days"></i>

              <span data-preview-value="durasi">
                Periode belum diisi
              </span>
            </span>

            <p
              class="editor-preview-description"
              data-preview-value="deskripsi"
            >
              Deskripsi pengalaman akan tampil di area ini.
            </p>
          </div>
        </article>
      </div>

      <div class="editor-preview-tip">
        <i data-lucide="sparkles"></i>

        <div>
          <strong>Tips portfolio</strong>
          <p>
            Tambahkan kontribusi, dampak, atau hasil
            yang dapat diukur.
          </p>
        </div>
      </div>
    `;

    return preview;
  };

  const createProjectPreview = () => {
    const preview = document.createElement("aside");
    preview.className = "editor-live-preview";
    preview.innerHTML = `
      <header class="editor-live-preview-header">
        <span>
          <i data-lucide="scan-eye"></i>
          Preview langsung
        </span>

        <span class="editor-live-badge">
          <i data-lucide="radio"></i>
          Live
        </span>
      </header>

      <div class="editor-preview-canvas">
        <article class="editor-preview-card">
          <div class="editor-project-media">
            <img
              src=""
              alt=""
              data-studio-project-image
              hidden
            >

            <div class="editor-project-placeholder">
              <i data-lucide="image"></i>
              <span>Visual proyek</span>
            </div>
          </div>

          <div class="editor-project-copy">
            <p class="editor-preview-eyebrow">
              FEATURED PROJECT
            </p>

            <h3 data-preview-value="judul">
              Judul proyek
            </h3>

            <p data-preview-value="deskripsi">
              Deskripsi proyek akan tampil di area ini.
            </p>

            <span class="editor-preview-link">
              <i data-lucide="external-link"></i>

              <span data-preview-value="link_project">
                Link belum tersedia
              </span>
            </span>
          </div>
        </article>
      </div>

      <div class="editor-preview-tip">
        <i data-lucide="wand-sparkles"></i>

        <div>
          <strong>Tips proyek</strong>
          <p>
            Gunakan visual horizontal dan jelaskan
            masalah yang diselesaikan.
          </p>
        </div>
      </div>
    `;

    return preview;
  };

  const createActionDock = (submitButton, type) => {
    const dock = document.createElement("div");
    dock.className = "editor-action-dock";

    const saveState = document.createElement("div");
    saveState.className = "editor-save-state";
    saveState.innerHTML = `
      <span class="editor-save-state-dot"></span>

      <div>
        <strong data-studio-save-status>
          Editor siap digunakan
        </strong>

        <small>
          Data disimpan setelah tombol ditekan.
        </small>
      </div>
    `;

    const originalText = type === "project"
      ? "Tambah Proyek"
      : "Tambah Pengalaman";

    submitButton.innerHTML = `
      <span class="editor-submit-symbol">
        <i data-lucide="plus"></i>
      </span>

      <span class="editor-submit-copy">
        <strong>${originalText}</strong>
        <small>Publikasikan ke portfolio</small>
      </span>

      <i
        data-lucide="arrow-right"
        class="editor-submit-arrow"
      ></i>
    `;

    dock.append(saveState, submitButton);

    return dock;
  };

  const improveFileInput = (form) => {
    const input = form.querySelector("#gambar_file");

    if (!input) {
      return;
    }

    const wrapper = input.closest(".admin-file-wrapper");

    if (!wrapper) {
      return;
    }

    wrapper.classList.add("editor-file-dropzone");

    if (
      !wrapper.querySelector(".editor-file-dropzone-label")
    ) {
      const label = document.createElement("label");
      label.className = "editor-file-dropzone-label";
      label.setAttribute("for", input.id);

      label.innerHTML = `
        <span class="editor-file-dropzone-icon">
          <i data-lucide="image-up"></i>
        </span>

        <span class="editor-file-dropzone-copy">
          <strong>Pilih atau jatuhkan gambar</strong>
          <small>
            PNG, JPG, JPEG, atau WEBP · Maksimal 5 MB
          </small>
        </span>

        <span class="editor-file-dropzone-action">
          Pilih file
        </span>
      `;

      wrapper.appendChild(label);
    }

    ["dragenter", "dragover"].forEach((eventName) => {
      wrapper.addEventListener(eventName, (event) => {
        event.preventDefault();
        wrapper.classList.add("is-dragging");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      wrapper.addEventListener(eventName, (event) => {
        event.preventDefault();
        wrapper.classList.remove("is-dragging");
      });
    });

    wrapper.addEventListener("drop", (event) => {
      const file = event.dataTransfer?.files?.[0];

      if (!file) {
        return;
      }

      const transfer = new DataTransfer();
      transfer.items.add(file);
      input.files = transfer.files;

      input.dispatchEvent(
        new Event("change", { bubbles: true })
      );
    });
  };

  const initializeEditor = (config) => {
    const card = document.querySelector(config.cardSelector);
    const form = card?.querySelector(config.formSelector);

    if (!card || !form || card.dataset.studioReady) {
      return;
    }

    card.dataset.studioReady = "true";
    card.classList.add("editor-studio-card");
    form.classList.add("editor-enhanced-form");

    const cardHeader = card.querySelector(".form-card-header");
    const toolbar = createToolbar(config);

    cardHeader?.insertAdjacentElement(
      "afterend",
      toolbar
    );

    if (config.type === "project") {
      improveFileInput(form);
    }

    const submitButton = form.querySelector(
      ":scope > .primary-button"
    );

    const formGroups = [
      ...form.querySelectorAll(":scope > .form-group"),
    ];

    if (!submitButton || !formGroups.length) {
      return;
    }

    const studioGrid = document.createElement("div");
    studioGrid.className = "editor-studio-grid";

    const fieldStack = document.createElement("div");
    fieldStack.className = "editor-field-stack";

    formGroups.forEach((group) => {
      fieldStack.appendChild(group);
    });

    const preview = config.type === "project"
      ? createProjectPreview()
      : createExperiencePreview();

    studioGrid.append(fieldStack, preview);

    const actionDock = createActionDock(
      submitButton,
      config.type
    );

    form.append(studioGrid, actionDock);

    const inputFields = [
      ...form.querySelectorAll(
        "input:not([type='hidden']), textarea, select"
      ),
    ];

    const progressValue = toolbar.querySelector(
      "[data-studio-progress-value]"
    );

    const progressLabel = toolbar.querySelector(
      "[data-studio-progress-label]"
    );

    const completionRing = toolbar.querySelector(
      ".editor-completion-ring"
    );

    const saveStatus = actionDock.querySelector(
      "[data-studio-save-status]"
    );

    const emptyCopy = {
      posisi: "Posisi Anda",
      perusahaan: "Nama organisasi",
      durasi: "Periode belum diisi",
      deskripsi: config.type === "project"
        ? "Deskripsi proyek akan tampil di area ini."
        : "Deskripsi pengalaman akan tampil di area ini.",
      judul: "Judul proyek",
      link_project: "Link belum tersedia",
    };

    const hasValue = (field) => {
      if (field.type === "file") {
        return Boolean(field.files?.length);
      }

      return field.value.trim().length > 0;
    };

    const updateGroupState = (field) => {
      const group = field.closest(".form-group");

      group?.classList.toggle(
        "is-complete",
        hasValue(field)
      );
    };

    const updatePreview = (field) => {
      const target = preview.querySelector(
        `[data-preview-value="${field.id}"]`
      );

      if (target) {
        target.textContent = field.value.trim()
          || emptyCopy[field.id]
          || "Belum diisi";
      }
    };

    const updateCompletion = () => {
      const required = inputFields.filter(
        (field) => field.required
      );

      const optional = inputFields.filter(
        (field) => !field.required
      );

      const requiredWeight = required.length
        ? 70 / required.length
        : 0;

      const optionalWeight = optional.length
        ? 30 / optional.length
        : 0;

      const score = [
        ...required.map(
          (field) => hasValue(field)
            ? requiredWeight
            : 0
        ),
        ...optional.map(
          (field) => hasValue(field)
            ? optionalWeight
            : 0
        ),
      ].reduce((total, value) => total + value, 0);

      const percentage = Math.min(
        100,
        Math.round(score)
      );

      completionRing?.style.setProperty(
        "--studio-progress",
        `${percentage * 3.6}deg`
      );

      if (progressValue) {
        progressValue.textContent = `${percentage}%`;
      }

      if (progressLabel) {
        progressLabel.textContent = percentage === 100
          ? "Siap dipublikasikan"
          : percentage >= 70
            ? "Hampir selesai"
            : percentage > 0
              ? "Lanjutkan pengisian"
              : "Mulai isi formulir";
      }

      if (saveStatus) {
        saveStatus.textContent = percentage >= 70
          ? "Perubahan siap disimpan"
          : percentage > 0
            ? "Formulir sedang dilengkapi"
            : "Editor siap digunakan";
      }
    };

    const setActiveStage = (field) => {
      const stageButtons = [
        ...toolbar.querySelectorAll(
          ".editor-stage-button"
        ),
      ];

      let activeButton = stageButtons.find(
        (button) => (
          button.dataset.editorTarget === field.id
        )
      );

      if (!activeButton) {
        const fieldIndex = inputFields.indexOf(field);
        const proportionalIndex = Math.min(
          stageButtons.length - 1,
          Math.floor(
            fieldIndex
            / Math.max(
              1,
              Math.ceil(
                inputFields.length / stageButtons.length
              )
            )
          )
        );

        activeButton = stageButtons[proportionalIndex];
      }

      stageButtons.forEach((button) => {
        button.classList.toggle(
          "is-active",
          button === activeButton
        );
      });
    };

    inputFields.forEach((field) => {
      updateGroupState(field);
      updatePreview(field);

      const eventName = field.type === "file"
        ? "change"
        : "input";

      field.addEventListener(eventName, () => {
        updateGroupState(field);
        updatePreview(field);
        updateCompletion();
      });

      field.addEventListener("focus", () => {
        const group = field.closest(".form-group");

        fieldStack.querySelectorAll(".form-group").forEach(
          (item) => item.classList.remove("is-focused")
        );

        group?.classList.add("is-focused");
        setActiveStage(field);
      });

      field.addEventListener("blur", () => {
        field.closest(".form-group")
          ?.classList.remove("is-focused");
      });
    });

    toolbar.querySelectorAll(
      ".editor-stage-button"
    ).forEach((button) => {
      button.addEventListener("click", () => {
        const target = document.getElementById(
          button.dataset.editorTarget
        );

        if (!target) {
          return;
        }

        toolbar.querySelectorAll(
          ".editor-stage-button"
        ).forEach((item) => {
          item.classList.toggle(
            "is-active",
            item === button
          );
        });

        target.closest(".form-group")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });

        window.setTimeout(
          () => target.focus(),
          350
        );
      });
    });

    if (config.type === "project") {
      const imageInput = form.querySelector(
        "#gambar_file"
      );

      const previewImage = preview.querySelector(
        "[data-studio-project-image]"
      );

      const placeholder = preview.querySelector(
        ".editor-project-placeholder"
      );

      let objectUrl = null;

      imageInput?.addEventListener("change", () => {
        const file = imageInput.files?.[0];

        if (!file || !previewImage) {
          return;
        }

        if (objectUrl) {
          URL.revokeObjectURL(objectUrl);
        }

        objectUrl = URL.createObjectURL(file);

        previewImage.src = objectUrl;
        previewImage.hidden = false;

        if (placeholder) {
          placeholder.hidden = true;
        }
      });

      window.addEventListener("beforeunload", () => {
        if (objectUrl) {
          URL.revokeObjectURL(objectUrl);
        }
      });
    }

    form.addEventListener("submit", () => {
      if (saveStatus) {
        saveStatus.textContent =
          "Menyimpan ke portfolio...";
      }
    });

    updateCompletion();
    renderIcons();
  };

  editors.forEach(initializeEditor);
});
