var form;
var datePicker;
var procPicker;

const interval = 30;

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
        $.ajax({
                    type: "GET",
                    url: "/get_free_time",
                    data: {'date': dateStr, 'procedure': procStr},
                    success: showFreeTime,
                    error: function(error) {
                        console.log(error);
                    }
        });
    }
}

function getNumArrayFromStrTime(timeStr){
    return [parseInt(timeStr.substring(0, 2)), parseInt(timeStr.substring(3, 5))];
}

function normalizeTime(timeArray){
    while(timeArray[1] >= 60){
        timeArray[0]++;
        timeArray[1] -= 60;
    }
}

function lessOrEqualTime(timeStart, timeEnd){
    return timeStart[0] < timeEnd[0] || (timeStart[0] === timeEnd[0] && timeStart[1] <= timeEnd[1]);
}

function getStrOfTimeArray(array) {
    return String(array[0]).padStart(2, '0') + ':' + String(array[1]).padStart(2, '0');
}

function createButton(timeArray, endArray){
    const button = $('<button class="time-button" data-toggle="modal" data-target="#modalConfirm"></button>');
    button.attr('onclick',
         'refreshModal("' +
         getStrOfTimeArray(timeArray) + ' - ' + getStrOfTimeArray(endArray) +
         '");'
    );
    button.text(getStrOfTimeArray(timeArray));
    return button;
}

function refreshModal(timeStr) {
    $('#modalConfirm .modal-date').html(datePicker.val());
    $('#modalConfirm .modal-time').html(timeStr);
    $('#modalConfirm .modal-master').html($('#index-tabs a.show').text());
    $('#modalConfirm .modal-procedure').html(procPicker.find('option:selected').text());
}

function confirmAppointment() {
    var fullUrl = window.location.href;
    var arr = fullUrl.split("/");
    var domain = arr[0] + "//" + arr[2];

    var url = domain + "/confirm?" +
                            "date=" + datePicker.val() + "&" +
                            "time=" + $('#modalConfirm .modal-time').html().substring(0, 5) + "&" +
                            "master=" + $('#index-tabs a.show').attr('href').substring(1) + "&" +
                            "procedure=" + procPicker.find('option:selected').val();
    const pref = $('#modalConfirm .modal-preferences').eq(0).val();
    if (pref.length > 0){
        url += '&preferences=' + pref;
    }
    window.location.replace(url);
}

function addFreeTimeToContent(content, time, duration) {

    var startArray = getNumArrayFromStrTime(time.start);
    var endArray = getNumArrayFromStrTime(time.end);

    while(startArray[1] % interval !== 0){
        startArray[1]++;
    }
    normalizeTime(startArray);

    var flag = true;
    while(flag){
        eventEnd = [startArray[0], startArray[1] + duration];
        normalizeTime(eventEnd);

        if(lessOrEqualTime(eventEnd, endArray)) {
            content.append(createButton(startArray, eventEnd));
        } else {
            flag = false;
        }

        startArray[1] += interval;
        normalizeTime(startArray);
    }
}

function showMasterFreeTime(master){
    var masterTabTitle = master.surname + ' ' + master.first_name;
    if ('favourite' in master){
        masterTabTitle = '<i class="fas fa-heart"></i> ' + masterTabTitle;
    }

    addTab($('#index-tabs'), master.id, masterTabTitle);
    const content = buildTabContent($('#index-content'), master.id);

    $.each(master.freeTime, function(){
        addFreeTimeToContent(content, this, master.duration);
    });

    if (content.html() === '') {
        content.html('На жаль, не залишилося вільних місць у майстра в даний день.');
    }
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
            if (data.length == 0) {
                $('#index-tabs').html('Немає майстрів на цю дату та процедуру');
            }
        }
}

function initAppointmentForm() {
    if (form !== undefined)
        return;

    $([document.documentElement, document.body]).animate({
        scrollTop: $("#appointment-jumbotron").offset().top
    }, 500);

    form = $('form#appointment');

    datePicker = form.find('#index-input').eq(0);
    procPicker = form.find('#indexProc').eq(0);

    setCurrentDateVal(datePicker);
    form.css('display', 'block');

    refreshFreeTime();
    datePicker.focusout(refreshFreeTime);
    procPicker.change(refreshFreeTime);
}

$(document).ready(function (){
    $('button.create-appointment').on('click', initAppointmentForm);
});