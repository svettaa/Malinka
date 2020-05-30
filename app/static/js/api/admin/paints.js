

function sendRequestGetAllPaints(callback) {
    $.ajax({
        type: "GET",
        url: "/api/paints",
        success: callback
    });
}

function sendRequestDeletePaint(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/paints/" + id,
        success: callback
    });
}

function sendRequestEditPaint(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/paints/" + id,
        data: data,
        success: callback
    });
}


function sendRequestGetPaint(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/paints/" + id,
        success: callback
    });
}

function sendRequestAddPaint(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/paints",
        data: data,
        success: callback
    });
}

