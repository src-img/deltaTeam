//NOTE: SOUNDS DO NOT WORK AT THE MOMENT (as of 1:49pm 2/18/2025)

const TRACKER_DIV = "trackerContainer";

let trackerSketch = function(p) {
  // Program that analyzes the time between two taps
  // You can use the keys 'a' and 's' to send inputs
  
  let inputs = [];
  let ms;
  let hit, result;
  
  p.preload = function() {
    hit = p.loadSound('https://src-img.github.io/deltaTeam/millisecondTracker/click.wav');
    result = p.loadSound('https://src-img.github.io/deltaTeam/millisecondTracker/pickupCoin.wav');
  }
  
  p.setup = function() {
    // silly little customization ᐠ( ᐛ )ᐟ
    let div = document.getElementById(TRACKER_DIV);

    let canvas = p.createCanvas(400, 400);
    p.background(255);
    canvas.id("inputTrackCanvas");
    canvas.parent(div);

    p.textSize(30);
    p.noStroke();
  }
  
  p.draw = function() {
    // shows the ms from program initialization
    p.rect(50, 65, 200, 50);
    p.text(p.round(performance.now()) + "ms", 55, 100);
  }
  
  p.keyPressed = function() {
    if (p.key == 'a' || p.key == 's') {
      
      // pushes the input time if there is one element or less
      if (inputs.length <= 1) {
        inputs.push(p.round(performance.now()));
        if (inputs.length == 1) {
          hit.play();
        }
      }
      // shifts the first element in the array, and pushes in a new one
      else {
        inputs.shift();
        inputs.push(p.round(performance.now()));
      }
      
      // calculates the difference between the two inputs
      if (inputs.length == 2) {
        ms = inputs[1] - inputs[0];
      }
      
      // if there is a value between the two inputs
      if (ms) {
        p.background(255);
        p.text(ms + "ms\nbetween each tap", 50, 200);  
        result.play();
      }
      
      // draws the inputs of the user
      if (inputs[0]) 
        p.text(inputs[0], 300, 75);
      if (inputs[1])
        p.text(inputs[1], 300, 125);
      
      // console.log(inputs);
    }
  }
}
new p5(trackerSketch, TRACKER_DIV);
