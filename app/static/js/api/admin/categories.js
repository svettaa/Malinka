
function sendRequestGetAllCategories(callback) {
    $.ajax({
        type: "GET",
        url: "/api/categories",
        success: callback
    });
}


function sendRequestGetCategory(id, callback) {
    $.ajax({
        type: "GET",
        url: "/api/categories/" + id,
        success: callback
    });
}

function sendRequestAddCategory(data, callback) {
    $.ajax({
        type: "POST",
        url: "/api/categories",
        data: data,
        success: callback
    });
}



function sendRequestDeleteCategory(id, callback) {
    $.ajax({
        type: "DELETE",
        url: "/api/categories/" + id,
        success: callback
    });
}

function sendRequestEditCategory(id, data, callback) {
    $.ajax({
        type: "PUT",
        url: "/api/categories/" + id,
        data: data,
        success: callback
    });
}