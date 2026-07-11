document.addEventListener("DOMContentLoaded", () => {
    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    /*
     * Mengambil seluruh text node, termasuk teks
     * yang berada di dalam span atau elemen lainnya.
     */
    const getTextNodes = (element) => {
        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT
        );

        const textNodes = [];
        let currentNode = walker.nextNode();

        while (currentNode) {
            textNodes.push(currentNode);
            currentNode = walker.nextNode();
        }

        return textNodes;
    };

    /*
     * TYPEWRITER EFFECT
     *
     * Otomatis diterapkan pada:
     * 1. Elemen yang memiliki data-typewriter.
     * 2. H1 pertama di dalam main.
     * 3. H1 pertama di halaman sebagai fallback.
     */
    const initializeTypewriter = () => {
        const heading =
            document.querySelector("[data-typewriter]")
            || document.querySelector("main h1")
            || document.querySelector("h1");

        if (
            !heading
            || heading.dataset.typewriterInitialized === "true"
        ) {
            return;
        }

        heading.dataset.typewriterInitialized = "true";

        const fullAccessibleText =
            heading.textContent
                .replace(/\s+/g, " ")
                .trim();

        heading.setAttribute(
            "aria-label",
            fullAccessibleText
        );

        /*
         * Tidak menjalankan animasi saat pengguna
         * memilih reduced motion.
         */
        if (reducedMotion) {
            heading.classList.add("typewriter-complete");
            return;
        }

        const sourceClone = heading.cloneNode(true);
        const targetClone = heading.cloneNode(true);

        const sourceNodes = getTextNodes(sourceClone);
        const targetNodes = getTextNodes(targetClone);

        const textPlan = sourceNodes.map((node) => {
            const originalText = node.nodeValue || "";

            /*
             * Menghilangkan spasi indentasi HTML,
             * tetapi mempertahankan spasi antar kata.
             */
            if (!originalText.trim()) {
                return "";
            }

            return originalText.replace(/\s+/g, " ");
        });

        targetNodes.forEach((node) => {
            node.nodeValue = "";
        });

        const originalHeight = heading.offsetHeight;

        if (originalHeight > 0) {
            heading.style.minHeight = `${originalHeight}px`;
        }

        heading.replaceChildren(
            ...Array.from(targetClone.childNodes)
        );

        const typingTargets = getTextNodes(heading);

        const speed = Number(
            heading.dataset.typewriterSpeed || 28
        );

        const startDelay = Number(
            heading.dataset.typewriterDelay || 250
        );

        let nodeIndex = 0;
        let characterIndex = 0;

        heading.classList.add("typewriter-active");

        const typeNextCharacter = () => {
            if (nodeIndex >= textPlan.length) {
                heading.classList.remove("typewriter-active");
                heading.classList.add("typewriter-complete");

                window.setTimeout(() => {
                    heading.style.minHeight = "";
                }, 300);

                return;
            }

            const currentText = textPlan[nodeIndex];
            const targetNode = typingTargets[nodeIndex];

            if (!targetNode) {
                nodeIndex += 1;
                characterIndex = 0;
                typeNextCharacter();
                return;
            }

            if (characterIndex >= currentText.length) {
                nodeIndex += 1;
                characterIndex = 0;
                typeNextCharacter();
                return;
            }

            const character = currentText[characterIndex];

            targetNode.nodeValue += character;
            characterIndex += 1;

            /*
             * Jeda sedikit lebih panjang setelah tanda baca.
             */
            let currentSpeed = speed;

            if ([".", ",", "!", "?", ":"].includes(character)) {
                currentSpeed = speed * 4;
            }

            window.setTimeout(
                typeNextCharacter,
                currentSpeed
            );
        };

        window.setTimeout(
            typeNextCharacter,
            startDelay
        );
    };

    /*
     * SCROLL PROGRESS BAR
     */
    const initializeScrollProgress = () => {
        const progressBar =
            document.createElement("div");

        progressBar.className =
            "global-scroll-progress";

        progressBar.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.appendChild(progressBar);

        const updateProgress = () => {
            const scrollableHeight =
                document.documentElement.scrollHeight
                - window.innerHeight;

            const progress =
                scrollableHeight > 0
                    ? window.scrollY / scrollableHeight
                    : 0;

            progressBar.style.transform =
                `scaleX(${Math.min(progress, 1)})`;
        };

        window.addEventListener(
            "scroll",
            updateProgress,
            {
                passive: true,
            }
        );

        window.addEventListener(
            "resize",
            updateProgress
        );

        updateProgress();
    };

    /*
     * TOMBOL KEMBALI KE ATAS
     */
    const initializeBackToTop = () => {
        const backToTopButton =
            document.createElement("button");

        backToTopButton.type = "button";
        backToTopButton.className =
            "global-back-to-top";

        backToTopButton.setAttribute(
            "aria-label",
            "Kembali ke bagian atas halaman"
        );

        backToTopButton.innerHTML = `
            <span aria-hidden="true">↑</span>
        `;

        document.body.appendChild(
            backToTopButton
        );

        const updateButtonVisibility = () => {
            backToTopButton.classList.toggle(
                "visible",
                window.scrollY > 550
            );
        };

        backToTopButton.addEventListener(
            "click",
            () => {
                window.scrollTo({
                    top: 0,
                    behavior: reducedMotion
                        ? "auto"
                        : "smooth",
                });
            }
        );

        window.addEventListener(
            "scroll",
            updateButtonVisibility,
            {
                passive: true,
            }
        );

        updateButtonVisibility();
    };

    /*
     * PARALLAX RINGAN PADA VISUAL HERO
     */
    const initializeHeroParallax = () => {
        if (
            reducedMotion
            || window.matchMedia(
                "(pointer: coarse)"
            ).matches
        ) {
            return;
        }

        const heroVisual =
            document.querySelector(
                '[class*="-hero-visual"]'
            );

        if (!heroVisual) {
            return;
        }

        const parallaxTarget =
            heroVisual.firstElementChild;

        if (!parallaxTarget) {
            return;
        }

        parallaxTarget.classList.add(
            "global-parallax-target"
        );

        heroVisual.addEventListener(
            "pointermove",
            (event) => {
                const bounds =
                    heroVisual.getBoundingClientRect();

                const horizontalPosition =
                    (event.clientX - bounds.left)
                    / bounds.width;

                const verticalPosition =
                    (event.clientY - bounds.top)
                    / bounds.height;

                const moveX =
                    (horizontalPosition - 0.5) * 14;

                const moveY =
                    (verticalPosition - 0.5) * 14;

                const rotateX =
                    (0.5 - verticalPosition) * 4;

                const rotateY =
                    (horizontalPosition - 0.5) * 4;

                parallaxTarget.style.transform = `
                    perspective(1000px)
                    translate3d(
                        ${moveX}px,
                        ${moveY}px,
                        0
                    )
                    rotateX(${rotateX}deg)
                    rotateY(${rotateY}deg)
                `;
            }
        );

        heroVisual.addEventListener(
            "pointerleave",
            () => {
                parallaxTarget.style.transform = "";
            }
        );
    };

    /*
     * EFEK TILT PADA KARTU
     */
    const initializeInteractiveCards = () => {
        if (
            reducedMotion
            || window.matchMedia(
                "(pointer: coarse)"
            ).matches
        ) {
            return;
        }

        const cardSelectors = [
            ".public-project-item",
        ].join(",");

        const cards =
            document.querySelectorAll(cardSelectors);

        cards.forEach((card) => {
            card.classList.add(
                "global-interactive-card"
            );

            card.addEventListener(
                "pointermove",
                (event) => {
                    const bounds =
                        card.getBoundingClientRect();

                    const positionX =
                        (event.clientX - bounds.left)
                        / bounds.width;

                    const positionY =
                        (event.clientY - bounds.top)
                        / bounds.height;

                    const rotateY =
                        (positionX - 0.5) * 5;

                    const rotateX =
                        (0.5 - positionY) * 5;

                    card.style.transform = `
                        perspective(900px)
                        translateY(-6px)
                        rotateX(${rotateX}deg)
                        rotateY(${rotateY}deg)
                    `;
                }
            );

            card.addEventListener(
                "pointerleave",
                () => {
                    card.style.transform = "";
                }
            );
        });
    };

    /*
     * SCROLL HALUS UNTUK LINK ANCHOR
     */
    const initializeSmoothAnchors = () => {
        const anchorLinks =
            document.querySelectorAll(
                'a[href^="#"]:not([href="#"])'
            );

        anchorLinks.forEach((link) => {
            link.addEventListener(
                "click",
                (event) => {
                    const targetId =
                        link.getAttribute("href");

                    const targetElement =
                        document.querySelector(targetId);

                    if (!targetElement) {
                        return;
                    }

                    event.preventDefault();

                    targetElement.scrollIntoView({
                        behavior: reducedMotion
                            ? "auto"
                            : "smooth",
                        block: "start",
                    });
                }
            );
        });
    };

    initializeTypewriter();
    initializeScrollProgress();
    initializeBackToTop();
    initializeHeroParallax();
    initializeInteractiveCards();
    initializeSmoothAnchors();
});