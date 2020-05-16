
//function fillMasterTimetable(result) {
//
//        clearMessages();
//        buildTimeTable($('#mainTable'));
//
//        var status = result['status'];
//        var message = result['message'];
//        var data = result['data'];
//
//        if(status == false){
//            showError(message);
//        } else {
//            $.each(data, function(){
//                addAppointment($('#mainTable'), this);
//            });
//        }
//}

$(document).ready(function () {
    var admin_socket = io('http://127.0.0.1:5000/admin')

    function get_timetable(){
        var msg = $('#admin-journal-input').val();
        admin_socket.emit('get_journal', msg);
    }

    setCurrentDateVal($('#admin-journal-input'));

    get_timetable();
    $('#admin-journal-input').focusout(get_timetable);

//    admin_socket.on('get_journal', fillMasterTimetable);
});
