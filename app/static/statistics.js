
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

    setMonthStartVal($('#statistics-start-input'));
    setCurrentDateVal($('#statistics-end-input'));

    get_interval_statistics();
    $('#statistics-start-input').focusout(get_interval_statistics);
    $('#statistics-end-input').focusout(get_interval_statistics);

    statistics_socket.on('get_interval_statistics', function(result){
        $('.added-block').remove();
        $('.stat-number').html('-');
        clearMessages();

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        if(status == false){
            showError(message);
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

