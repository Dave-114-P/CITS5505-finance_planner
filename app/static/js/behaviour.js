//This jquery function change the color of the navigation item when it was clicked
$(function() {
    $('.nav-item .nav-link').on('click', function () {
        if ($(this).parent('.nav-item').hasClass('skip')) {
            return; // Skip the click event if the link has the 'skip' class
        }
    });
});