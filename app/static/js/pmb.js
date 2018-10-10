$(document).ready(function () {
    console.log('load');
    $('#btnSideBarOpen').click(function(){
        $('#mySidebar').show();
    })

    $('#sideBarClose').click(function(){
        $('#mySidebar').hide();
    })
    $('.dropdown-toggle').dropdown()
    // $('.dropdown-toggle').hover(function(){
    //     console.log('toogle');
    //     $('.dropdown-toggle').dropdown('toggle')
    // })
    var dropdownTownshipLinkSelector = '.k-menu-dropdown .nav-link'
    $(dropdownTownshipLinkSelector).click(function (e) {
        console.log('WAS CLICKED');
        e.preventDefault()
        $(dropdownTownshipLinkSelector).removeClass("active");
        $(dropdownTownshipLinkSelector).removeClass("show");
        $(this).tab('show');
    });
    $('.row-dropdown').on('show.bs.dropdown', function () {
        console.log('up')
        $('.row-dropdown').css('display', 'flex');
        console.log('WAS CLICKED');
    })

    $('.row-dropdown').on('show.bs.dropdown', function () {
        console.log('down')
        $('.row-dropdown').css('display', '');
    })
    // $('.lead .nav-link').on('mouseenter',function(e){
    //     console.log('OOOn');
    // });
//    var weekIntention = false;
//    $('#table-week-intention').hide();
//    $('#btn-week-intention').click(function(){
//        var textToDisplay = weekIntention ? 'Cały tydzień' : 'Zwiń';
//        $(this).text(textToDisplay);
//        $('#card-week-intention').toggle(weekIntention);
//        $('#table-week-intention').toggle(!weekIntention);
//        weekIntention = !weekIntention;
//    })

});

var myIndex = 0;
var myIndex2 = 0;
var myIndex3 = 0;
carousel(myIndex, 'mySlides');
carousel(myIndex2, 'mySlides2');
carousel(myIndex3, 'mySlides3');

function carousel(index, className) {
    var i;
    var x = document.getElementsByClassName(className);
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";
    }
    index++;
    if (index > x.length) {index = 1}
    x[index-1].style.display = "flex";
    setTimeout(function() {
        carousel(index, className);
    }    , 2000); // Change image every 2 seconds
}
//carousel2();

function carousel2() {
    var i;
    var x = document.getElementsByClassName("mySlides2");
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";
    }
    myIndex2++;
    if (myIndex2 > x.length) {myIndex2 = 1}
    x[myIndex2-1].style.display = "flex";
    setTimeout(carousel, 2000); // Change image every 2 seconds
}