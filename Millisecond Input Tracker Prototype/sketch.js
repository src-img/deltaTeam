// Program that analyzes the time between two taps
// You can use the keys 'a' and 's' to send inputs

let inputs = [];
let ms;
let hit, result;

function preload() {
  // loading sounds for input
  hit = loadSound('click.wav');
  result = loadSound('pickupCoin.wav');
}

function setup() {
  // silly little customization ᐠ( ᐛ )ᐟ
  createCanvas(400, 400);
  background(255);
  textSize(30);
  noStroke();
}

function draw() {
  // shows the ms from program initialization
  rect(50, 65, 200, 50);
  text(round(performance.now()) + "ms", 55, 100);
}

function keyPressed() {
  if (key == 'a' || key == 's') {
    
    // pushes the input time if there is one element or less
    if (inputs.length <= 1) {
      inputs.push(round(performance.now()));
      if (inputs.length == 1) {
        hit.play();
      }
    }
    // shifts the first element in the array, and pushes in a new one
    else {
      inputs.shift();
      inputs.push(round(performance.now()));
    }
    
    // calculates the difference between the two inputs
    if (inputs.length == 2) {
      ms = inputs[1] - inputs[0];
    }
    
    // if there is a value between the two inputs
    if (ms) {
      background(255);
      text(ms + "ms\nbetween each tap", 50, 200);  
      result.play();
    }
    
    // draws the inputs of the user
    if (inputs[0]) 
      text(inputs[0], 300, 75);
    if (inputs[1])
      text(inputs[1], 300, 125);
    
    // console.log(inputs);
  }
}