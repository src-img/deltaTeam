let metroSound;
let metroGraphic;
let canvas;
let inputBPM;
let metroPlay;
let showBPM;

const SIZE_X = 50;
const SIZE_Y = 50;

let timeouts = [];

function preload(){
  metroSound = loadSound("metro.wav");
  metroGraphic = loadImage("metroLogo.png");
}

function setup() {
  canvas = createCanvas(SIZE_X, SIZE_Y);
  canvas.id("metroImg");
  
  image(metroGraphic, 0, 0, SIZE_X, SIZE_Y); //applied to canvas element
  
  inputBPM = createSlider(1, 218);
  inputBPM.position(50, 10);
  inputBPM.size(100);
  inputBPM.input(inputHandler);
  inputBPM.id("metroSlider");
  
  metroPlay = createButton("Play");
  metroPlay.mousePressed(toggle);
  metroPlay.position(190, 10);
  metroPlay.id("metroPlay");
  
  showSlider = createP("60");
  showSlider.position(155, -5);
  showSlider.id("metroSliderCount");
  
  showBPM = createP("60 BPM");
  showBPM.position(50, 20);
  showBPM.id("metroBPM");
}

function inputHandler(){
  metroSound.stop();
  
  for(let i = 0; i < timeouts.length; i++){
    clearTimeout(timeouts[i]);
  }
  
  timeouts.splice(0, timeouts.length);
  
  showSlider.html(inputBPM.value());
  showBPM.html("Changing BPM");
  
  timeouts.push(setTimeout(changeBPM, 750));
}

function changeBPM(){
  showBPM.html(inputBPM.value() + " BPM");
  
  if(metroPlay.html() == "Pause"){
    play(inputBPM.value());
  } 
}

function toggle(){
  if(metroPlay.html() == "Play"){
    metroPlay.html("Pause");
  } else {
    metroPlay.html("Play");
  }
  
  play(inputBPM.value());
}

function play(BPM){  
  if(metroPlay.html() == "Pause" && showBPM.html() != "Changing BPM"){
    metroSound.play();
    timeoutID = setTimeout(() => play(BPM), 60000/BPM);
    timeouts.push(timeoutID);
  } else {
    clearTimeout(timeoutID);
    metroSound.stop();
  }
  
  if(BPM != inputBPM.value()){
    clearTimeout(timeoutID);
    metroSound.stop();
  }
}