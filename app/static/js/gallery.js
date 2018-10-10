console.log('hi')

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

//function deleteRow(rowId) {
//    form = document.getElementsByTagName('form')[0];
//    console.log('form', rowId);
//    if (form.getElementsByTagName('select').length ===1) {
//        alert('Nie można usunąć wszystkich!');
//        return;
//    }
//    if (rowId.startsWith('row-')) {
//        var hiddenInput = document.createElement("input");
//        hiddenInput.setAttribute("type", "hidden");
//        hiddenInput.setAttribute("name", "deletions");
//        hiddenInput.setAttribute("value", rowId);
//        form.appendChild(hiddenInput);
//    }
//    row = document.getElementById(rowId);
//    row.parentNode.removeChild(row);
//}

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}