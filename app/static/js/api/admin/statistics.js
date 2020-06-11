

function getBaseData(callback) {
    $.ajax({
        type: "GET",
        url: "/get_base_statistics",
        data: {},
        success: callback
    });
}

function getIntervalData(start, end, callback) {
    $.ajax({
        type: "GET",
        url: "/get_interval_statistics",
        data: {'date_start': start, 'date_end': end},
        success: callback
    });
}