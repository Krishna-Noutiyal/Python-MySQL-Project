const body = document.querySelector("body");
sidebar = body.querySelector("nav");
toggle = body.querySelector(".toggle");
searchBtn = body.querySelector(".search-box");
modeSwitch = body.querySelector(".toggle-switch");
modeText = body.querySelector(".mode-text");

toggle.addEventListener("click", () => {
  // If sidebar is closed then stops scrolling
  if (sidebar.classList.contains("close") == true) {
    // If Innder Width of window is greater than 768px
    if (window.innerWidth <= 768) {
      body.style.overflowY = "hidden";
    }
  } else {
    body.style.overflow = "auto";
  }
  sidebar.classList.toggle("close");
});

searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
});

modeSwitch.addEventListener("click", () => {
  body.classList.toggle("dark");

  if (body.classList.contains("dark")) {
    modeText.innerText = "Light mode";
  } else {
    modeText.innerText = "Dark mode";
  }
});
