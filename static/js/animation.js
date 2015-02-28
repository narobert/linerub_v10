var currPosRight = 1200;
var currPosTop = 100;
var currPosLeft = 300;
var currPosBottom = 100;
var currPosRotate = 0;
var bird = document.getElementById("bird");
var fire = document.getElementById("fire");
var smoke1 = document.getElementById("smoke1");
var smoke2 = document.getElementById("smoke2");
var smoke3 = document.getElementById("smoke3");
var frantic1 = document.getElementById("frantic1");
var frantic2 = document.getElementById("frantic2");
var frantic3 = document.getElementById("frantic3");
var frantic4 = document.getElementById("frantic4");
var frantic5 = document.getElementById("frantic5");
var frantic6 = document.getElementById("frantic6");

function animateBird() {

    currPosRight -= 0.7;

    bird.style.left = currPosRight + "px";

    if (currPosRight < 840) {
        $("#frantic1").fadeTo("fast", 0.8);
        $("#frantic2").fadeTo("fast", 0.8);
        $("#frantic3").fadeTo("fast", 0.8);
        $("#frantic4").fadeTo("fast", 0.8);
        $("#frantic5").fadeTo("fast", 0.8);
        $("#frantic6").fadeTo("fast", 0.8);
        $("#frantic1").fadeOut("fast");
        $("#frantic2").fadeOut("fast");
        $("#frantic3").fadeOut("fast");
        $("#frantic4").fadeOut("fast");
        $("#frantic5").fadeOut("fast");
        $("#frantic6").fadeOut("fast");
        currPosRight = 840;
        setTimeout(function() {saveShip()}, 600);
        return;
    }
 
    window.requestAnimationFrame(animateBird);
}
window.requestAnimationFrame(animateBird);


function saveShip() {

    currPosRight -= 10;

    bird.style.left = currPosRight + "px";

    if (currPosRight < 270) {
        currPosRight = 270;
        turnShip();
        return;
    }
 
    window.requestAnimationFrame(saveShip);
}


function turnShip() {

    currPosLeft -= 10;
    currPosTop += 15;
    currPosRotate -= 10;

    bird.style.transform = "rotate(" + currPosRotate + "deg)";
 
    bird.style.left = currPosLeft + "px";
    bird.style.top = currPosTop + "px";

    if (currPosLeft < 150) {
        currPosLeft = 150;
        backwardShip();
        return;
    }
 
    window.requestAnimationFrame(turnShip);

}


function backwardShip() {

    currPosLeft += 10;
    currPosTop += 10;
    currPosRotate -= 3;

    bird.style.transform = "rotate(" + currPosRotate + "deg)";
 
    bird.style.left = currPosLeft + "px";
    bird.style.top = currPosTop + "px";

    if (currPosTop > 430) {
        currPosTop = 430;
        saveFire();
        return;
    }
 
    window.requestAnimationFrame(backwardShip);
}


function saveFire() {

    currPosLeft += 10;
 
    bird.style.left = currPosLeft + "px";

    if (currPosLeft > 700) {
        currPosLeft = 700;
        $("#fire").fadeOut("fast");
        $("#smoke1").fadeOut("fast");
        $("#smoke2").fadeOut("fast");
        $("#smoke3").fadeOut("fast");
        setTimeout(function() {flyAway()}, 600);
        return;
    }
 
    window.requestAnimationFrame(saveFire);
}


function flyAway() {

    currPosLeft += 8;

    bird.style.left = currPosLeft + "px";

    if (currPosLeft > 1200) {
        currPosLeft = 1200;
    }
 
    window.requestAnimationFrame(flyAway);
}


var trees = [];

var counter = 0;
var counted = 0;

document.addEventListener("DOMContentLoaded", function() {

    function Tree(element, xPos, yPos, width, height) {

        this.element = element;
        this.xPos = xPos;
        this.yPos = yPos;
        this.width = width;
        this.height = height;

    }

    Tree.prototype.grow = function () {

        this.width += 0.05;
        this.height += 0.05;

        var width = this.width + "px";
        var height = this.height + "px";
        this.element.style.width = width;
        this.element.style.height = height;
    
        if (this.height > 55) {
            this.height = 55;
            counted++;

            if (counted > 3000) {
                fire.style.opacity = 0.8;
            }
            if (counted > 4000) {
                smoke1.style.opacity = 0.8;
            }
            if (counted > 5000) {
                smoke2.style.opacity = 0.8;
            }
            if (counted > 6000) {
                smoke3.style.opacity = 0.8;
            }
        }
        if (this.width > 40) {
            this.width = 40;
        }
    }

    Tree.prototype.shrink = function () {

        this.width -= 0.05;
        this.height -= 0.05;

        var width = this.width + "px";
        var height = this.height + "px";
        this.element.style.width = width;
        this.element.style.height = height;
    
        if (this.height < 45) {
            this.height = 45;
        }
        if (this.width < 30) {
            this.width = 30;
        }
    }

    Tree.prototype.update = function () {

        this.xPos += 0;
        this.yPos -= 4;

        var val = "translate(" + Math.round(this.xPos) + "px, " + Math.round(this.yPos) + "px)";
        this.element.style.transform = val;
        this.element.style.webkitTransform = val;
        this.element.style.mozTransform = val;
        this.element.style.oTransform = val;
    
        if (this.yPos < 510) {
    	    this.yPos = 510;
            counter++;

            if (counter > 1000) {
                for (var i = 0; i < trees.length; i=i+2) {
                    var tree = trees[i];
                    tree.grow();
                }
                for (var i = 1; i < trees.length; i=i+2) {
                    var tree = trees[i];
                    tree.shrink();
                }
            }
        }
    }

    function generateTrees() {
	
        var originalTree = document.querySelector("#tree");
        var treeContainer = document.querySelector(".treeBox");
	        
        for (var i = 0; i < 12; i++) {
    
            var clone = originalTree.cloneNode(true);
            treeContainer.appendChild(clone);

            var initialXPos = 330 + i*50;
            var initialYPos = 1400 + i*50;
            var initialWidth = 35;
            var initialHeight = 50;
        
            var treeObject = new Tree(clone, initialXPos, initialYPos, initialWidth, initialHeight);
            trees.push(treeObject);
        }
    
        treeContainer.removeChild(originalTree);
	
        moveTrees();
    }

    function moveTrees() {
        for (var i = 0; i < trees.length; i++) {
            var tree = trees[i];
            tree.update();
        }
    
        window.requestAnimationFrame(moveTrees);
    }

    generateTrees();

});
