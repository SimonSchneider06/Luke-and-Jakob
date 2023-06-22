import {ResponsiveDesign} from "./ResponsiveDesign";

window.onresize = () => {
    productContainerRow.changeClassName();
    //on window resize check if class needs to be changed
    if(window.innerWidth <= 805){
        // align headcontainer items in column
        headContainerEl.className = "container-xxl column m-auto mt-3";

        // align all product-containers column
        // for(let i = 0; i < productContainerRowELs.length; i++){
        //     productContainerRowELs[i].className = "column border p-2 m-2 product-container";
        // }  
    }
    else{
        // align headcontainer items next to each other
        headContainerEl.className = "container-xxl row between big m-auto mt-3";

        // align all product-containers row
        // for(let i = 0; i < productContainerRowELs.length; i++){
        //     productContainerRowELs[i].className = "row border p-2 m-2 product-container";
        // } 
    }
}

//shopping cart price box ---------------------

// headcontainer
const headContainerEl = document.getElementById("head-container");

// product rows 
//const productContainerRowELs = document.getElementsByClassName("product-container");

productContainerRow = ResponsiveDesign("column border p-2 m-2 product-container","row border p-2 m-2 product-container",805);

// 
// const productImgEls = document.getElementsByClassName("product-img");

// for searchbar --------------------

function openSearch(){
    document.getElementById("myOverlay").style.display = "block";
}
function closeSearch(){
    document.getElementById("myOverlay").style.display = "none";
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