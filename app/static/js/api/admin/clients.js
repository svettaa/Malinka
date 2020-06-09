

function sendRequestGetClients(callback) {
    $.ajax({
        type: "GET",
        url: "/api/clients",
        success: callback
    });
}

function sendRequestGetClientsNotMasters(callback) {
    $.ajax({
        type: "GET",
        url: "/api/clients/not_masters",
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