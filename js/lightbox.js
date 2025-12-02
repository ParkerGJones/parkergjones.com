document.addEventListener("DOMContentLoaded", () => {
  const lightbox = document.getElementById("lightbox");
  const lightboxImage = document.getElementById("lightbox-image");
  const closeBtn = document.querySelector(".lightbox-close");
  const backdrop = document.querySelector(".lightbox-backdrop");

  // open lightbox when any image in .photo-grid is clicked
  document.querySelectorAll(".photo-grid img").forEach((img) => {
    img.addEventListener("click", () => {
      lightboxImage.src = img.src;
      lightboxImage.alt = img.alt || "Photo";
      lightbox.classList.add("is-open");
    });
  });

  function closeLightbox() {
    lightbox.classList.remove("is-open");
    lightboxImage.src = "";
  }

  closeBtn.addEventListener("click", closeLightbox);
  backdrop.addEventListener("click", closeLightbox);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeLightbox();
  });
});
