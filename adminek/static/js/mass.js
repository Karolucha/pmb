console.log('hi')

function addMassForm(){
    console.log('Hi button');
    var massRow = document.getElementsByClassName('mass-hour-row')[0];
    var newRow = massRow.cloneNode(true);
    setTimeout(function(){
        var currentTime = new Date().getTime();
        newRow.id = 'n-' + currentTime;
        var parentAll = document.getElementById('hours-all');
        parentAll.appendChild(newRow);
        newRow.getElementsByClassName('w3-btn')[0].addEventListener("click", function() {
            deleteRow(newRow.id)
        })
        newRow.getElementsByTagName('input')[0].name='n-hour-' + currentTime;
        newRow.getElementsByTagName('select')[0].name='n-church-' + currentTime;
    }, 1)
}

function deleteRow(rowId) {
    form = document.getElementsByTagName('form')[0];
    console.log('form', rowId);
    if (form.getElementsByTagName('select').length ===1) {
        alert('Nie można usunąć wszystkich!');
        return;
    }
    if (rowId.startsWith('row-')) {
        var hiddenInput = document.createElement("input");
        hiddenInput.setAttribute("type", "hidden");
        hiddenInput.setAttribute("name", "deletions");
        hiddenInput.setAttribute("value", rowId);
        form.appendChild(hiddenInput);
    }
    row = document.getElementById(rowId);
    row.parentNode.removeChild(row);
}