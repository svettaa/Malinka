
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

function getData(){
    $.ajax({
                type: "GET",
                url: "/get_journal",
                data: $('#admin-journal-input').val(),
                success: initJournal,
                error: function(error) {
                    console.log(error);
                }
    });
}

$(document).ready(function () {

    setCurrentDateVal($('#admin-journal-input'));

    getData();
    $('#admin-journal-input').focusout(getData);
});
