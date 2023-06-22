class ResponsiveDesign{

    /**
     * Switches ClassNames from html elements to make a windowSize responsive web design
     * 
     * @param {*} normalScreenSizeClassName the class name which should be present, when screensize normal, so for laptop for example
     * @param {*} smallScreenSizeClassName the class name which should be present, when screenSize small, so when smartphone screen for example
     * @param {*} windowChangeSize the size(in px) by which the classes should be switched; if windowSize is below that point, small screen should be enabled
     */

    constructor(normalScreenSizeClassName,smallScreenSizeClassName,windowChangeSize){
        this.normalScreenSizeEls = document.getElementsByClassName(normalScreenSizeClassName);
        this.normalScreenSizeClassName = normalScreenSizeClassName;

        this.smallScreenSizeEls = document.getElementsByClassName(smallScreenSizeClassName);
        this.smallScreenSizeClassName = smallScreenSizeClassName;

        this.windowChangeSize = windowChangeSize;
    }

    changeClassName(){
        // small Screen enabled
        if(window.innerWidth <= this.windowChangeSize){
            //loop through all elements with normal screen class and change it to small screen class
            for(let elementNumber = 0; elementNumber < this.normalScreenSizeEls.length; elementNumber ++){
                this.normalScreenSizeEls[elementNumber].className = this.smallScreenSizeClassName;
            }
            console.log("smallScreen");
        }
        else{
            //loop through all elements with small screen class and change it to normal screen class
            for(let elementNumber = 0; elementNumber < this.smallScreenSizeEls.length; elementNumber ++){
                this.smallScreenSizeEls[elementNumber].className = this.normalScreenSizeClassName;
            }
            console.log("normalScreen")
        }
    }
}