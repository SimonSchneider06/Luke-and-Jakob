const cookieAllowBtn = document.getElementById("cookie-allow");
const cookieDenyBtn = document.getElementById("cookie-deny");
const cookieContainer = document.getElementById("cookie-container");
const cookieFloating = document.getElementById("cookie-floating");

cookieAllowBtn.addEventListener("click", () => {
    toggleBannerFloatingIcon()
    document.cookie = "cookie_consent = true; SameSite = Lax";
    location.reload()
}) 
cookieDenyBtn.addEventListener("click", () => {
    toggleBannerFloatingIcon()
    document.cookie = "cookie_consent = false; SameSite = Lax";
    location.reload()
})
cookieFloating.addEventListener("click", () => {
    toggleBannerFloatingIcon();
})

const toggleBannerFloatingIcon = () => {
    cookieContainer.classList.toggle("d-none");
    cookieFloating.classList.toggle("d-none");
}