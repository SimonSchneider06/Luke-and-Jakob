// get all Icons from the FAQ Menu

let faqHeadingList = document.getElementsByClassName("faq-heading");
let faqTextList = document.getElementsByClassName("faq-text");

const areSiblings = (elm1, elm2) => 
  elm1 != elm2 && elm1.parentNode == elm2.parentNode;

// add eventListener to each of them
for(let faqHeading of faqHeadingList){

    //loop through all faqTextItems
    for(let faqTextItem of faqTextList){

        // if faqHeading is sibling element to textbox
        // add eventlistener
        if(areSiblings(faqHeading,faqTextItem)){
            faqHeading.addEventListener("click", () => {
                //change depending on eventclick
                toggleIcon(faqHeading);
                toggleVisibility(faqTextItem, "flex");
            })
        }
    }
    
}



/**
*   Toggles the visibility of a HTML Element
*   
* @param {Element} element - the HTML Element which visibility gets toggled
* @param {String} previousState - the Display value of the HTML element before the
* toggling
* @return {void}
*
*/
const toggleVisibility = (element, previousState) => {
    if(element.style.display == previousState){
        element.style.display = "none";
    }
    else{
        element.style.display = previousState;
    }
}

/**
*   Returns the child of a HTML Element
*   
* @param {Element} element - the HTML Parent Element
* 
* @return {HTMLCollection}
*
*/
const getChildElement = (element) => {
    return element.children
}

/**
*   Toggles the visibility of a the icons
*   
* @param {Element} element - the HTML Element which's children icons get toggled
* 
* @return {void}
*
*/
const toggleIcon = (element) => {
    let children = getChildElement(element);
    let Icons = getChildElement(children[0]);

    if(Icons[0].className == "hidden"){
        Icons[1].className = "hidden";
        Icons[0].className = "visible";
    }
    else{
        Icons[0].className = "hidden";
        Icons[1].className = "visible";
    }
}