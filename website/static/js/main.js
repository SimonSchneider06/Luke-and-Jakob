
// for searchbar 

function openSearch(){
    document.getElementById("myOverlay").style.display = "block";
}
function closeSearch(){
    document.getElementById("myOverlay").style.display = "none";
}

//making the product-imgs bigger on click
const imgs = document.getElementsByClassName("img-3");
let clicked_img = "";

for(let i = 0; i<imgs.length; i++){
    imgs[i].addEventListener("click",() => {
        //open new window with big img in the middle
    })
}