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
    var weekIntention = false;
    $('#table-week-intention').hide();
    $('#btn-week-intention').click(function(){
        var textToDisplay = weekIntention ? 'Cały tydzień' : 'Zwiń';
        $(this).text(textToDisplay);
        $('#card-week-intention').toggle(weekIntention);
        $('#table-week-intention').toggle(!weekIntention);
        weekIntention = !weekIntention;
    })

});