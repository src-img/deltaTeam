let test1 = "|h+e.S+Q+|E.sq+sE+S+SEs|qQ.E+Ses|w|h.Q|h.+e.S|sE+S+Q+SEsq|E.S+E.S+H+|SeseE+EE+E.S+|Q.+SSqSes|";
let test2 = "|e.S+SE+S+SES+E.S+|QQH+|W+|";
let test3 = "|mnoq|";
let test4 = "|Hqq|qqqq|qqqq|qyyy|yyyy|yyyy|mmnq|";
let test5 = "|qqqUseUs|qqqq|qqqq|";

let playbackSketch = function(p) {
    let sound;
    let BPM;
    let isPlaying = false;

    let timeouts = [];

    p.preload = function() {
        sound = p.loadSound('./static/assets/sounds/snare.mp3');
    }

    // Main Functions

    function convertString(stringInput) {
    /*
    
        NOTE CONVERSION KEY:
        q = Q, e = E, s = S, h = H, w = W and vice versa for rests
        n = EE, N = SS
        y = EEEE, Y = SSSS
        m = SSE, M = ESS
        o = ES, O = SE
        U = +
        j = Q., J = q.
        i = E., I = e.
        d = H., D = h.
        
    */
    
    let result = "";
    for (let i = 0; i < stringInput.length; i++) {
        switch(stringInput[i]) {
        case '|':
            result += '|';
            break;
            
        // notes
        case 's':
            result += 'S';
            break;
        case 'e':
            result += 'E';
            break;
        case 'q':
            result += 'Q';
            break;
        case 'h':
            result += 'H';
            break;
        case 'w':
            result += 'W';
            break;
            
        // rests
        case 'S':
            result += 's';
            break;
        case 'E':
            result += 'e';
            break;
        case 'Q':
            result += 'q';
            break;
        case 'H':
            result += 'h';
            break;
        case 'W':
            result += 'w';
            break;
            
        // ties
        case 'U':
            result += '+';
            break;
        case 'v':
            result += '+';
            break;
            
        // dotted rhythms
        case 'i':
            result += 'E.';
            break;
        case 'j':
            result += 'Q.';
            break;
        case 'd':
            result += 'H.';
            break;
        case 'I':
            result += 'e.';
            break;
        case 'J':
            result += 'q.';
            break;
        case 'D':
            result += 'h.';
            break;  
            
        // compound rhythms
        case 'n':
            result += 'EE';
            break;
        case 'N':
            result += 'SS';
            break;
        case 'y':
            result += 'SSSS';
            break;
        case 'Y':
            result += 'EEEE';
            break;
        case 'm':
            result += 'ESS';
            break;
        case 'M':
            result += 'SSE';
            break;
        case 'T':
            result += 'SES';
            break;
        case 'o':
            result += 'E.S';
            break;
        case 'O':
            result += 'SE.';
            break;
        }
    }
        // console.log("New string = " + result);
        // console.log("String length = " + result.length);
        return result;
    }

    function playback(song) {
        // first, the program loads the length of the notes into an array
        // goes through each letter, assigns a value.
        let length = [];
        let isRest = [];
        let isTie = false;
        let ch;
        for (let i = 0; i < song.length; i++) {
            ch = song[i];
            switch (ch) {
            case '+':
                isTie = true;
                break;
            case '.':
                // period case to alter the length of the previous note by 1.5x
                // console.log(length.at(-1));
                // ik this looks like ass
                length[length.length - 1] += length.at(-1)/2;
                break;
            // NOTE CASES ======================================================
            case 'S':
                length.push(15000/BPM);
                if (isTie) {
                isRest.push(true);
                isTie = false;
                }
                else {
                isRest.push(false);
                }
                break;
            case 'E':
                length.push(30000/BPM);
                if (isTie) {
                isRest.push(true);
                isTie = false;
                }
                else {
                isRest.push(false);
                }
                break;  
            case 'Q':
                length.push(60000/BPM);
                if (isTie) {
                isRest.push(true);
                isTie = false;
                }
                else {
                isRest.push(false);
                }
                break;
            case 'H':
                length.push(120000/BPM);
                if (isTie) {
                isRest.push(true);
                isTie = false;
                }
                else {
                isRest.push(false);
                }
                break;
            case 'W':
                length.push(240000/BPM);
                if (isTie) {
                isRest.push(true);
                isTie = false;
                }
                else {
                isRest.push(false);
                }
                break;
            // REST CASES =====================================================
            case 's':
                length.push(15000/BPM);
                isRest.push(true);
                break;
            case 'e':
                length.push(30000/BPM);
                isRest.push(true);
                break;
            case 'q':
                length.push(60000/BPM);
                isRest.push(true);
                break;
            case 'h':
                length.push(120000/BPM);
                isRest.push(true);
                break;
            case 'w':
                length.push(240000/BPM);
                isRest.push(true);
                break;
            default:
                break;
            }
        }
        // console.log(length);
        playNotes(length, isRest);
    }

    // to be frank, i have no clue how this is working
    // it plays the notes based on intervals provided in playback()
    function playNotes(noteDurations, rests) {
        if(!isPlaying){
            isPlaying = true;
            let currentTime = 0; 
            noteDurations.forEach((duration, index) => {
                timeoutID = setTimeout(() => {
                if(isPlaying){
                    let isRests = rests[index];
                    if (!isRests) {
                        sound.play();
                    }
                }
                }, currentTime);
                timeouts.push(timeoutID);
                currentTime += duration;
            });
        }
    }
    let comp = ""
    document.addEventListener('togglePlayback', () => {
        let button = document.getElementById("playTracks");
        if(button.innerHTML == "Pause"){
            // figure out this -------
            console.log("Getting composition");
            const selected = document.getElementsByClassName("noteContainer")[0];
            comp = selected.textContent
            console.log(comp)

            BPM = document.getElementById("metroBPM").textContent;
            // figure out this -------

            // this is the conversion part that is already figured out
            let song = convertString(comp);
            playback(song);
            // p.console.log(song);
        } else {
            isPlaying = false;
            sound.stop();

            timeouts.forEach(timeoutID => {
                clearTimeout(timeoutID);
            });

            timeouts = [];
        }
    });
}
new p5(playbackSketch);
