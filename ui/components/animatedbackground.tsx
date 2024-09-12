import React from "react";
import './Home.module.css'

var waterBG = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/498726/water-back.png";
var waterFG = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/498726/water-front.png";

function verticalParallax(parallaxPanel: any, parallaxPanel2: any, directionY: any, speedY: any, distanceFactor: any, zoomFactor: any, zFactor: any){

	distanceFactor = (distanceFactor) ? distanceFactor:.5;
	zoomFactor = (zoomFactor) ? zoomFactor:1;
	zFactor = (zFactor) ? zFactor:0;

	var parallaxPanelY = Number(parallaxPanel.dataset.y);
	var parallaxPanel2Y = Number(parallaxPanel2.dataset.y);
	var height = Number(parallaxPanel.dataset.height);

	if (directionY === 1){
		parallaxPanelY += speedY*distanceFactor;
		parallaxPanelY = (parallaxPanelY > height) ? 0:parallaxPanelY;
		parallaxPanel2Y = (parallaxPanelY < height) ? parallaxPanelY-height:parallaxPanelY+height;

		parallaxPanel2Y = zoomFactor * parallaxPanel2Y;
		parallaxPanelY = zoomFactor * parallaxPanelY;
	}else{
		parallaxPanelY = parallaxPanelY - (speedY*distanceFactor);
		parallaxPanelY = (parallaxPanelY < height && parallaxPanelY > (-1*height)) ? parallaxPanelY:0;
		parallaxPanel2Y = (parallaxPanelY > (-1*height)) ? parallaxPanelY+height:parallaxPanelY-height;

		parallaxPanel2Y = zoomFactor * parallaxPanel2Y;
		parallaxPanelY = zoomFactor * parallaxPanelY;
	}

	parallaxPanel.dataset.y = parallaxPanelY;
	parallaxPanel2.dataset.y = parallaxPanel2Y;

	parallaxPanel.style[ cssPrefix.cssTransform ] = "translate3d(0px, " + parallaxPanelY + "px, " + zFactor + "px) scale(" + zoomFactor + ")";
	parallaxPanel2.style[ cssPrefix.cssTransform ] = "translate3d(0px, " + parallaxPanel2Y + "px, " + zFactor + "px) scale(" + zoomFactor + ")";

}


function horizontalParallax(parallaxPanel: any, parallaxPanel2: any, directionX: any, speedX: any, distanceFactor: any, zoomFactor: any, zFactor: any){

	distanceFactor = (distanceFactor) ? distanceFactor:.5;
	zoomFactor = (zoomFactor) ? zoomFactor:1;
	zFactor = (zFactor) ? zFactor:0;

	var parallaxPanelX = Number(parallaxPanel.dataset.x);
	var parallaxPanel2X = Number(parallaxPanel2.dataset.x);
	var width = Number(parallaxPanel.dataset.width);

	if (directionX === 1){
		parallaxPanelX += speedX*distanceFactor;
		parallaxPanelX = (parallaxPanelX > width) ? 0:parallaxPanelX;
		parallaxPanel2X = (parallaxPanelX < width) ? parallaxPanelX-width:parallaxPanelX+width;

		parallaxPanel2X = zoomFactor * parallaxPanel2X;
		parallaxPanelX = zoomFactor * parallaxPanelX;
	}else{
		parallaxPanelX = parallaxPanelX - (speedX*distanceFactor);
		parallaxPanelX = (parallaxPanelX < width && parallaxPanelX > (-1*width)) ? parallaxPanelX:0;
		parallaxPanel2X = (parallaxPanelX > (-1*width)) ? parallaxPanelX+width:parallaxPanelX-width;

		parallaxPanel2X = zoomFactor * parallaxPanel2X;
		parallaxPanelX = zoomFactor * parallaxPanelX;
	}

	parallaxPanel.dataset.x = parallaxPanelX;
	parallaxPanel2.dataset.x = parallaxPanel2X;

	parallaxPanel.style[ cssPrefix.cssTransform ]  = "translate3d("+parallaxPanelX+"px, 0px, " + zFactor + "px) scale(" + zoomFactor + ")";
	parallaxPanel2.style[ cssPrefix.cssTransform ] = "translate3d("+parallaxPanel2X+"px, 0px, " + zFactor + "px) scale(" + zoomFactor + ")";

}

function update(){
	// use one of the two approaches to manage the parallax scrolling

	// 1 - HORIZONTAL
	// horizontalParallax(bg1, bg2, -1, 10, .5);
	// horizontalParallax(fg1, fg2, -1, 10, 1);

	// OR

	// 2 - VERTICAL
	verticalParallax(bg1, bg2, 1, 5, .15);
	verticalParallax(fg1, fg2, 1, 5, .25);

  window.requestAnimationFrame(update);
}

function parallaxLayer(imageURL: any, width: any, height: any, x: any, y: any, className: any){

	var parallax = document.createElement("div");

	parallax.dataset.x = x;
	parallax.dataset.y = y;
	//parallax.dataset.width = width;
  parallax.dataset.height = height;
	parallax.className = (className) ? className : "";
	parallax.style.background = "url(" + imageURL + ")";
	parallax.style.width = width + "px";
	parallax.style.height = height + "px";
	// parallax.style.backgroundSize = width + "px " + height + "px";
	parallax.style.position = "absolute";
	// parallax.style.display = "block";
	parallax.style[cssPrefix.cssTransform + "Origin"] = "0px 0px";

      var container = document.getElementById("main");
	container.appendChild(parallax);

	return parallax;
}

var fg1;
var fg2;
var bg1;
var bg2;

function prepareExample() {

    // background layer
	bg1 = parallaxLayer(waterBG, 640, 480, 0, 0, "parallax");
	bg2 = parallaxLayer(waterBG, 640, 480, 0, 0, "parallax");

	// foreground layer
	fg1 = parallaxLayer(waterFG, 640, 480, 0, 0, "");
	fg2 = parallaxLayer(waterFG, 640, 480, 0, 0, "");

  window.requestAnimationFrame(update);
}

// on load
window.addEventListener("load", function load(event){
    window.removeEventListener("load", load, false); //remove listener, no longer needed
  prepareExample();
},false);