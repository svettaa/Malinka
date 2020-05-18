
function initJournalTab(master) {
    addTab($('#main-tabs'), master.id, master.surname + ' ' + master.first_name);
    const content = buildTabContent($('#main-content'), master.id);

    const table = buildTable();
    content.append(table);

    buildTimeTable(table);

    $.each(master.appointments, function(){
         addAppointment(table, this);
    });

    $.each(master.vacations, function(){
         addVacation(table, this);
    });

    $.each(master.notWorking, function(){
         if (this.start !== this.end) {
            addNotWorking(table, this);
         }
    });
}

function initJournal(result) {

        clearMessages();
        clearTabs($('#main-tabs'));
        clearTabsContent($('#main-content'));

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        if(status == false){
            showError(message);
        } else {
            $.each(data, function(){
                initJournalTab(this);
            });
        }
}

$(document).ready(function () {
    var admin_socket = io(URL + '/admin')

    function get_journal(){
        var msg = $('#admin-journal-input').val();
        admin_socket.emit('get_journal', msg);
    }

    setCurrentDateVal($('#admin-journal-input'));

    get_journal();
    $('#admin-journal-input').focusout(get_journal);

    admin_socket.on('get_journal', initJournal);
});
