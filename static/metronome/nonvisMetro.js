let inputBPM;
let recordingBPM;

function setup() {
  inputBPM = document.getElementById("metroSlider");
  inputBPM.input(inputHandler);
}

function inputHandler(){
   recordingBPM = inputBPM.value() * 4;
}

function play(){  
   inputBPM.disabled() = true;
}

function stop() {
   inputBPM.disabled() = false;
}
