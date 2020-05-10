
$(document).ready(function () {

    var master_socket = io('http://127.0.0.1:5000/master')

    function get_timetable(){
        var msg = $('#master-timetable-input').val();
        master_socket.emit('get_master_timetable', msg);
    }

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    var dateStr = dd + '.' + mm + '.' + yyyy;
    $('#master-timetable-input').val(dateStr);

    get_timetable();
    $('#master-timetable-input').focusout(get_timetable);

    master_socket.on('get_master_timetable', function(result){

        $('#message').html('');
        $('#mainTable > tbody').html('');

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        if(status == false){
            $('#message').html('<div class="alert alert-danger" role="alert">' + message + '</div>');
        } else {
            $.each(data, function(){
                $('#mainTable > tbody').append('<tr>' +
                '<td>' + this['appoint_start'].substring(11) + '</td>' +
                '<td>' + this['appoint_end'].substring(11) + '</td>' +
                '<td>' + this['procedure_name'] + '</td>' +
                '<td>' + this['client_surname'] + ' ' + this['client_first_name'] + '</td>' +
                '<td>' + (this['status'] ? '+' : '-') + '</td>' +
                '</tr>');
            });
        }
    });

});

