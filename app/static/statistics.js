
$(document).ready(function () {

    var statistics_socket = io('http://127.0.0.1:5000/statistics');

    statistics_socket.emit('get_base_statistics');

    statistics_socket.on('get_base_statistics', function(result){
        $('#message').html('');

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        $('#users-amount').html(data['users']);
        $('#masters-amount').html(data['masters']);
    });

    function get_interval_statistics(){
        var start = $('#statistics-start-input').val();
        var end = $('#statistics-end-input').val();
        statistics_socket.emit('get_interval_statistics', [start, end]);
    }

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    var endDateStr = dd + '.' + mm + '.' + yyyy;
    var startDateStr = '01.' + mm + '.' + yyyy;
    $('#statistics-start-input').val(startDateStr);
    $('#statistics-end-input').val(endDateStr);

    get_interval_statistics();
    $('#statistics-start-input').focusout(get_interval_statistics);
    $('#statistics-end-input').focusout(get_interval_statistics);

    statistics_socket.on('get_interval_statistics', function(result){
        $('.added-block').remove();
        $('.stat-number').html('-');
        $('#message').html('');

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        if(status == false){
            $('#message').html('<div class="alert alert-danger" role="alert">' + message + '</div>');
        } else {

            $('#appointments-amount').html(data['appointments']);
            $('#money-amount').html(data['money']);
            $('#paints-amount').html(data['paints']);
            $('#supplies-amount').html(data['supplies']);

            $.each(data['appointments-by-master'], function(){
                $('#all-appointments').append(
                '<div class="col-md-3 stat-label added-block">' +
                this['surname'] + ' ' + this['first_name'] +
                '</div>' +
                '<div class="col-md-9 stat-number added-block">' +
                this['amount'] +
                '</div>');
            });
            $.each(data['money-by-master'], function(){
                $('#all-money').append(
                '<div class="col-md-3 stat-label added-block">' +
                this['surname'] + ' ' + this['first_name'] +
                '</div>' +
                '<div class="col-md-9 stat-number added-block">' +
                this['sum_price'] +
                '</div>');
            });
            $.each(data['paints-by-paints'], function(){
                $('#all-paints').append(
                '<div class="col-md-3 stat-label added-block">' +
                this['code'] + ' ' + this['name'] +
                '</div>' +
                '<div class="col-md-9 stat-number added-block">' +
                this['amount'] +
                '</div>');
            });
            $.each(data['supplies-by-paints'], function(){
                $('#all-supplies').append(
                '<div class="col-md-3 stat-label added-block">' +
                this['code'] + ' ' + this['name'] +
                '</div>' +
                '<div class="col-md-9 stat-number added-block">' +
                this['amount'] +
                '</div>');
            });
        }
    });

});

