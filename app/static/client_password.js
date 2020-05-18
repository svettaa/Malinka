
function showPasswordMessage(result){
    if (result['status'] === true) {
        showSuccess(result['message']);
    } else {
        showError(result['message']);
    }
}

function resetPassword(){
    const id = $(this).val();

    $.ajax({
                    type: "GET",
                    url: "/reset_password",
                    data: {'id': id},
                    success: showPasswordMessage,
                    error: function(error) {
                        console.log(error);
                    }
    });
}

$(document).ready(function(){
    $('#reset-password').on('click', resetPassword);
});