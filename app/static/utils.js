function showSuccess(message) {
    $('#message').html('<div class="alert alert-success" role="alert">' + message + '</div>');
}

function showError(message) {
    $('#message').html('<div class="alert alert-danger" role="alert">' + message + '</div>');
}

function clearMessages() {
    $('#message').html('');
}