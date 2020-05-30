

function sendRequestGetAppointmentPaints(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/appointments/" + id + "/paints",
        success: callback
    });
}

function sendRequestGetAppointmentPaint(appointmentID, paintID, callback) {
    $.ajax({
        type: "GET",
        url: "/api/appointments/" + appointmentID + "/paints/" + paintID,
        success: callback
    });
}

function sendRequestAddAppointmentPaint(appointmentID, data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/appointments/" + appointmentID + "/paints",
        data: data,
        success: callback
    });
}

function sendRequestEditAppointmentPaint(appointmentID, paintID, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/appointments/" + appointmentID + "/paints/" + paintID,
        data: data,
        success: callback
    });
}

function sendRequestDeleteAppointmentPaint(appointmentID, paintID, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/appointments/" + appointmentID + '/paints/' + paintID,
        success: callback
    });
}