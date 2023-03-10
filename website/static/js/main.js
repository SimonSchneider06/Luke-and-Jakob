
// for searchbar 

function openSearch(){
    document.getElementById("myOverlay").style.display = "block";
}
function closeSearch(){
    document.getElementById("myOverlay").style.display = "none";
}

//making the product-imgs bigger on click
const imgHolderEl = document.getElementById("pop-up-div");
const popUpImg = document.getElementById("pop-up-img");
const imgs = document.getElementsByClassName("img-3");
let clicked_img = "";

//ads event to every img in imgs
for(let i = 0; i<imgs.length; i++){
    imgs[i].addEventListener("click",() => {
        //open new window with big img in the middle

        //make pop-up-img visible
        imgHolderEl.style.display = "block";
        let path = imgs[i].src;
        popUpImg.src = path;
    })
}

//selecting the pop-up-close el
const popUpCloseBtn = document.getElementById("pop-up-close");

//adding event to close imgHolderEl
popUpCloseBtn.addEventListener("click",() => {
    imgHolderEl.style.display = "none";
})