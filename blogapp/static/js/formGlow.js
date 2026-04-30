// ==========================================
// Global Form Glow Validation
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      let isValid = true;
      const inputs = form.querySelectorAll(".form-control");

      inputs.forEach((input) => {
        input.classList.remove("input-error", "input-valid");

        // Trim value for checking
        const value = input.value.trim();

        // Basic validation: required and not empty
        if (input.hasAttribute("required") && value === "") {
          input.classList.add("input-error");
          isValid = false;
          return;
        }

        // Number validation (if numeric input)
        if (input.type === "number") {
          const min = input.min ? parseFloat(input.min) : -Infinity;
          const max = input.max ? parseFloat(input.max) : Infinity;
          const num = parseFloat(value);
          if (isNaN(num) || num < min || num > max) {
            input.classList.add("input-error");
            isValid = false;
            return;
          }
        }

        // Textarea length check (if minlength defined)
        if (input.tagName === "TEXTAREA" && input.minLength > 0 && value.length < input.minLength) {
          input.classList.add("input-error");
          isValid = false;
          return;
        }

        // If passed all checks, mark valid
        input.classList.add("input-valid");
      });

      if (!isValid) {
        e.preventDefault();
      }
    });

    // Live feedback on input
    const inputs = form.querySelectorAll(".form-control");
    inputs.forEach((input) => {
      input.addEventListener("input", () => {
        input.classList.remove("input-error", "input-valid");
        const value = input.value.trim();

        if (input.type === "number") {
          const min = input.min ? parseFloat(input.min) : -Infinity;
          const max = input.max ? parseFloat(input.max) : Infinity;
          const num = parseFloat(value);
          if (!isNaN(num) && num >= min && num <= max) {
            input.classList.add("input-valid");
          } else if (value !== "") {
            input.classList.add("input-error");
          }
        } else if (value !== "") {
          input.classList.add("input-valid");
        }
      });
    });
  });
});
