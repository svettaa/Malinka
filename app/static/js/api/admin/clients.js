

function sendRequestGetClients(callback) {
    $.ajax({
        type: "GET",
        url: "/api/clients",
        success: callback
    });
}