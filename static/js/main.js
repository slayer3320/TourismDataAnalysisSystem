// Filter Functionality
document.addEventListener("DOMContentLoaded", function () {
  // Toggle filters
  const toggleBtn = document.querySelector(".toggle-filters");
  const filterForm = document.querySelector(".filter-form");

  if (toggleBtn && filterForm) {
    toggleBtn.addEventListener("click", function () {
      filterForm.classList.toggle("collapsed");
      const icon = this.querySelector("i");
      icon.classList.toggle("bi-chevron-down");
      icon.classList.toggle("bi-chevron-up");
    });

    // Start with filters collapsed on mobile
    if (window.innerWidth < 768) {
      filterForm.classList.add("collapsed");
    }
  }

  // 价格输入验证
  const minPriceInput = document.getElementById("min_price");
  const maxPriceInput = document.getElementById("max_price");

  if (minPriceInput && maxPriceInput) {
    minPriceInput.addEventListener("change", function () {
      if (parseInt(this.value) > parseInt(maxPriceInput.value)) {
        this.value = maxPriceInput.value;
      }
    });

    maxPriceInput.addEventListener("change", function () {
      if (parseInt(this.value) < parseInt(minPriceInput.value)) {
        this.value = minPriceInput.value;
      }
    });
  }

  // Close alert button
  document.querySelectorAll(".alert .btn-close").forEach((btn) => {
    btn.addEventListener("click", function () {
      this.closest(".alert").remove();
    });
  });
});
