let noteMapping = {
    "W": 1,
    "H": 1/2,
    "Q": 1/4,
    "E": 1/8,
    "S": 1/16,
    "W.": 1 * 1.5,
    "H.": 1/2 * 1.5,
    "Q.": 1/4 * 1.5,
    "E.": 1/8 * 1.5,
    "S.": 1/16 * 1.5,
}

let elementToRecordOn;

//composition is an array of arrays... level 1 is a measure, each measure contains an array of notes

document.addEventListener('keydown', function(event) {
    fetch('/keyboard_event', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ key: event.key })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.noteType);
        console.log(data.recordee);
        recordeeId = "noteContainer" + data.recordee;
        elementToRecordOn = document.getElementById(recordeeId);
        //|e.S+SES+QEe|h.Q|hEeq|W+|HSesq|hQ.E+|EEEeh|h.Q+|SesE.S+E.S+E.S+|Q.+SSQ.+Ss|
        if (elementToRecordOn.dataset.composition != undefined) { //apparently there IS a js null!
            let comp = elementToRecordOn.dataset.composition //im not typing that
            let measureValue = 0;
            for (let note of comp[comp.length - 1]) { //iterate thru notes of most recent wip measure
                measureValue += noteMapping[note]
            }
        }
        else {
            elementToRecordOn.dataset.composition = [[data.noteType]];
        }
        //console.log(elementToRecordOn.dataset.composition)

    })
    .catch(error => {
        console.error('Someone\s throwing a fit... ', error);
    });
});