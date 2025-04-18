// document.addEventListener('keydown', function(event) {
//     const key = event.key; 
//     fetch('/keyboard_event', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify({ key: key })
//     })
//     .then(response => response.text())
//     //.then(data => console.log(data));

//     let span = document.getElementsByClassName("trackRecordType")[0];
//     fetch('/grabRecording')
//         .then(response => response.json())
//         .then(data => {
//             if(data.recording){
//                 if(key == 'a'){
//                     span.innerHTML = "Inputting notes";
//                 } else if (key == 's'){
//                     span.innerHTML = "Inputting rests";
//                 }
//             } else {
//                 span.innerHTML = "";
//             }
//         });
// });


window.onload = function() {
    fetch("/compositionString")
            .then(response => {return response.text();})
            .then((html) => document.getElementsByClassName("noteContainer")[0].innerHTML = html);

    // //fixes bug of refreshing while recording
    // fetch("/grabRecording")
    //         .then(response => response.json())
    //         .then(data => {
    //             if(data.recording){
    //                 fetch('/recording', {
    //                     method: 'POST',
    //                     headers: {'Content-Type': 'application/json'},
    //                     body: JSON.stringify({key: 'value'})
    //                   });
    //             }
    //         });
}

document.addEventListener('toggleNotes', () => {
    fetch("/compositionString")
            .then(response => {return response.text();})
            .then((html) => document.getElementsByClassName("noteContainer")[0].innerHTML = html);
  });

document.addEventListener('togglePlay', () => {
    let button = document.getElementById("playTracks");
    let BPM = document.getElementById("metroBPM");
    const togglePlayback = new CustomEvent('togglePlayback', {detail:{}});
    if(button.innerHTML == "Play" && BPM.innerHTML != "Changing BPM" && BPM.innerHTML != ""){
        button.innerHTML = "Pause";
        document.dispatchEvent(togglePlayback);
    } else {
        button.innerHTML = "Play";
        document.dispatchEvent(togglePlayback);
    }
});

document.addEventListener('toggleEndOfPlayback', () => {
    let button = document.getElementById("playTracks");
    button.innerHTML = "Play";
});