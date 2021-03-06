
$(document).ready(function () {


    $('.paint_left').each(function () {
        if (parseInt($(this).text()) <= 100){
            $(this).parent().css( "background-color", "#FF6262");
        };
    });
/*
    $('.appointStatus').each(function () {
        if ($(this).text() == "-"){
            $(this).parent().css( "background-color", "#FF6262");
        };
    });*/

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


    $('#master_timetable_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'L'
    });

    $('#index_datetimepicker').datetimepicker({
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


    $('#statistics_start_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'L'
    });


    $('#statistics_end_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'L'
    });


    $('#admin_journal_datetimepicker').datetimepicker({
        locale: 'ru',
        format: 'L'
    });

    $('.entriesList').DataTable( {
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.10.20/i18n/Ukrainian.json"
            }
        });

});

