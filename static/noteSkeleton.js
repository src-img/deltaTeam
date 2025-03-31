const SKELETON_DIV = "noteSkeletonContainer";

let skeletonSketch = function(p) {
  let playButton;
  let addButton;
  let holderCount = 0;
  let current = 0;
  let tracks = [];
  let current_composition = 0; //dummy lol

  let canvasSizeX = 600;
  let canvasSizeY = 200;

  class track {
    constructor(p5, x, y){
      this.p = p5;

      this.number = this.p.createDiv(holderCount + 1);
      //this.number.position(x, y - (-310));
      this.number.class("numberDisplay");
      this.number.id("numberDisplay" + holderCount);

      this.trackContainer = this.p.createDiv();
      this.trackContainer.id("trackContainer" + holderCount);
      this.trackContainer.class("trackContainer");

      this.x = x;
      this.y = y;
      this.id = holderCount;
    
      this.muted = false;
      this.isolated = false;

      //BUTTON CREATION ---------------------------------------------------------------------------------
      this.buttonContainer = this.p.createDiv();
      this.buttonContainer.id("buttonContainer" + holderCount);
      this.buttonContainer.class("buttonContainer");
      this.buttonContainer.parent(this.trackContainer);

      this.buttonContainerRowA = this.p.createDiv();
      this.buttonContainerRowA.id("buttonContainerRowA" + holderCount);
      this.buttonContainerRowA.class("buttonContainerRowA buttonContainerRow");
      this.buttonContainerRowA.parent(this.buttonContainer);
      
      this.nameField = this.p.createInput();
      this.nameField.class("trackName");
      //this.nameField.placeholder("Track Name");
      this.nameField.id("trackName" + holderCount);
      this.nameField.parent(this.buttonContainerRowA);
      
      this.recordButton = this.p.createButton("-");
      //this.recordButton = this.p.createImg("skeletonAssets/recordIcon.png", "Record");
      this.recordButton.class("trackRecord");
      this.recordButton.id("trackRecord" + holderCount);
      this.recordButton.parent(this.buttonContainerRowA);

      // Event listener to turn recording on/off
      // const rButton = document.getElementById("trackRecord" + holderCount);
      // rButton.addEventListener('click', () => {
      //   console.log("record button clicked!");

      //   let string = rButton.id;
      //   console.log(string);
      //   string = string.replace(/\D/g, ""); //gets only digits
      //   console.log(string);
        
      //   fetch('/recording', {
      //     method: 'POST',
      //     headers: {'Content-Type': 'application/json'},
      //     body: JSON.stringify({key: 'value', trackId: string})
      //   })
      // })

      // Event listener to turn recording on/off
      const rButton = document.getElementById("trackRecord" + holderCount);
      rButton.addEventListener('click', () => {
      console.log("record button clicked!");

      let string = rButton.id;
        console.log(string);
        string = string.replace(/\D/g, ""); //gets only digits
        console.log(string);

      if (rButton.classList.contains('trackRecordOn')) rButton.classList.remove('trackRecordOn');
      else rButton.classList.add('trackRecordOn'); //trackRecordOn needs to be lower in the css to take priority

      fetch('/recording', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({key: 'value'})
      })

      const toggleMetroEvent = new CustomEvent('toggleAction', {detail:{}});
      document.dispatchEvent(toggleMetroEvent);
      })


















      this.buttonContainerRowB = this.p.createDiv();
      this.buttonContainerRowB.id("buttonContainerRowB" + holderCount);
      this.buttonContainerRowB.class("buttonContainerRowB buttonContainerRow");
      this.buttonContainerRowB.parent(this.buttonContainer);

      this.muteButton = this.p.createButton(".");
      //this.muteButton = this.p.createImg("skeletonAssets/unmutedIcon.png", "Mute");
      this.muteButton.mousePressed(() => {
        if (this.muteButton.style('background').includes('unmutedIcon.png')) {
          this.muteButton.style('background-image', 'url(../static/assets/skeleton/mutedIcon.png)');
          this.muted = true;
        } else {
          this.muteButton.style('background-image', 'url(../static/assets/skeleton/unmutedIcon.png)');
          this.muted = false;
        }
      });
      this.muteButton.class("trackMute");
      this.muteButton.id("trackMute" + holderCount);
      this.muteButton.parent(this.buttonContainerRowB);
      
      this.isoButton = this.p.createButton(".");
      //NO FUNCTIONALITY YET
      this.isoButton.class("trackIso");
      this.isoButton.id("trackIso" + holderCount);
      this.isoButton.parent(this.buttonContainerRowB);
      
      this.deleteButton = this.p.createButton(".");
      //this.deleteButton = this.p.createImg("skeletonAssets/deleteIcon.png", "Delete");;
      //THERE IS FUNCTIONALITY BUT IT EATS THE IDS WHEN YOU DELETE SOMETHING 
      //the display is nice but internally your ids are absolutely screwed. only of note if we need them tho lol
      //also for consideration: actually only deleting the final track and shifting everything else's data down. but that seems. harder
      this.deleteButton.class("trackDelete");
      this.deleteButton.id("trackDelete" + holderCount);
      this.deleteButton.parent(this.buttonContainerRowB);
      this.deleteButton.mousePressed(() => {
        if (document.getElementsByClassName("trackContainer").length > 1) {
          removeTrack(this);
          let trackNums = document.getElementsByClassName("numberDisplay");
          for (let i = 0; i < trackNums.length; i++) {
            trackNums[i].innerHTML = i + 1;
            trackNums[i].id = "numberDisplay" + i;
          }

          let trackTracks = document.getElementsByClassName("trackContainer");
          for (let i = 0; i < trackTracks.length; i++) {
            trackTracks[i].id = "trackContainer" + i;
          }

          let trackButton = document.getElementsByClassName("buttonContainer");
          for (let i = 0; i < trackButton.length; i++) {
            trackButton[i].id = "buttonContainer" + i;
          }

          let trackButtonRA = document.getElementsByClassName("buttonContainerRowA buttonContainerRow");
          for (let i = 0; i < trackButtonRA.length; i++) {
            trackButtonRA[i].id = "buttonContainerRowA" + i;
          }

          let trackButtonRB = document.getElementsByClassName("buttonContainerRowB buttonContainerRow");
          for (let i = 0; i < trackButtonRB.length; i++) {
            trackButtonRB[i].id = "buttonContainerRowB" + i;
          }

          let trackButtonRC = document.getElementsByClassName("buttonContainerRowC buttonContainerRow");
          for (let i = 0; i < trackButtonRC.length; i++) {
            trackButtonRC[i].id = "buttonContainerRowC" + i;
          }

          let trackName = document.getElementsByClassName("trackName");
          for (let i = 0; i < trackName.length; i++) {
            trackName[i].id = "trackName" + i;
          }

          let trackRecord = document.getElementsByClassName("trackRecord");
          for (let i = 0; i < trackRecord.length; i++) {
            trackRecord[i].id = "trackRecord" + i;
          }

          let trackMute = document.getElementsByClassName("trackMute");
          for (let i = 0; i < trackMute.length; i++) {
            trackMute[i].id = "trackMute" + i;
          }

          let trackIso = document.getElementsByClassName("trackIso");
          for (let i = 0; i < trackIso.length; i++) {
            trackIso[i].id = "trackIso" + i;
          }

          let trackDelete = document.getElementsByClassName("trackDelete");
          for (let i = 0; i < trackDelete.length; i++) {
            trackDelete[i].id = "trackDelete" + i;
          }

          let trackVolume = document.getElementsByClassName("trackVolume");
          for (let i = 0; i < trackVolume.length; i++) {
            trackVolume[i].id = "trackVolume" + i;
          }

          let trackNote = document.getElementsByClassName("noteContainer");
          for (let i = 0; i < trackNote.length; i++) {
            trackNote[i].id = "noteContainer" + i;
          }
        }

        console.log("delete!")
        fetch('/deleteRecording', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({key: 'value'})
        })
      });
      // add functionality to delete button
      const dButton = document.getElementById("trackDelete" + holderCount);
      dButton.addEventListener('click', () => {
        console.log("delete!")
        fetch('/deleteRecording', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({key: 'value'})
        })
      })

      this.buttonContainerRowC = this.p.createDiv();
      this.buttonContainerRowC.id("buttonContainerRowC" + holderCount);
      this.buttonContainerRowC.class("buttonContainerRowC buttonContainerRow");
      this.buttonContainerRowC.parent(this.buttonContainer);
      
      this.volumeSlider = this.p.createSlider(0, 200, 100);
      //this.volumeSlider.position(x + 15, y + 445);
      this.volumeSlider.class("trackVolume");
      this.volumeSlider.id("trackVolume" + holderCount);
      this.volumeSlider.parent(this.buttonContainerRowC);
      
      this.p.strokeWeight(5);
      this.p.startOfMusic = this.p.line(x + 190, y + 15, x + 190, y + 100);
      
      this.p.strokeWeight(2);
      this.p.sequenceLine = this.p.line(x + 200, y + 60, x + 650, y + 60);
      
      //NOTE CREATION ------------------------------------------------------------------------------

      this.noteContainer = this.p.createDiv();
      this.noteContainer.id("noteContainer" + holderCount)
      this.noteContainer.class("noteContainer");
      this.noteContainer.parent(this.trackContainer);

      holderCount += 1;
    }
    
    draw(){
      this.p.strokeWeight(5);
      this.p.line(this.x + 190, this.y + 15, this.x + 190, this.y + 100);
      
      this.p.strokeWeight(2);
      this.p.line(this.x + 200, this.y + 60, this.x + 650, this.y + 60);
    }
  }

  function addTrack(){
    tracks[current + 1] = new track(p, tracks[current].x, tracks[current].y + 135);
    
    current++;
    
    canvasSizeY += 135;
    //p.resizeCanvas(canvasSizeX, canvasSizeY);
    p.background(220);
    
    for(let i = current; i >= 0; i--){
      tracks[i].draw();
    }

    //creates new composition in back end
    fetch('/addTrack', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({key: 'value'})
    })
  }

  function togglePlay(){
    if(playButton.html() == "Play"){
      playButton.html("Pause");
    } else {
      playButton.html("Play");
    }
  }

  function removeTrack(obj) {
    tracks.splice(obj.id, 1); //removes track from array
    current--; //for add track to add past an actual track
    obj.number.remove();
    obj.trackContainer.remove();
    holderCount--;
  }

  p.setup = function(){
    let div = document.getElementById(SKELETON_DIV);

    let canvas = p.createCanvas(0, 0);
    p.background(0);
    canvas.id("trackCanvas");
    canvas.parent(div);

    let trackBar = p.createDiv();
    trackBar.id("trackBar");
    trackBar.parent(document.getElementsByTagName("header")[0])

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
    
    playButton = p.createButton("Play");
    playButton.mousePressed(togglePlay)
    //playButton.position(5, 320);
    playButton.id("playTracks");
    playButton.parent(trackBarPropertyContainer);
    playButton.mousePressed(() =>{
      const togglePlay = new CustomEvent('togglePlay', {detail:{}});
      document.dispatchEvent(togglePlay);
    })
  // here you can change the placment of the track .
    addButton = p.createButton("Add Track");
    addButton.mousePressed(addTrack);
    //addButton.position(470, 320);
    addButton.size(125);
    addButton.id("addTrack");
    addButton.parent(trackBarPropertyContainer);
    
    tracks[0] = new track(p, 10, 35);
  }
}

new p5(skeletonSketch, SKELETON_DIV);

