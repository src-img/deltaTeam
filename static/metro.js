let METRO_DIV = "trackBarBPMContainer";

let metroSketch = function(p) {
  let metroSound;
  let metroGraphic;
  let canvas;
  let inputBPM;
  let metroPlay;
  let showBPM;
  let metroSoundTimer = 0;

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

      p.image(metroGraphic, 0, 0, SIZE_X, SIZE_Y); // Applied to canvas element

      inputBPM = p.createSlider(240, 600, 240, 4);
      //inputBPM.position(50, 280);
      inputBPM.size(100);
      inputBPM.input(inputHandler);
      inputBPM.id("metroSlider");
      inputBPM.parent(div);

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
      //fixxes bug of refreshing while playing
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
      if(metroSoundTimer % 4 == 0){
          metroSound.play();
      }

      const toggleNoteDisplayEvent = new CustomEvent('toggleNotes', {detail:{}});
      document.dispatchEvent(toggleNoteDisplayEvent);
        
      fetch('/metronome')
      .then(response => response.json())
      .then(data => {
        //console.log(data.currentNote);
      });
        
      timeoutID = setTimeout(() => play(BPM), 60000 / BPM);
      timeouts.push(timeoutID);
    } else {
      clearTimeout(timeoutID);
      metroSound.stop();
    }

    if (BPM != inputBPM.value()) {
      clearTimeout(timeoutID);
      metroSound.stop();
    }
  }

  document.addEventListener('toggleAction', (e) => {
    if(metroPlay.html() == "Play") toggle();
    if(inputBPM.elt.disabled){
        inputBPM.removeAttribute('disabled');
    } else {
        inputBPM.attribute('disabled', 'true');
    }

    let span = document.getElementsByClassName("trackRecordType")[0];
    fetch('/grabRecording')
        .then(response => response.json())
        .then(data => {
            if(data.recording){
                fetch('/grabInputType')
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.state);
                        if(data.state === 1){
                            span.innerHTML = "Inputting notes";
                        } else if (data.state === 2){
                            span.innerHTML = "Inputting rests";
                        }
                    });
            } else {
                span.innerHTML = "";
            }
        });
  });
};

// Attach this sketch to the "metroContainer" div
new p5(metroSketch, METRO_DIV);
