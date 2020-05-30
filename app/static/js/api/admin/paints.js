

function sendRequestGetAllPaints(callback) {
    $.ajax({
        type: "GET",
        url: "/api/paints",
        success: callback
    });
}