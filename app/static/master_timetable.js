
function fillMasterTimetable(result) {

        clearMessages();
        buildTimeTable($('#mainTable'));

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        if(status == false){
            showError(message);
        } else {
            $.each(data.appointments, function(){
                addAppointment($('#mainTable'), this);
            });
            $.each(data.vacations, function(){
                addVacation($('#mainTable'), this);
            });
            $.each(data.notWorking, function(){
                 if (this.start !== this.end) {
                    addNotWorking($('#mainTable'), this);
                 }
            });
        }
}

$(document).ready(function () {
    var master_socket = io(URL + '/master')

    function get_timetable(){
        var msg = $('#master-timetable-input').val();
        master_socket.emit('get_master_timetable', msg);
    }

    setCurrentDateVal($('#master-timetable-input'));

    get_timetable();
    $('#master-timetable-input').focusout(get_timetable);

    master_socket.on('get_master_timetable', fillMasterTimetable);
});
