

function sendRequestGetAllSupply(callback) {
    $.ajax({
        type: "GET",
        url: "/api/supplies",
        success: callback
    });
}

function sendRequestGetSupply(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/supplies/" + id,
        success: callback
    });
}

function sendRequestAddSupply(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/supplies",
        data: data,
        success: callback
    });
}

function sendRequestEditSupply(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/supplies/" + id,
        data: data,
        success: callback
    });
}

function sendRequestDeleteSupply(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/supplies/" + id,
        success: callback
    });
}