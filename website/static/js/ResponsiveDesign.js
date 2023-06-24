export class ResponsiveElementStyle{

    /**
     * @param {*} className apply the behavior to all elements with this className
     * @param {*} cssProperty the css property that gets changed by window resize
     * @param {*} aboveBreakingPointValue styling of elements if windowSize above BreakingPoint
     * @param {*} belowBreakingPointValue styling of elements if windowSize below BreakingPoint
     * @param {*} widthBreakingPoint setting the width, by which the elements change their behavior
     */

    constructor(className, cssProperty, aboveBreakingPointValue, belowBreakingPointValue, widthBreakingPoint){
        this.elements = document.getElementsByClassName(className);
        this.cssProperty = cssProperty;
        this.aboveBreakingPointValue = aboveBreakingPointValue;
        this.belowBreakingPointValue = belowBreakingPointValue;
        this.widthBreakingPoint = widthBreakingPoint;
    }


    /**
     * to be called in window on_resize function
     * changes the styling property by windowWidth
     */
    changeStyle(){
        //checks if elements defined
        if(this.elements){

            console.log("Style-changing")
            //sets the property, otherwise it wouldn't be recognized in code, because of style.this.cssProperty
            let cssProperty = this.cssProperty; 

            //checks breakPoint and assignes value
            // if(window.innerWidth <= this.widthBreakingPoint){
            //     for(let elementNumber in this.elements){
            //         this.elements[elementNumber].style.cssProperty = this.belowBreakingPointValue;
            //     }
            // }

            // else{
            //     for(let elementNumber in this.elements){
            //         this.elements[elementNumber].style.cssProperty = this.aboveBreakingPointValue;
            //     }
            // }
        }
        
    }
}