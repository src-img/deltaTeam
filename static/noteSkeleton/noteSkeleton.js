const SKELETON_DIV = "noteSkeletonContainer";

let skeletonSketch = function(p) {
  let playButton;
  let addButton;
  let holderCount = 0;
  let current = 0;
  let tracks = [];

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
      
      this.nameField = this.p.createInput();
      //this.nameField.position(x + 1, y + 355);
      this.nameField.class("trackName");
      this.nameField.id("trackName" + holderCount);
      this.nameField.size(100);
      this.nameField.parent(this.buttonContainer);
      
      this.recordButton = this.p.createButton("-");
      //this.recordButton = this.p.createImg("skeletonAssets/recordIcon.png", "Record");
      //this.recordButton.size(25, 25);
      //this.recordButton.position(x + 140, y + 355);
      this.recordButton.class("trackRecord");
      this.recordButton.id("trackRecord" + holderCount);
      this.recordButton.parent(this.buttonContainer);
      
      this.muteButton = this.p.createButton("mute");
      //this.muteButton = this.p.createImg("skeletonAssets/unmutedIcon.png", "Mute");
      //this.muteButton.size(25, 25);
      this.muteButton.mousePressed(() => {
        if(this.muteButton.attribute("src") == "skeletonAssets/unmutedIcon.png"){
          this.muteButton.attribute("src", "skeletonAssets/mutedIcon.png");
          this.muted = true;
        } else {
          this.muteButton.attribute("src", "skeletonAssets/unmutedIcon.png");
          this.muted = false;
        }
      });
      //this.muteButton.position(x + 1, y + 405);
      this.muteButton.class("trackMute");
      this.muteButton.id("trackMute" + holderCount);
      this.muteButton.parent(this.buttonContainer);
      
      this.isoButton = this.p.createButton("Isolate");
      //NO FUNCTIONALITY YET
      //this.isoButton.position(x + 38, y + 400);
      this.isoButton.class("trackIso");
      this.isoButton.id("trackIso" + holderCount);
      this.isoButton.parent(this.buttonContainer);
      
      this.deleteButton = this.p.createButton("delete");
      //this.deleteButton = this.p.createImg("skeletonAssets/deleteIcon.png", "Delete");
      //this.deleteButton.size(25, 25);
      //THERE IS FUNCTIONALITY BUT IT EATS THE IDS WHEN YOU DELETE SOMETHING 
      //the display is nice but internally your ids are absolutely screwed. only of note if we need them tho lol
      //also for consideration: actually only deleting the final track and shifting everything else's data down. but that seems. harder
      //this.deleteButton.position(x + 130, y + 405);
      this.deleteButton.class("trackDelete");
      this.deleteButton.id("trackDelete" + holderCount);
      this.deleteButton.parent(this.buttonContainer);
      this.deleteButton.mousePressed(() => {
        if (document.getElementsByClassName("trackContainer").length > 1) {
          removeTrack(this);
          let trackNums = document.getElementsByClassName("numberDisplay");
          for (let i = 0; i < trackNums.length; i++) {
            trackNums[i].innerHTML = i + 1;
          }
        }
      });
      
      this.volumeSlider = this.p.createSlider(0, 200, 100);
      //this.volumeSlider.position(x + 15, y + 445);
      this.volumeSlider.class("trackVolume");
      this.volumeSlider.id("trackVolume" + holderCount);
      this.volumeSlider.parent(this.buttonContainer);
      
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
  }

  function togglePlay(){
    if(playButton.html() == "Play"){
      playButton.html("Pause");
    } else {
      playButton.html("Play");
    }
  }

  function removeTrack(obj) {
    obj.number.remove();
    obj.trackContainer.remove();
    
  }

  p.setup = function(){
    let div = document.getElementById(SKELETON_DIV);

    let canvas = p.createCanvas(0, 0);
    p.background(0);
    canvas.id("trackCanvas");
    canvas.parent(div);

    let trackBar = p.createDiv();
    trackBar.id("trackBar");

    //establishing trackbar elements
    let trackBarPropertyContainer = p.createDiv();
    trackBarPropertyContainer.id("trackBarPropertyContainer");
    trackBarPropertyContainer.parent(trackBar);
    let trackBarBPMContainer = p.createDiv();
    trackBarBPMContainer.id("trackBarBPMContainer");
    trackBarBPMContainer.parent(trackBar);
    let trackBarBackingContainer = p.createDiv();
    trackBarBackingContainer.id("trackBarBackingContainer");
    trackBarBackingContainer.parent(trackBar);
    
    playButton = p.createButton("Play");
    playButton.mousePressed(togglePlay)
    //playButton.position(5, 320);
    playButton.id("playTracks");
    playButton.parent(trackBarPropertyContainer);
  // here you can change the placment of the track .
    addButton = p.createButton("Add New Track");
    addButton.mousePressed(addTrack);
    //addButton.position(470, 320);
    addButton.size(125);
    addButton.id("addTrack");
    addButton.parent(trackBarPropertyContainer);
    
    tracks[0] = new track(p, 10, 35);
  }
}

new p5(skeletonSketch, SKELETON_DIV);
