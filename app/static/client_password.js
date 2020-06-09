
function showPasswordMessage(result){
    if (result['status'] === true) {
        showSuccess(result['message']);
    } else {
        showError(result['message']);
    }
}

$(document).ready(function(){
    $('#reset-password').on('click', resetPassword);
    $('#delete-password').on('click', deletePassword);
});