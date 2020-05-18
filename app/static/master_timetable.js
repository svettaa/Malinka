
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

function getData() {
    $.ajax({
                    type: "GET",
                    url: "/get_master_timetable",
                    data: {'date': $('#master-timetable-input').val()},
                    success: fillMasterTimetable,
                    error: function(error) {
                        console.log(error);
                    }
    });
}

$(document).ready(function () {
    setCurrentDateVal($('#master-timetable-input'));

    getData();
    $('#master-timetable-input').focusout(getData);
});
