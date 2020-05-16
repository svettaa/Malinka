var appointmentSocket;

var form;
var datePicker;
var procPicker;

function clearIndexMessages() {
    $('#index-message').html('');
}

function showIndexError(error) {
    $('#index-message').html('<div class="alert alert-danger" role="alert">' + error + '</div>');
}

function hideIndexFreeTime() {
    $('#index-free-time').css('display', 'none');
}

function showIndexFreeTime(error) {
    $('#index-free-time').css('display', 'block');
}

function refreshFreeTime() {
    const dateStr = datePicker.val();
    const procStr = procPicker.find('option:selected').val();

    clearIndexMessages();
    hideIndexFreeTime();
    clearTabs($('#index-tabs'));
    clearTabsContent($('#index-content'));

    if(dateStr.length > 0 && procStr.length > 0){
        appointmentSocket.emit('get_free_time', {'date': dateStr, 'procedure': procStr});
    }
}

function showMasterFreeTime(master){
    addTab($('#index-tabs'), master.id, master.surname + ' ' + master.first_name);
    const content = buildTabContent($('#index-content'), master.id);

    $.each(master.freeTime, function(){
        content.append(this.start + ' - ' + this.end + '<br>');
    });
}

function showFreeTime(result) {

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        if(status == false){
            showIndexError(message);
        } else {
            showIndexFreeTime();
            $.each(data, function(){
                showMasterFreeTime(this);
            });
        }
}

function initAppointmentForm() {
    if (form !== undefined)
        return;

    appointmentSocket = io('http://127.0.0.1:5000/appointment');

    $([document.documentElement, document.body]).animate({
        scrollTop: $("#appointment-jumbotron").offset().top
    }, 500);

    form = $('form#appointment');

    datePicker = form.find('#index-input').eq(0);
    procPicker = form.find('#indexProc').eq(0);

    setCurrentDateVal(datePicker);
    form.css('display', 'block');

    datePicker.focusout(refreshFreeTime);
    procPicker.change(refreshFreeTime);
    refreshFreeTime();

    appointmentSocket.on('get_free_time', showFreeTime);
}

$(document).ready(function (){
    initAppointmentForm();
//    $('button.create-appointment').on('click', initAppointmentForm);
});