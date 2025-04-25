const SKELETON_DIV = "noteSkeletonContainer";

let autoScroll = false;
const observer = new MutationObserver((mutationsList) => {
  // Loop through all mutations to handle them

  mutationsList.forEach((mutation) => {
    // Ensure that the target element exists and is scrollable
    const target = mutation.target;

    if (target && target.scroll && autoScroll) {
      target.parentElement.scrollLeft = target.parentElement.scrollWidth;
    }
  });
});

let skeletonSketch = function (p) {
  let playButton;
  let deleteEnabled = true;

  class track {
    constructor(p5, x, y) {
      this.p = p5;

      this.trackContainer = this.p.createDiv();
      this.trackContainer.class("trackContainer");

      this.x = x;
      this.y = y;

      this.muted = false;
      this.isolated = false;

      //BUTTON CREATION ---------------------------------------------------------------------------------
      this.buttonContainer = this.p.createDiv();
      this.buttonContainer.class("buttonContainer");
      this.buttonContainer.parent(this.trackContainer);

      this.buttonContainerRowA = this.p.createDiv();
      this.buttonContainerRowA.class("buttonContainerRowA buttonContainerRow");
      this.buttonContainerRowA.parent(this.buttonContainer);

      this.nameField = this.p.createInput();
      this.nameField.class("trackName");
      this.nameField.parent(this.buttonContainerRowA);

      this.recordButton = this.p.createButton("-");
      this.recordButton.class("trackRecord");
      this.recordButton.parent(this.buttonContainerRowA);

      // Event listener to turn recording on/off
      const rButton = document.getElementsByClassName("trackRecord")[0];
      const mainDiv = document.getElementById(SKELETON_DIV);

      rButton.addEventListener("click", () => {
        console.log("record button clicked!");

        if (rButton.classList.contains("trackRecordOn")) {
          rButton.classList.remove("trackRecordOn");
          mainDiv.classList.remove("recording-active");
        } else {
          rButton.classList.add("trackRecordOn"); //trackRecordOn needs to be lower in the css to take priority
          mainDiv.classList.add("recording-active");
        }

        const toggleMetroEvent = new CustomEvent("toggleAction", { detail: {} });
        document.dispatchEvent(toggleMetroEvent);

        if (!autoScroll) {
          autoScroll = true;
        } else {
          autoScroll = false;
        }
      });

      this.buttonContainerRowB = this.p.createDiv();
      this.buttonContainerRowB.class("buttonContainerRowB buttonContainerRow");
      this.buttonContainerRowB.parent(this.buttonContainer);

      this.deleteButton = this.p.createButton(".");
      //this.deleteButton = this.p.createImg("skeletonAssets/deleteIcon.png", "Delete");;
      this.deleteButton.class("trackDelete");
      this.deleteButton.parent(this.buttonContainerRowB);
      this.deleteButton.mousePressed(() => {
        if (deleteEnabled) {
          console.log("delete!");
          fetch("/deleteRecording", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key: "value" }),
          }).then((data) => {
            const toggleNoteDisplayEvent = new CustomEvent("toggleNotes", { detail: {} });
            document.dispatchEvent(toggleNoteDisplayEvent);
            1;
          });
        }
      });

      this.buttonContainerRowC = this.p.createDiv();
      this.buttonContainerRowC.class("buttonContainerRowC buttonContainerRow");
      this.buttonContainerRowC.parent(this.buttonContainer);

      this.volumeSlider = this.p.createSlider(0, 200, 100);
      //this.volumeSlider.position(x + 15, y + 445);
      this.volumeSlider.class("trackVolume");
      this.volumeSlider.parent(this.buttonContainerRowC);

      this.buttonContainerRowD = this.p.createDiv();
      this.buttonContainerRowD.class("buttonContainerRowD buttonContainerRow");
      this.buttonContainerRowD.parent(this.buttonContainer);
      this.recordIndicator = this.p.createSpan();
      this.recordIndicator.class("trackRecordType");
      this.recordIndicator.parent(this.buttonContainerRowD);

      this.p.strokeWeight(5);
      this.p.startOfMusic = this.p.line(x + 190, y + 15, x + 190, y + 100);

      this.p.strokeWeight(2);
      this.p.sequenceLine = this.p.line(x + 200, y + 60, x + 650, y + 60);

      //NOTE CREATION ------------------------------------------------------------------------------

      this.noteContainer = this.p.createDiv();
      this.noteContainer.class("noteContainer");
      this.noteContainer.parent(this.trackContainer);
      observer.observe(this.noteContainer.elt, { characterData: false, childList: true, attributes: false }); //.elt makes it a real element lol
    }

    draw() {
      this.p.strokeWeight(5);
      this.p.line(this.x + 190, this.y + 15, this.x + 190, this.y + 100);

      this.p.strokeWeight(2);
      this.p.line(this.x + 200, this.y + 60, this.x + 650, this.y + 60);
    }
  }

  function togglePlay() {
    if (playButton.html() == "Play") {
      playButton.html("Pause");
    } else {
      playButton.html("Play");
    }
  }

  p.setup = function () {
    let div = document.getElementById(SKELETON_DIV);

    let canvas = p.createCanvas(0, 0);
    p.background(0);
    canvas.id("trackCanvas");
    canvas.parent(div);

    let trackBar = p.createDiv();
    trackBar.id("trackBar");
    trackBar.parent(document.getElementsByTagName("header")[0]);

    //establishing trackbar elements
    //im gonna be honest this ought to be a different file but thats a problem for next week
    let trackBarPropertyContainer = p.createDiv();
    trackBarPropertyContainer.id("trackBarPropertyContainer");
    trackBarPropertyContainer.parent(trackBar);
    let bar1 = p.createDiv();
    bar1.class("trackBarBreak");
    bar1.parent(trackBar);
    let trackBarBPMContainer = p.createDiv();
    trackBarBPMContainer.id("trackBarBPMContainer");
    trackBarBPMContainer.parent(trackBar);
    let bar2 = p.createDiv();
    bar2.class("trackBarBreak");
    bar2.parent(trackBar);
    let trackBarBackingContainer = p.createDiv();
    trackBarBackingContainer.id("trackBarBackingContainer");
    trackBarBackingContainer.parent(trackBar);

    let badText = p.createP("Backing Track");
    badText.style("color", "black");
    badText.style("text-align", "right");
    badText.style("margin", "0");
    badText.style("line-height", "30px");
    badText.parent(trackBarBackingContainer);

    let trackDropdown = p.createSelect();
    trackDropdown.id("trackDropdown");
    trackDropdown.class("trackDropdown");
    trackDropdown.style("margin-left", "10px");
    trackDropdown.parent(trackBarBackingContainer);

    let editButton = p.createImg("static/assets/editButton/editButton.png", "Edit");
    editButton.id("editButton");
    editButton.class("trackBarButton");
    editButton.style("margin-left", "10px");
    editButton.parent(trackBarBackingContainer);

    // Populate dropdown with track names
    trackDropdown.option("Select Track");
    trackDropdown.changed(() => {
      let selectedTrack = trackDropdown.value();
      console.log("Selected Track:", selectedTrack);
    });

    playButton = p.createButton("Play");
    playButton.mousePressed(togglePlay);
    //playButton.position(5, 320);
    playButton.id("playTracks");
    playButton.parent(trackBarPropertyContainer);
    playButton.mousePressed(() => {
      const togglePlay = new CustomEvent("togglePlay", { detail: {} });
      document.dispatchEvent(togglePlay);
    });

    new track(p, 10, 35);
  };

  document.addEventListener("toggleAction", () => {
    if (deleteEnabled) {
      deleteEnabled = false;
    } else {
      deleteEnabled = true;
    }
  });
};

new p5(skeletonSketch, SKELETON_DIV);
