
$(document).ready(function () {


    $('.paint_left').each(function () {
        if (parseInt($(this).text()) <= 100){
            $(this).addClass("bg-danger");
        };
    });






    /*$(function () {
        $('#datetimepicker').datetimepicker({
            format: 'L'
        });
    });
*/



});


