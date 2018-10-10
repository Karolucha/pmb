console.log('hell3o')

function renderNextAnnouncementField(){
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
        // var textarea = newRow.getElementsByTagName('textarea')[0]
        // textarea.name='n-a-' + currentTime;
        // textarea.value='';
        var imgInput = newRow.getElementsByTagName('input')[0]
        imgInput.name='n-a-' + currentTime;
        imgInput.value='';
        console.log('imgInput ', imgInput)
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

function removeImage(rowId){
    var cancelText = 'Anuluj';
    var deleteText = 'Usuń'
    var textOnButton = document.querySelector('#'+rowId+' .w3-btn').textContent;
    if (textOnButton === deleteText) {
        console.log('Remove image')
        var imageRow = document.getElementById(rowId);
        console.log(imageRow)
        imageRow.style.backgroundColor = 'rgb(244, 98, 66, 0.8)';
        document.querySelector('#'+rowId+' img').className='remove_image';
        document.querySelector('#'+rowId+' .w3-btn').textContent='Anuluj';
        document.querySelector('#'+rowId+' p').style.display='';
        document.querySelector('#'+rowId+' input').name='deletions';
    } else {
        console.log('Remove image')
        var imageRow = document.getElementById(rowId);
        console.log(imageRow)
        imageRow.style.backgroundColor = '';
        document.querySelector('#'+rowId+' img').className='w-30';
        document.querySelector('#'+rowId+' .w3-btn').textContent='Usuń';
        document.querySelector('#'+rowId+' p').style.display='None';
        document.querySelector('#'+rowId+' input').name='gallery';
    }

    //imageRow.getElementsByTagName('img').style.display='None';
}
