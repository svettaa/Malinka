

function sendRequestGetAllProcedure(callback) {
    $.ajax({
        type: "GET",
        url: "/api/procedures",
        success: callback
    });
}

function sendRequestGetProcedure(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/procedures/" + id,
        success: callback
    });
}

function sendRequestAddProcedure(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/procedures",
        data: data,
        success: callback
    });
}

function sendRequestEditProcedure(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/procedures/" + id,
        data: data,
        success: callback
    });
}

function sendRequestDeleteProcedure(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/procedures/" + id,
        success: callback
    });
}