// let stringInput1 = "|W+|W|"
// let stringInput2 = "|H+H|HH+|HH|"
// let stringInput3 = "|QQQE+E|QQQEE+|EQQQE|"
// let stringInput4 = "|Q+QQQ+|QQQQ|"
// let testString = "|e.S+SES+QEe|h.Q|hEeq|W+|HSesq|hQ.E+|EEEeh|h.Q+|SesE.S+E.S+E.S+|Q.+SSQ.+Ss|"

// take from whichever string input we want to use
let selected = ""

let canvasWidth = selected.length * 150;

let staffStart = 100;
let staffEnd = canvasWidth - 100;

function setup() {
  createCanvas(canvasWidth, 200);
  strokeWeight(2);
  textSize(50);
  textAlign(CENTER, CENTER);
}

function draw() {
  background(255);
  //line(staffStart, 100, staffEnd, 100);
  const element = document.getElementById('jinja'); 
  selected = element.textContent;
  canvasWidth = selected.length * 150;
  resizeCanvas(canvasWidth, 200);
  printNotes(selected);
}

function printNotes(measure) {
  // var used to determine note spacing
  let space = 0;
  let notePos = staffStart;
  
  for (let i = 1; i < measure.length + 1; i++) {
    let ch = measure[i - 1];
    switch (ch) {
      // tie case
      case '+':
        // gets the previous note location that was just placed
        let prevNote = space;
        if (measure[i] == '|') {
          space += 60;
        } 
        // calculates curve between the next note and the current one
        // gets the location of the next note
        let nextNote = notePos + space;
        curve(notePos, 50, notePos, 120, nextNote, 120, nextNote, 50);
        space = prevNote;
        break;
      // measure line
      case '|':
        notePos += space;
        line(notePos, 50, notePos, 150);
        space = 60;
        break;
      // NOTE CASES -------------------------------------
      // quarter note
      case 'Q':
        notePos += space;
        text('Q', notePos, 100);
        if (measure[i] == '.') {
          space = 25;
          text('.', notePos + space, 100);
        }
        space = 60;
        break;
      // eighth note
      case 'E':
        notePos += space;
        text('E', notePos, 100);
        if (measure[i] == '.') {
          space = 20;
          text('.', notePos + space, 100);
        }
        space = 40;
        break;
      // half note
      case 'H':
        notePos += space;
        text ('H', notePos, 100);
        if (measure[i] == '.') {
          space = 20;
          text('.', notePos + space, 100);
        }
        space = 120;
        break;
      // whole note
      case 'W':
        notePos += space;
        text('W', notePos, 100);
        space = 240;
        break;
      // sixteenth note
      case 'S':
        notePos += space;
        text('S', notePos, 100);
        space = 40;
        break;
      // REST CASES -------------------------------------
      // quarter rest
      case 'q':
        notePos += space;
        text('q', notePos, 100);
        if (measure[i] == '.') {
          space = 25;
          text('.', notePos + space, 100);
        }
        space = 60;
        break;
      // eighth rest
      case 'e':
        notePos += space;
        text('e', notePos, 100);
        if (measure[i] == '.') {
          space = 20;
          text('.', notePos + space, 100);
        }
        space = 40;
        break;
      // half rest
      case 'h':
        notePos += space;
        text ('h', notePos, 100);
        if (measure[i] == '.') {
          space = 20;
          text('.', notePos + space, 100);
        }
        space = 120;
        break;
      // whole rest
      case 'w':
        notePos += space;
        text('W', notePos, 100);
        space = 240;
        break;
      // sixteenth rest
      case 's':
        notePos += space;
        text('S', notePos, 100);
        space = 40;
        break;
    }
  }
  line(staffStart, 100, notePos, 100);
}
