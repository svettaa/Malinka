
$(document).ready(function () {


    $('.paint_left').each(function () {
        if (parseInt($(this).text()) <= 100){
            $(this).addClass("bg-danger");
        };
    });


    $('#change_start_datetimepicker').datetimepicker({
        locale: 'ru'
    });


    $('#change_end_datetimepicker').datetimepicker({
        locale: 'ru'
    });


    $('#supply_date_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'L'
    });


    $('#admin_appointment_date_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'L'
    });


    $('#admin_appointment_start_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'LT'
    });


    $('#admin_appointment_end_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'LT'
    });

    $('.entriesList').DataTable();


});

