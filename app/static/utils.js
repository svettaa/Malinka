function showError(message) {
    $('#message').html('<div class="alert alert-danger" role="alert">' + message + '</div>');
}

function clearMessages() {
    $('#message').html('');
}