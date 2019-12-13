var curent_page_number = 1;
var in_progress = false;

$(document).ready(function () {
    $(window).scroll(() => {
        if($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !in_progress) {
            in_progress = true;
            curent_page_number++;
            alert(curent_page_number);
            in_progress = false;
        }
    })
})