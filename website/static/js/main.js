window.onresize = () => {
    screenwidth = window.innerWidth
    const burgermenuIconOpen1 = document.getElementById("navbar-burgermenu-icon-open-id")
    const burgermenuIconClose1 = document.getElementById("navbar-burgermenu-icon-close-id")
    //on window resize check if class needs to be changed
    if(screenwidth <= 805){
        // align headcontainer items in column
        if(headContainerEl){
            headContainerEl.className = "container-xxl column m-auto mt-3";
        }

        // align all product-containers column
        for(let i = 0; i < productContainerRowELs.length; i++){
            productContainerRowELs[i].className = "column border p-2 m-2 product-container";
        }  
    }
    else{
        // align headcontainer items next to each other
        if(headContainerEl){
            headContainerEl.className = "container-xxl row between big m-auto mt-3";
        }

        // align all product-containers row
        for(let i = 0; i < productContainerRowELs.length; i++){
            productContainerRowELs[i].className = "row border p-2 m-2 product-container";
        } 
    }
    
    
    if (screenwidth > 1000) {
        burgermenuContentId1.style.transition = "none";
        burgermenuContentId2.style.transition = "none";
        burgermenuContentId1.style.transform = "none";
        burgermenuContentId2.style.transform = "none";
        burgermenuIconClose1.style.display = "none";
        burgermenuIconOpen1.style.display = "flex";
        burgermenuopen = false;
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
        burgermenuIconClose1.style.display = "none";
        burgermenuIconOpen1.style.display = "flex";
        burgermenuopen = false;
    }
}

// for searchbar --------------------
// for searchbar and navbar 
const searchbar = document.getElementById("myOverlay")
const burgermenuContent = document.getElementsByClassName("navbar-burgermenu-content")
const burgermenuButton = document.getElementsByClassName("navbar-burgermenu-button")
let burgermenuopen = false
let searchopen = false
let searchwasopen = false
let screenwidth = window.innerWidth
const burgermenuContentId1 = document.getElementById("navbar-burgermenu-content-id1")
const burgermenuContentId2 = document.getElementById("navbar-burgermenu-content-id2")
const searchbarinput = document.getElementById("navbar-overlay-search-input-id")


function openSearch() {
    searchbar.style.display = "flex";
    searchbar.style.transition = "all ease-in-out .2s";
    searchbar.style.transform = "translate(0%, 0px)";
    searchbarinput.focus();
    if (burgermenuopen == true) {
        burgermenuContentId1.style.transition = "all ease-in-out .2s";
        burgermenuContentId2.style.transition = "all ease-in-out .2s";
        burgermenuContentId1.style.marginTop = "66px";
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
    setTimeout(() => { searchbar.style.display = "none";}, 200);
    searchbar.style.transition = "all ease-in-out .2s";
    if (burgermenuopen == false && screenwidth <= 1000) {
        searchbar.style.transition = "none";
    }
    searchbar.style.transform = "translate(0px, -100%)";
    searchbarinput.value = "";
    burgermenuContentId1.style.marginTop = "0px";
    searchwasopen = false;
    searchopen = false;
}
function burgermenu() {
    const burgermenuIconOpen = document.getElementById("navbar-burgermenu-icon-open-id");
    const burgermenuIconClose = document.getElementById("navbar-burgermenu-icon-close-id");
    if (burgermenuopen == false) {
        burgermenuContentId1.style.transition = "all ease-in-out .8s";
        burgermenuContentId2.style.transition = "all ease-in-out .8s";
        burgermenuContentId1.style.transform = "none";
        burgermenuContentId2.style.transform = "none";
        setTimeout(() => { burgermenuIconClose.style.display = "flex"; burgermenuIconOpen.style.display = "none";}, 200);
        burgermenuopen = true;
    }
    else if (burgermenuopen == true) {
        searchbar.style.transition = "all ease-in-out .8s";
        searchbar.style.transform = "translate(-100%, 0px)";
        setTimeout(() => { closeSearch()}, 800);
        burgermenuContentId1.style.transition = "all ease-in-out .8s";
        burgermenuContentId2.style.transition = "all ease-in-out .8s";
        burgermenuContentId1.style.transform = "translate(-100%, 0px)";
        burgermenuContentId2.style.transform = "translate(-100%, 0px)";
        setTimeout(() => { burgermenuIconClose.style.display = "none"; burgermenuIconOpen.style.display = "flex"; }, 200);
        burgermenuopen = false;
    }
}


//shopping cart price box ---------------------

// headcontainer
const headContainerEl = document.getElementById("head-container");

// product rows 
const productContainerRowELs = document.getElementsByClassName("product-container");

// 
// const productImgEls = document.getElementsByClassName("product-img");

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