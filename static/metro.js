let METRO_DIV = "trackBarBPMContainer";

let metroSketch = function (p) {
  let metroSound;
  let gnome;
  let canvas;
  let inputBPM;
  let metroPlay;
  let showBPM;
  let showSlider;
  let metroSoundTimer = 0;

  const SIZE_X = 50;
  const SIZE_Y = 50;

  let timeouts = [];
  let isPlaying = false;

  p.preload = function () {
    metroSound = p.loadSound("./static/assets/metronome/metro.wav");

    // Load gnome animation frames
    window.animations = [];
    for (let i = 1; i <= 8; i++) {
      let num = i.toString().padStart(3, "0");
      window.animations.push(p.loadImage(`./static/assets/metronome/gnome/gnome${num}.png`));
    }
  };

  p.setup = function () {
    let div = document.getElementById(METRO_DIV);

    canvas = p.createCanvas(SIZE_X, SIZE_Y);
    canvas.id("metroImg");
    canvas.parent(div);

    gnome = new Gnome(p, SIZE_X / 2, SIZE_Y / 2, 50);

    inputBPM = p.createSlider(240, 600, 240, 4);
    inputBPM.size(100);
    inputBPM.input(inputHandler);
    inputBPM.id("metroSlider");
    inputBPM.parent(div);

    metroPlay = p.createButton("Play");
    metroPlay.mousePressed(toggle);
    metroPlay.id("metroPlay");
    metroPlay.parent(div);

    showSlider = p.createSpan();
    showSlider.id("metroSliderCount");
    showSlider.parent(div);
    showSlider.html("Slider: 60");

    showBPM = p.createSpan();
    showBPM.id("metroBPM");
    showBPM.parent(div);

    timeouts.push(setTimeout(changeBPM, 750));
  };

  p.draw = function () {
    p.clear();
    if (gnome) gnome.display();
  };

  function inputHandler() {
    metroSound.stop();

    for (let i = 0; i < timeouts.length; i++) {
      clearTimeout(timeouts[i]);
    }
    timeouts = [];

    showSlider.html(`Slider: ${inputBPM.value() / 4}`);
    showBPM.html("Changing BPM");

    timeouts.push(setTimeout(changeBPM, 750));
  }

  function changeBPM() {
    showBPM.html(parseInt(inputBPM.value() / 4));
    if (isPlaying) {
      play(parseInt(inputBPM.value()));
    }
  }

  function toggle() {
    for (let i = 0; i < timeouts.length; ++i) {
      clearTimeout(timeouts[i]);
    }
    timeouts = [];

    if (metroPlay.html() === "Play") {
      metroPlay.html("Pause");
      isPlaying = true;
    } else {
      metroPlay.html("Play");
      isPlaying = false;
    }

    play(inputBPM.value());
  }

  function play(BPM) {
    if (isPlaying && showBPM.html() !== "Changing BPM") {
      metroSoundTimer++;
      if (metroSoundTimer % 4 === 0) {
        metroSound.play();
      }

      document.dispatchEvent(new CustomEvent("toggleNotes"));

      fetch("/metronome")
        .then((response) => response.json())
        .then((data) => {
          // console.log(data.currentNote);
        });

      let timeoutID = setTimeout(() => play(BPM), 60000 / BPM);
      timeouts.push(timeoutID);
    } else {
      for (let id of timeouts) clearTimeout(id);
      timeouts = [];
      metroSound.stop();
    }
  }

  document.addEventListener("toggleAction", (e) => {
    if (metroPlay.html() === "Play") toggle();

    if (inputBPM.elt.disabled) {
      inputBPM.removeAttribute("disabled");
    } else {
      inputBPM.attribute("disabled", "true");
    }

    let span = document.getElementsByClassName("trackRecordType")[0];
    fetch("/grabRecording")
      .then((response) => response.json())
      .then((data) => {
        if (data.recording) {
          fetch("/grabInputType")
            .then((response) => response.json())
            .then((data) => {
              if (data.state === 1) {
                span.innerHTML = "Inputting notes";
              } else if (data.state === 2) {
                span.innerHTML = "Inputting rests";
              }
            });
        } else {
          span.innerHTML = "";
        }
      });
  });

  class Gnome {
    constructor(p, x, y, size = 50) {
      this.p = p;
      this.x = x;
      this.y = y;
      this.size = size;
      this.frames = window.animations;
      this.frameTimer = 100;
      this.lastFrameIndex = 0;
    }

    display() {
      if (!this.frames || this.frames.length === 0) return;

      if (isPlaying) {
        this.lastFrameIndex = Math.floor(this.p.millis() / this.frameTimer) % this.frames.length;
      }

      const img = this.frames[this.lastFrameIndex];

      this.p.push();
      this.p.translate(this.x, this.y);
      this.p.imageMode(this.p.CENTER);
      this.p.image(img, 0, 0, this.size, this.size);
      this.p.pop();
    }
  }
};

new p5(metroSketch, METRO_DIV);
