let metrognome;
window.metrognome = null;
function setup() {
    const canvas = createCanvas(50, 50);
    canvas.id("gnomeCanvas");
    canvas.parent(document.getElementById("trackBarBPMContainer")); 
  
    loadAnimations(this);
    metrognome = new Gnome(this, 25, 25, 48); 
    window.metrognome = metrognome;
  }
  
  function draw() {
    background(255);
    if (metrognome) metrognome.display();
  }
  

class Gnome {
  constructor(p, x, y, size = 20) {
    this.p = p;
    this.size = size;
    this.x = x;
    this.y = y;
    this.frame = 8;
  }

  nextBeat() {
    this.frame = (this.frame + 1) % window.animations["gnome"].length;
  }
  
  setIdle() {
    this.frame = 8; 
  }
  display() {
    const p = this.p;
    const img = window.animations["gnome"][this.frame];
    p.push();
    p.translate(this.x, this.y);
    p.imageMode(p.CENTER);
    p.image(img, 0, 0, this.size, this.size);
    p.pop();
  }
}

function loadAnimations(p) {
  window.animations = {};
  window.animations["gnome"] = [];

  for (let i = 1; i <= 9; i++) {
    const frameNum = String(i).padStart(3, '0');
    window.animations["gnome"].push(p.loadImage(`/static/assets/gnome/gnome${frameNum}.png`));
  }

  console.log("Gnome frames loaded");
}
