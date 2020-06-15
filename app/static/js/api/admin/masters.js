function sendRequestGetAllMasters(callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters",
        success: callback
    });
}

function sendRequestGetAllRelevantMasters(callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters/relevant",
        success: callback
    });
}

function sendRequestRefreshGetMastersDoingWholeCategory(category_id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters/categories/" + category_id,
        success: callback
    });
}

function sendRequestRefreshGetMastersDoingProcedures(callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters/procedures",
        success: callback
    });
}

function sendRequestGetMasterProcedures(master_id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/masters/" + master_id + "/procedures",
        success: function (result) {
            var newResultData = [];

            var lastCategory;
            var currElement;
            $.each(result.data, function () {
                const currCategory = this.category_name;
                if (lastCategory === undefined || lastCategory !== currCategory) {
                    currElement = {};
                    currElement.category_name = currCategory;
                    currElement.procedures = [];
                    lastCategory = currCategory;
                    newResultData.push(currElement);
                }
                currElement.procedures.push({
                    'id': this.procedure_id,
                    'name': this.procedure_name,
                    'duration': this.duration
                });
            })

            result.data = newResultData;
            callback(result);
        }
    });
}

function sendRequestRefreshMasterProcedures(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/masters/" + id + "/procedures",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
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

function sendRequestRefreshMasterPhoto(id, data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/masters/" + id + "/photo",
        contentType: false,
        cache: false,
        processData: false,
        data: data,
        success: callback
    });
}

function sendRequestDeleteMasterPhoto(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/masters/" + id + "/photo",
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