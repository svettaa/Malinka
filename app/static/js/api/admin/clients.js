

function sendRequestGetClients(callback) {
    $.ajax({
        type: "GET",
        url: "/api/clients",
        success: callback
    });
}



function sendRequestResetClientPassword(id, callback){
    $.ajax({
        type: "GET",
        url: "/reset_password",
        data: {'id': id},
        success: callback
    });
}

function sendRequestDeleteClientPassword(id, callback){
    $.ajax({
        type: "GET",
        url: "/delete_password",
        data: {'id': id},
        success: callback
    });
}

function sendRequestGetClient(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/clients/" + id,
        success: callback
    });
}

function sendRequestAddClient(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/clients",
        data: data,
        success: callback
    });
}

function sendRequestEditClient(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/clients/" + id,
        data: data,
        success: callback
    });
}

function sendRequestDeleteClient(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/clients/" + id,
        success: callback
    });
}

function sendRequestDeleteClientAppointment(client_id, appointment_id, callback) {
    $.ajax({
        type: "DELETE",
        url: '/api/clients/' + client_id + '/appointments/' + appointment_id,
        success: callback
    });
}

function sendRequestAddFavouriteMaster(id, data, callback) {
    $.ajax({
        type: "POST",
        url: '/api/clients/' + id + '/favourite_masters',
        data: data,
        success: callback
    });
}

function sendRequestDeleteFavouriteMaster(client_id, master_id, callback) {
    $.ajax({
        type: "DELETE",
        url: '/api/clients/' + client_id + '/favourite_masters/' + master_id,
        success: callback
    });
}


function sendRequestAddFavouriteProcedure(id, data, callback) {
    $.ajax({
        type: "POST",
        url: '/api/clients/' + id + '/favourite_procedures',
        data: data,
        success: callback
    });
}

function sendRequestDeleteFavouriteProcedure(client_id, procedure_id, callback) {
    $.ajax({
        type: "DELETE",
        url: '/api/clients/' + client_id + '/favourite_procedures/' + procedure_id,
        success: callback
    });
}

function sendRequestChangePassword(client_id, data, callback) {
    $.ajax({
        type: "PUT",
        data: data,
        url: '/api/clients/' + client_id + '/password',
        success: callback
    });

}