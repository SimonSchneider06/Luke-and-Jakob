
// for searchbar 
const searchbar = document.getElementById("myOverlay")
const burgermenuContent = document.getElementsByClassName("navbar-burgermenu-content")
const burgermenuButton = document.getElementsByClassName("navbar-burgermenu-button")
let burgermenuopen = false
let searchopen = false
let searchwasopen = false
let screenwidth = window.innerWidth
const burgermenuContentId1 = document.getElementById("navbar-burgermenu-content-id1")
const burgermenuContentId2 = document.getElementById("navbar-burgermenu-content-id2")


function openSearch() {
    searchbar.style.display = "flex";
    if (burgermenuopen == true) {
        burgermenuContentId1.style.transition = "none";
        burgermenuContentId2.style.transition = "none";
        burgermenuContentId1.style.marginTop = "94px";
        searchbar.style.backgroundColor = "black";
    }
    if (screenwidth <= 1000) {
        searchwasopen = true;
    }
    if (searchopen == true) {
        closeSearch();

    }
    else {
        searchopen = true;
    }
}
function closeSearch() {
    searchbar.style.display = "none";
    burgermenuContentId1.style.marginTop = "0px";
    searchwasopen = false;
    searchopen = false;
}
function burgermenu() {
    if (burgermenuopen == false) {
        burgermenuContentId1.style.transition = "all ease-in-out .5s";
        burgermenuContentId2.style.transition = "all ease-in-out .5s";
        burgermenuContentId1.style.transform = "none";
        burgermenuContentId2.style.transform = "none";
        burgermenuopen = true;
    }
    else if (burgermenuopen == true) {
        closeSearch();
        burgermenuContentId1.style.transition = "all ease-in-out .5s";
        burgermenuContentId2.style.transition = "all ease-in-out .5s";
        burgermenuContentId1.style.transform = "translate(-100%, 0px)";
        burgermenuContentId2.style.transform = "translate(-100%, 0px)";
        burgermenuopen = false;
    }
}
window.addEventListener("resize", onresize)
function onresize() {
    screenwidth = window.innerWidth
    if (screenwidth > 1000) {
        burgermenuContentId1.style.transition = "none";
        burgermenuContentId2.style.transition = "none";
        burgermenuContentId1.style.transform = "none";
        burgermenuContentId2.style.transform = "none";
        burgermenuopen = false;
        searchbar.style.backgroundColor = "initial";
        if (searchwasopen == true) {
            closeSearch();
        }
    }
    if (screenwidth <= 1000 && burgermenuopen == false) {
        if (searchopen == true) {
            closeSearch();
            searchopen = false;
        }
        burgermenuContentId1.style.transition = "none";
        burgermenuContentId2.style.transition = "none";
        burgermenuContentId1.style.transform = "translate(-100%, 0px)";
        burgermenuContentId2.style.transform = "translate(-100%, 0px)";
        burgermenuopen = false;
    }
}


//making the product-imgs bigger on click-----------------------

// getting the html elements
const imgHolderEl = document.getElementById("pop-up-div");
const popUpImg = document.getElementById("pop-up-img");
const imgs = document.getElementsByClassName("img-4"); //list of all imgs

//ads event to every img in imgs
for(let i = 0; i<imgs.length; i++){
    imgs[i].addEventListener("click",() => {

        //make pop-up-img visible
        imgHolderEl.style.display = "flex";
        let path = imgs[i].src;
        popUpImg.src = path;
        if(window.innerHeight > window.innerWidth){
            popUpImg.style.width = "70vw";
        }
        else{
            popUpImg.style.height = "70vh";
        }
    })
}

//selecting the pop-up-close el
const popUpCloseBtn = document.getElementById("pop-up-close");

//adding event to close imgHolderEl
popUpCloseBtn.addEventListener("click",() => {
    imgHolderEl.style.display = "none";
})