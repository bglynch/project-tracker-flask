// files for initializing materialize jquery
$(document).ready(function() {
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    setTimeout(function() {
        $('body').addClass('loaded');
    }, 0);
});
