document.addEventListener('keydown', function(event) {
    const key = event.key; 
    fetch('/keyboard_event', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ key: key })
    })
    .then(response => response.text())
    .then(data => console.log(data));
});


window.onload = function() {
    fetch("/compositionString")
            .then(response => {return response.text();})
            .then((html) => document.getElementById("noteContainer0").innerHTML = html);     
}

document.addEventListener('toggleNotes', (e) => {
    fetch("/compositionString")
            .then(response => {return response.text();})
            .then((html) => document.getElementById("noteContainer0").innerHTML = html)  
  });

document.addEventListener('togglePlay', (e) => {
    let button = document.getElementById("playTracks");
    if(button.innerHTML == "Play"){
        button.innerHTML = "Pause";
    } else {
        button.innerHTML = "Play";
    }
    const togglePlayback = new CustomEvent('togglePlayback', {detail:{}});
    document.dispatchEvent(togglePlayback);
})

