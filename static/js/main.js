const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav-links");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  nav.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }));
}
const dateInput = document.querySelector('input[name="date"]');
if (dateInput) {
  const today = new Date();
  const localDate = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0,10);
  dateInput.min = localDate;
}

