let playButton;
let addButton;
let holderCount = 0;
let current = 0;
let tracks = [];

let canvasSizeX = 700;
let canvasSizeY = 200;

class track {
  constructor(x, y){
    this.x = x;
    this.y = y;
    this.id = holderCount;
  
    this.muted = false;
    this.isolated = false;

    this.number = createP(holderCount + 1);
    this.number.position(x, y - 10);
    this.number.class("numberDisplay");
    this.number.id("numberDisplay" + holderCount);
    
    this.nameField = createInput();
    this.nameField.position(x + 10, y + 25);
    this.nameField.class("trackName");
    this.nameField.id("trackName" + holderCount);
    this.nameField.size(100);
    
    this.recordButton = createImg("skeletonAssets/recordIcon.png", "Record");
    this.recordButton.size(25, 25);
    this.recordButton.position(x + 140, y + 22);
    this.recordButton.class("trackRecord");
    this.recordButton.id("trackRecord" + holderCount);
    
    this.muteButton = createImg("skeletonAssets/unmutedIcon.png", "Mute");
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
    this.muteButton.position(x + 10, y + 58);
    this.muteButton.class("trackMute");
    this.muteButton.id("trackMute" + holderCount);
    
    this.isoButton = createButton("Isolate");
    //NO FUNCTIONALITY YET
    this.isoButton.position(x + 52, y + 60);
    this.isoButton.class("trackIso");
    this.isoButton.id("trackIso" + holderCount);
    
    this.deleteButton = createImg("skeletonAssets/deleteIcon.png", "Delete");
    this.deleteButton.size(25, 25);
    //NO FUNCTIONALITY YET
    this.deleteButton.position(x + 125, y + 58);
    this.deleteButton.class("trackDelete");
    this.deleteButton.id("trackDelete" + holderCount);
    
    this.volumeSlider = createSlider(0, 200, 100);
    this.volumeSlider.position(x + 10, y + 85);
    this.volumeSlider.class("trackVolume");
    this.volumeSlider.id("trackVolume" + holderCount);
    
    strokeWeight(5);
    this.startOfMusic = line(x + 190, y + 15, x + 190, y + 100);
    
    strokeWeight(2);
    this.sequenceLine = line(x + 200, y + 60, x + 650, y + 60);
    
    holderCount += 1;
  }
  
  draw(){
    strokeWeight(5);
    line(this.x + 190, this.y + 15, this.x + 190, this.y + 100);
    
    strokeWeight(2);
    line(this.x + 200, this.y + 60, this.x + 650, this.y + 60);
  }
}

function addTrack(){
  tracks[current + 1] = new track(tracks[current].x, tracks[current].y + 100);
  
  current++;
  
  canvasSizeY += 100;
  resizeCanvas(canvasSizeX, canvasSizeY);
  background(220);
  
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

function setup(){
  let canvas = createCanvas(canvasSizeX, canvasSizeY);
  background(220);
  canvas.id("trackCanvas");
  
  playButton = createButton("Play");
  playButton.mousePressed(togglePlay)
  playButton.position(10, 10);
  playButton.id("playTracks");
  
  addButton = createButton("Add New Track");
  addButton.mousePressed(addTrack);
  addButton.position(560, 10);
  addButton.size(125);
  addButton.id("addTrack");
  
  tracks[0] = new track(10, 35);
}