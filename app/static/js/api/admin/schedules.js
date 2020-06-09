

function sendRequestGetAllSchedule(callback) {
    $.ajax({
        type: "GET",
        url: "/api/schedules",
        success: callback
    });
}

function sendRequestGetSchedule(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/schedules/" + id,
        success: callback
    });
}

function sendRequestAddSchedule(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/schedules",
        data: data,
        success: callback
    });
}

function sendRequestEditSchedule(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/schedules/" + id,
        data: data,
        success: callback
    });
}

function sendRequestDeleteSchedule(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/schedules/" + id,
        success: callback
    });
}