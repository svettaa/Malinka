

function sendRequestGetAllAppointments(callback) {
    $.ajax({
        type: "GET",
        url: "/api/appointments",
        success: callback
    });
}

function sendRequestGetAppointment(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/appointments/" + id,
        success: callback
    });
}

function sendRequestAddAppointment(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/appointments",
        data: data,
        success: callback
    });
}

function sendRequestEditAppointment(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/appointments/" + id,
        data: data,
        success: callback
    });
}

function sendRequestDeleteAppointment(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/appointments/" + id,
        success: callback
    });
}