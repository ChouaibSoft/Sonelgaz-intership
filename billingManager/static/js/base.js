$(document).ready(function(){


    // Select Cour Or Exam Or TDs From Liste
    $(".item-dropdown").click(function() {
       $(this).addClass("now").siblings(".item-dropdown").removeClass("now").end().next().slideDown(250)
       .siblings(".info").slideUp(250);
    });


});


