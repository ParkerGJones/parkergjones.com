document.addEventListener("DOMContentLoaded", () => {
    const lightbox = document.getElementById("lightbox");
    const lightboxImage = document.getElementById("lightbox-image");
    const closeBtn = document.getElementById("lightbox-close");
    const backdrop = document.querySelector(".lightbox-backdrop");
    const lightboxContent = document.querySelector(".lightbox-content");

    document.querySelectorAll(".photo-grid img").forEach((img) => {
        img.addEventListener("click", () => {
            lightboxImage.src = img.src;
            lightbox.classList.add("is-open");
        });
    });

    function closeLightbox() {
        lightbox.classList.remove("is-open");
        lightboxImage.src = "";
    }

    // X button closes
    closeBtn.addEventListener("click", closeLightbox);

    // Clicking outside (backdrop) closes
    backdrop.addEventListener("click", closeLightbox);

    // NEW: clicking top area OR any place in the content except the image closes
    lightboxContent.addEventListener("click", (e) => {
        if (e.target !== lightboxImage) closeLightbox();
    });

    // ESC key closes
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeLightbox();
    });
});
