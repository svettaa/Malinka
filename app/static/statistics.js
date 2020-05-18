
function fillBaseStatistics(result){
        $('#message').html('');

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        $('#users-amount').html(data['users']);
        $('#masters-amount').html(data['masters']);
}

function fillIntervalStatistics(result){

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
}

function getBaseData() {
    $.ajax({
                    type: "GET",
                    url: "/get_base_statistics",
                    data: {},
                    success: fillBaseStatistics,
                    error: function(error) {
                        console.log(error);
                    }
    });
}

function getIntervalData() {
    var start = $('#statistics-start-input').val();
    var end = $('#statistics-end-input').val();

    $.ajax({
                    type: "GET",
                    url: "/get_interval_statistics",
                    data: {'date_start': start, 'date_end': end},
                    success: fillIntervalStatistics,
                    error: function(error) {
                        console.log(error);
                    }
    });
}

$(document).ready(function () {

    getBaseData();

    setMonthStartVal($('#statistics-start-input'));
    setCurrentDateVal($('#statistics-end-input'));

    getIntervalData();
    $('#statistics-start-input').focusout(getIntervalData);
    $('#statistics-end-input').focusout(getIntervalData);

});

