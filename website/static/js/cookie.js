const cookieAllowBtn = document.getElementById("cookie-allow");
const cookieDenyBtn = document.getElementById("cookie-deny");
const cookieContainer = document.getElementById("cookie-container");
const cookieFloating = document.getElementById("cookie-floating");

cookieAllowBtn.addEventListener("click", () => {
    toggleBannerFloatingIcon()
    let expiryDate = new Date()
    expiryDate.setMonth(expiryDate.getMonth() + 1);
    document.cookie = `cookie_consent = true; SameSite = Lax; expires=${expiryDate.toUTCString()}`;
    location.reload()
}) 
cookieDenyBtn.addEventListener("click", () => {
    toggleBannerFloatingIcon()
    let expiryDate = new Date()
    expiryDate.setMonth(expiryDate.getMonth() + 1);
    document.cookie = `cookie_consent = false; SameSite = Lax; expires=${expiryDate.toUTCString()}`;
    location.reload()
})
cookieFloating.addEventListener("click", () => {
    toggleBannerFloatingIcon();
})

const toggleBannerFloatingIcon = () => {
    cookieContainer.classList.toggle("d-none");
    cookieFloating.classList.toggle("d-none");
}