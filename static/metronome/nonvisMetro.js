let inputBPM;
let recordingBPM;

function setup() {
  inputBPM = document.getElementById("metroSlider");
  inputBPM.input(inputHandler);
}

function inputHandler(){
   recordingBPM = inputBPM.value() * 4; 
  //fetch from here or from play()?
}

function play(){  
   inputBPM.disabled() = true;
  //fetch from here or from inputHandler()?
}

function stop() {
   inputBPM.disabled() = false;
}
