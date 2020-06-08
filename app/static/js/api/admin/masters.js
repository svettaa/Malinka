

function sendRequestGetAllMasters(callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters",
        success: callback
    });
}

function sendRequestGetMastersProcedures(master_id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters/" + master_id + "/procedures",
        success: callback
    });
}

function sendRequestDeleteMaster(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/masters/" + id,
        success: callback
    });
}

function sendRequestEditMaster(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/masters/" + id,
        data: data,
        success: callback
    });
}


function sendRequestGetMaster(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters/" + id,
        success: callback
    });
}

function sendRequestAddMaster(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/masters",
        data: data,
        success: callback
    });
}