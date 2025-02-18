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

      this.x = x;
      this.y = y;
      this.id = holderCount;
    
      this.muted = false;
      this.isolated = false;

      this.number = this.p.createP(holderCount + 1);
      this.number.position(x, y - (-310));
      this.number.class("numberDisplay");
      this.number.id("numberDisplay" + holderCount);
      
      this.nameField = this.p.createInput();
      this.nameField.position(x + 1, y + 355);
      this.nameField.class("trackName");
      this.nameField.id("trackName" + holderCount);
      this.nameField.size(100);
      
      this.recordButton = this.p.createImg("skeletonAssets/recordIcon.png", "Record");
      this.recordButton.size(25, 25);
      this.recordButton.position(x + 140, y + 355);
      this.recordButton.class("trackRecord");
      this.recordButton.id("trackRecord" + holderCount);
      
      this.muteButton = this.p.createImg("skeletonAssets/unmutedIcon.png", "Mute");
      this.muteButton.size(25, 25);
      this.muteButton.mousePressed(() => {
        if(this.muteButton.attribute("src") == "skeletonAssets/unmutedIcon.png"){
          this.muteButton.attribute("src", "skeletonAssets/mutedIcon.png");
          this.muted = true;
        } else {
          this.muteButton.attribute("src", "skeletonAssets/unmutedIcon.png");
          this.muted = false;
        }
      });
      this.muteButton.position(x + 1, y + 405);
      this.muteButton.class("trackMute");
      this.muteButton.id("trackMute" + holderCount);
      
      this.isoButton = this.p.createButton("Isolate");
      //NO FUNCTIONALITY YET
      this.isoButton.position(x + 38, y + 400);
      this.isoButton.class("trackIso");
      this.isoButton.id("trackIso" + holderCount);
      
      this.deleteButton = this.p.createImg("skeletonAssets/deleteIcon.png", "Delete");
      this.deleteButton.size(25, 25);
      //NO FUNCTIONALITY YET
      this.deleteButton.position(x + 130, y + 405);
      this.deleteButton.class("trackDelete");
      this.deleteButton.id("trackDelete" + holderCount);
      
      this.volumeSlider = this.p.createSlider(0, 200, 100);
      this.volumeSlider.position(x + 15, y + 445);
      this.volumeSlider.class("trackVolume");
      this.volumeSlider.id("trackVolume" + holderCount);
      
      this.p.strokeWeight(5);
      this.p.startOfMusic = this.p.line(x + 190, y + 15, x + 190, y + 100);
      
      this.p.strokeWeight(2);
      this.p.sequenceLine = this.p.line(x + 200, y + 60, x + 650, y + 60);
      
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
    p.resizeCanvas(canvasSizeX, canvasSizeY);
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

  p.setup = function(){
    let div = document.getElementById(SKELETON_DIV);

    let canvas = p.createCanvas(canvasSizeX, canvasSizeY);
    p.background(220);
    canvas.id("trackCanvas");
    canvas.parent(div);
    
    playButton = p.createButton("Play");
    playButton.mousePressed(togglePlay)
    playButton.position(5, 320);
    playButton.id("playTracks");
    playButton.parent(div);
  // here you can change the placment of the track .
    addButton = p.createButton("Add New Track");
    addButton.mousePressed(addTrack);
    addButton.position(470, 320);
    addButton.size(125);
    addButton.id("addTrack");
    addButton.parent(div);
    
    tracks[0] = new track(p, 10, 35);
  }
}

new p5(skeletonSketch, SKELETON_DIV);
