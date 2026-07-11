document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("foto_file");
  const previewImage = document.getElementById("profilePhotoImage");
  const previewPlaceholder = document.getElementById("profilePhotoPlaceholder");
  const fileNameLabel = document.getElementById("profileCropFileName");
  const modal = document.getElementById("photoCropModal");
  const backdrop = document.getElementById("photoCropBackdrop");
  const closeButton = document.getElementById("photoCropClose");
  const cancelButton = document.getElementById("photoCropCancel");
  const applyButton = document.getElementById("photoCropApply");
  const rotateLeftButton = document.getElementById("photoRotateLeft");
  const rotateRightButton = document.getElementById("photoRotateRight");
  const resetButton = document.getElementById("photoCropReset");
  const zoomInput = document.getElementById("photoCropZoom");
  const canvas = document.getElementById("photoCropCanvas");

  if (!fileInput || !modal || !canvas) {
    return;
  }

  const context = canvas.getContext("2d", { alpha: false });
  const initialPreviewSource = previewImage?.getAttribute("src") || "";
  let sourceImage = null;
  let selectedOriginalFile = null;
  let previewObjectUrl = null;
  let rotation = 0;
  let zoom = 1;
  let offsetX = 0;
  let offsetY = 0;
  let baseScale = 1;
  let pointerStart = null;
  let modalScrollPosition = 0;

  const allowedTypes = ["image/png", "image/jpeg", "image/webp"];
  const maximumFileSize = 5 * 1024 * 1024;

  const rotatedDimensions = () => {
    const quarterTurn = Math.abs(rotation % 180) === 90;
    return {
      width: quarterTurn ? sourceImage.height : sourceImage.width,
      height: quarterTurn ? sourceImage.width : sourceImage.height,
    };
  };

  const calculateBaseScale = () => {
    const dimensions = rotatedDimensions();
    baseScale = Math.max(
      canvas.width / dimensions.width,
      canvas.height / dimensions.height,
    );
  };

  const clampOffsets = () => {
    if (!sourceImage) return;
    const dimensions = rotatedDimensions();
    const scale = baseScale * zoom;
    const maximumX = Math.max(0, (dimensions.width * scale - canvas.width) / 2);
    const maximumY = Math.max(0, (dimensions.height * scale - canvas.height) / 2);
    offsetX = Math.min(maximumX, Math.max(-maximumX, offsetX));
    offsetY = Math.min(maximumY, Math.max(-maximumY, offsetY));
  };

  const drawToCanvas = (targetCanvas, outputRatio = 1) => {
    const targetContext = targetCanvas.getContext("2d", { alpha: false });
    targetContext.save();
    targetContext.fillStyle = "#ffffff";
    targetContext.fillRect(0, 0, targetCanvas.width, targetCanvas.height);
    targetContext.translate(
      targetCanvas.width / 2 + offsetX * outputRatio,
      targetCanvas.height / 2 + offsetY * outputRatio,
    );
    targetContext.rotate((rotation * Math.PI) / 180);
    const scale = baseScale * zoom * outputRatio;
    targetContext.scale(scale, scale);
    targetContext.drawImage(
      sourceImage,
      -sourceImage.width / 2,
      -sourceImage.height / 2,
    );
    targetContext.restore();
  };

  const drawPreview = () => {
    if (!sourceImage) return;
    clampOffsets();
    drawToCanvas(canvas, 1);
  };

  const resetCrop = () => {
    rotation = 0;
    zoom = 1;
    offsetX = 0;
    offsetY = 0;
    zoomInput.value = "1";
    calculateBaseScale();
    drawPreview();
  };

  const lockModalScroll = () => {
    modalScrollPosition = window.scrollY;
    document.body.style.top = `-${modalScrollPosition}px`;
    document.body.classList.add("photo-crop-open");
  };

  const unlockModalScroll = () => {
    document.body.classList.remove("photo-crop-open");
    document.body.style.top = "";
    window.scrollTo(0, modalScrollPosition);
  };

  const openModal = () => {
    modal.hidden = false;
    lockModalScroll();
    window.setTimeout(() => closeButton?.focus(), 80);
  };

  const restorePreviousPreview = () => {
    if (!previewImage) return;
    if (previewObjectUrl) {
      URL.revokeObjectURL(previewObjectUrl);
      previewObjectUrl = null;
    }
    previewImage.src = initialPreviewSource;
    previewImage.hidden = !initialPreviewSource;
    if (previewPlaceholder) {
      previewPlaceholder.hidden = Boolean(initialPreviewSource);
    }
  };

  const closeModal = ({ cancelSelection = false } = {}) => {
    modal.hidden = true;
    unlockModalScroll();
    pointerStart = null;
    if (cancelSelection) {
      fileInput.value = "";
      selectedOriginalFile = null;
      if (fileNameLabel) fileNameLabel.textContent = "Belum memilih foto baru";
      restorePreviousPreview();
    }
  };

  const loadImageSource = async (file) => {
    if ("createImageBitmap" in window) {
      return window.createImageBitmap(file, { imageOrientation: "from-image" });
    }

    return new Promise((resolve, reject) => {
      const image = new Image();
      const objectUrl = URL.createObjectURL(file);
      image.onload = () => {
        URL.revokeObjectURL(objectUrl);
        resolve(image);
      };
      image.onerror = () => {
        URL.revokeObjectURL(objectUrl);
        reject(new Error("Foto tidak dapat dibaca."));
      };
      image.src = objectUrl;
    });
  };

  fileInput.addEventListener("change", async () => {
    const file = fileInput.files?.[0];
    if (!file) return;

    if (!allowedTypes.includes(file.type)) {
      window.alert("Format foto harus PNG, JPG, JPEG, atau WEBP.");
      fileInput.value = "";
      return;
    }

    if (file.size > maximumFileSize) {
      window.alert("Ukuran foto maksimal 5 MB.");
      fileInput.value = "";
      return;
    }

    try {
      if (sourceImage && typeof sourceImage.close === "function") {
        sourceImage.close();
      }
      selectedOriginalFile = file;
      sourceImage = await loadImageSource(file);
      resetCrop();
      openModal();
    } catch (error) {
      fileInput.value = "";
      window.alert(error.message || "Foto tidak dapat dibuka.");
    }
  });

  zoomInput.addEventListener("input", () => {
    zoom = Number(zoomInput.value);
    drawPreview();
  });

  rotateLeftButton.addEventListener("click", () => {
    rotation = (rotation - 90) % 360;
    offsetX = 0;
    offsetY = 0;
    calculateBaseScale();
    drawPreview();
  });

  rotateRightButton.addEventListener("click", () => {
    rotation = (rotation + 90) % 360;
    offsetX = 0;
    offsetY = 0;
    calculateBaseScale();
    drawPreview();
  });

  resetButton.addEventListener("click", resetCrop);

  canvas.addEventListener("pointerdown", (event) => {
    pointerStart = {
      x: event.clientX,
      y: event.clientY,
      offsetX,
      offsetY,
    };
    canvas.setPointerCapture(event.pointerId);
    canvas.classList.add("dragging");
  });

  canvas.addEventListener("pointermove", (event) => {
    if (!pointerStart) return;
    offsetX = pointerStart.offsetX + event.clientX - pointerStart.x;
    offsetY = pointerStart.offsetY + event.clientY - pointerStart.y;
    drawPreview();
  });

  const stopDragging = (event) => {
    pointerStart = null;
    canvas.classList.remove("dragging");
    if (event.pointerId !== undefined && canvas.hasPointerCapture(event.pointerId)) {
      canvas.releasePointerCapture(event.pointerId);
    }
  };

  canvas.addEventListener("pointerup", stopDragging);
  canvas.addEventListener("pointercancel", stopDragging);

  applyButton.addEventListener("click", () => {
    if (!sourceImage || !selectedOriginalFile) return;

    const exportCanvas = document.createElement("canvas");
    exportCanvas.width = 800;
    exportCanvas.height = 800;
    drawToCanvas(exportCanvas, 800 / canvas.width);

    applyButton.disabled = true;

    exportCanvas.toBlob(
      (blob) => {
        applyButton.disabled = false;
        if (!blob) {
          window.alert("Crop foto gagal dibuat.");
          return;
        }

        const baseName = selectedOriginalFile.name.replace(/\.[^.]+$/, "");
        const croppedFile = new File(
          [blob],
          `${baseName}-cropped.jpg`,
          { type: "image/jpeg", lastModified: Date.now() },
        );

        const transfer = new DataTransfer();
        transfer.items.add(croppedFile);
        fileInput.files = transfer.files;

        if (previewObjectUrl) URL.revokeObjectURL(previewObjectUrl);
        previewObjectUrl = URL.createObjectURL(croppedFile);

        if (previewImage) {
          previewImage.src = previewObjectUrl;
          previewImage.hidden = false;
        }
        if (previewPlaceholder) previewPlaceholder.hidden = true;
        if (fileNameLabel) fileNameLabel.textContent = croppedFile.name;

        closeModal();
      },
      "image/jpeg",
      0.92,
    );
  });

  backdrop.addEventListener("click", () => closeModal({ cancelSelection: true }));
  closeButton.addEventListener("click", () => closeModal({ cancelSelection: true }));
  cancelButton.addEventListener("click", () => closeModal({ cancelSelection: true }));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !modal.hidden) {
      closeModal({ cancelSelection: true });
    }
  });

  window.addEventListener("beforeunload", () => {
    if (previewObjectUrl) URL.revokeObjectURL(previewObjectUrl);
    if (sourceImage && typeof sourceImage.close === "function") sourceImage.close();
  });
});
