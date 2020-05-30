

function sendRequestGetMasters(callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters",
        success: callback
    });
}