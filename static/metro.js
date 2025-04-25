let METRO_DIV = "trackBarBPMContainer";

let metroSketch = function(p) {
  const InputState = {
    addNote: 1,
    addRest: 2,
    noInput: 3
  };

  let metroSound;
  let metroGraphic;
  let canvas;
  let inputBPM;
  let metroPlay;
  let showBPM;
  let metroSoundTimer = 0;
  let record = false;
  let userInput = InputState.addRest;
  let lastUserInput = InputState.addRest; //holds input state of last key press
  let fourCount;
  let timeoutID;
  let timeoutFetch;

  const SIZE_X = 50;
  const SIZE_Y = 50;

  let timeouts = [];

  p.preload = function() {
      metroSound = p.loadSound("./static/assets/metronome/metro.wav");
      metroGraphic = p.loadImage("./static/assets/metronome/metroLogo.png");
  };

  p.setup = function() {
      let div = document.getElementById(METRO_DIV);

      canvas = p.createCanvas(SIZE_X, SIZE_Y);
      canvas.id("metroImg");
      canvas.parent(div);

     // p.image(metroGraphic, 0, 0, SIZE_X, SIZE_Y); // Applied to canvas element
      
      inputBPM = p.createSlider(240, 600, 240, 4);
      //inputBPM.position(50, 280);
      inputBPM.size(100);
      inputBPM.input(inputHandler);
      inputBPM.id("metroSlider");
      inputBPM.parent(div);
    
      window.getCurrentBPM = () => parseInt(inputBPM.value() / 4);
     
      muteButton = p.createButton("Mute");
      muteButton.id("metroMute");
      muteButton.parent(div);
      muteButton.mousePressed(() => {
        if(muteButton.html() == "Mute"){
          muteButton.html("Unmute");
          metroSound.setVolume(0);
        } else if (muteButton.html() == "Unmute"){
          muteButton.html("Mute");
          metroSound.setVolume(1);
        }
      })

      metroPlay = p.createButton("Play");
      metroPlay.mousePressed(toggle);
      //metroPlay.position(185, 270);
      metroPlay.id("metroPlay");
      metroPlay.parent(div);

      showSlider = p.createSpan();// these are from when metronome had 2 readouts... don't feel like chasing it down, but normal readdout cant function w/o showslider, so  here we are
      //showSlider.position(153, 265);
      showSlider.id("metroSliderCount");
      showSlider.parent(div);
      showSlider.html("Slider: 60");

      showBPM = p.createSpan();
      //showBPM.position(50, 285);
      showBPM.id("metroBPM");
      showBPM.parent(div);
      timeouts.push(setTimeout(changeBPM, 750)); //have it say the inital bpm
  };

  function inputHandler() {
      metroSound.stop();

      for (let i = 0; i < timeouts.length; i++) {
          clearTimeout(timeouts[i]);
      }

      timeouts.splice(0, timeouts.length);

      showSlider.html(`Slider: ${inputBPM.value() / 4}`);
      showBPM.html("Changing BPM");

      timeouts.push(setTimeout(changeBPM, 750));
  }

  function changeBPM() {
      showBPM.html(parseInt(inputBPM.value() / 4)/* + " BPM"*/);    // temporary fix until the bpm can be pulled correctly into playback.

      if (metroPlay.html() == "Pause") {
          play(parseInt(inputBPM.value()));
      }
  }

  function toggle() {
    if (metroPlay.html() == "Play") {
      //fixes bug of refreshing while playing
        for(let i = 0; i < timeouts.length; ++i){
          clearTimeout(timeouts[i]);
        }
        timeouts = [];

        metroPlay.html("Pause");
    } else {
        metroPlay.html("Play");
    }
    play(inputBPM.value());
  }

  function play(BPM) {
    if (metroPlay.html() == "Pause" && showBPM.html() != "Changing BPM") {
      metroSoundTimer++;
      if(metroSoundTimer == 4){
          metroSound.play();
          metroSoundTimer = 0;
          if (window.metrognome) {
            window.metrognome.nextBeat();
          }
          
          console.log("metronome hit", metroSoundTimer, Date.now())
      }
  
      if(record && fourCount != 0){
        fourCount--;
        console.log("fourCount:", fourCount, "metroSoundTimer:", metroSoundTimer)
      }

      timeoutID = setTimeout(() => play(BPM), 60000 / BPM);
      timeouts.push(timeoutID);
      timeoutFetch = setTimeout(() => sendInput(), 100);
      timeouts.push(timeoutFetch)
      
    } else {
      clearTimeout(timeoutID);
      clearTimeout(timeoutFetch);
      metroSound.stop();

      if (window.metrognome) {
        window.metrognome.setIdle();
      }
    }

    if (BPM != inputBPM.value()) {
      clearTimeout(timeoutID);
      clearTimeout(timeoutFetch);
      metroSound.stop();
    }
  }
  

  function sendInput() {
    if(fourCount == 0){
      console.log("fetchnow for metrosSoundTimer ", metroSoundTimer, Date.now())
      fetch('/metronome', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'userInput': userInput, 'record': record})
      })
      .then(() => {
        const toggleNoteDisplayEvent = new CustomEvent('toggleNotes', {detail:{}});
        document.dispatchEvent(toggleNoteDisplayEvent);
      });

      userInput = InputState.noInput;        
    }
  }

  document.addEventListener('keydown', (e) => {
    console.log("metroSoundTimer, keyboardpress milliseconds: ", metroSoundTimer, Date.now())
    const key = e.key;
    let inputTypeSpan = document.getElementsByClassName("trackRecordType")[0];
    if(key == 'a'){
      userInput = InputState.addNote;
      lastUserInput = userInput;
      if(record) inputTypeSpan.innerHTML = "Inputting notes";
    } else if (key == 's'){
      userInput = InputState.addRest;
      lastUserInput = userInput;
      if(record) inputTypeSpan.innerHTML = "Inputting rests";
    }
  });

  document.addEventListener('toggleAction', () => {
    if((metroPlay.html() == "Play" && !record) || (metroPlay.html() == "Pause" && record)) toggle();
    if(inputBPM.elt.disabled){
        inputBPM.removeAttribute('disabled');
    } else {
        inputBPM.attribute('disabled', 'true');
    }

    if(metroPlay.elt.disabled){
      metroPlay.removeAttribute('disabled');
    } else {
      metroPlay.attribute('disabled', 'true');
    }

    let inputTypeSpan = document.getElementsByClassName("trackRecordType")[0];

    if(!record){
      record = true;
      fourCount = 20 - metroSoundTimer;
      console.log("Record clicked! fourCount", fourCount, "metroSoundTimer:", metroSoundTimer)
      if(lastUserInput == InputState.addNote){
        inputTypeSpan.innerHTML = "Inputting notes"
      } else if (lastUserInput == InputState.addRest){
        inputTypeSpan.innerHTML = "Inputting rests"
      }
      userInput = lastUserInput;
    } else {
      record = false;
      fourCount = 16;
      metroSoundTimer = 0;

      inputTypeSpan.innerHTML = "";

      fetch('/metronome', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'userInput': userInput, 'record': record})
      })
      // .then(response => response.json())
      .then(data => {
        const toggleNoteDisplayEvent = new CustomEvent('toggleNotes', {detail:{}});
        document.dispatchEvent(toggleNoteDisplayEvent);
      });
    }
  });
};

// Attach this sketch to the "metroContainer" div
new p5(metroSketch, METRO_DIV);
