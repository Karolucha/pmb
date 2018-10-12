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
        var imgInput = newRow.getElementsByTagName('input')[0]
        imgInput.name='n-a-' + currentTime;
        imgInput.value='';
        console.log('imgInput ', imgInput)
    }, 1)
}

document.addEventListener('keydown', function(event) {
    if (event.keyCode == '37') {
       plusSlides(-1)
    }
    else if (event.keyCode == '39') {
       plusSlides(1)
    }
});



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
  var slides = document.getElementsByClassName("mySlidesGallery");
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