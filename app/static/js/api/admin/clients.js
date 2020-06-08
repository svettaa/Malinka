

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