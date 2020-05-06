
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
    });


    $('#admin_appointment_end_datetimepicker').datetimepicker({
        locale: 'ru',
    });

    $('.entriesList').DataTable( {
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.10.20/i18n/Ukrainian.json"
            }
        });

});

