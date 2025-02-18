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
  
  fetch('/metronome', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({key: 'value'}),
})
}

function stop() {
   inputBPM.disabled() = false;
}
