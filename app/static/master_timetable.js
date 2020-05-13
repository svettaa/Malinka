
$(document).ready(function () {
    var master_socket = io('http://127.0.0.1:5000/master')

    function get_timetable(){
        var msg = $('#master-timetable-input').val();
        master_socket.emit('get_master_timetable', msg);
    }

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    var dateStr = dd + '.' + mm + '.' + yyyy;
    $('#master-timetable-input').val(dateStr);

    get_timetable();
    $('#master-timetable-input').focusout(get_timetable);

    var START_H = 9;
    var START_M = 0;
    var END_H = 20;
    var END_M = 0;
    var interval = 10;
    var edge = 60;

    function buildTimeTable(table){
        table.html('')
        var h = START_H;
        var m = START_M;

        while(h != END_H || m != END_M){
            if(m % edge == 0){
                table.append(
                    '<tr style="height:25px;"><td rowspan="' + (edge / interval) + '">' +
                    String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') +
                    '</td><td class="appointment"></td></tr>'
                );
            } else {
                table.append(
                    '<tr style="height:25px;"><td class="appointment"></td></tr>'
                );
            }
            m += interval;
            if(m == 60){
                h += 1;
                m = 0;
            }
        }
    }

    function getRow(time){
         time_h = parseInt(time.substring(0, 2));
         time_m = parseInt(time.substring(3));
         while(time_m % interval != 0){
              time_m--;
         }

         var full_h = (time_h - START_H) * (60 / interval) - START_M / interval;
         var more_m = time_m / interval;
         return full_h + more_m;
    }



    master_socket.on('get_master_timetable', function(result){

        $('#message').html('');
        buildTimeTable($('#mainTable > tbody'));

        var status = result['status'];
        var message = result['message'];
        var data = result['data'];

        if(status == false){
            $('#message').html('<div class="alert alert-danger" role="alert">' + message + '</div>');
        } else {
            $.each(data, function(){

                start_time = this['appoint_start'].substring(11);
                end_time = this['appoint_end'].substring(11);

                start_index = getRow(start_time);
                end_index = getRow(end_time);

                $('.appointment').eq(start_index).append(
                    'Час: ' +
                    this['appoint_start'].substring(11) +
                    ' - ' +
                    this['appoint_end'].substring(11) +
                    '<br>' +
                    'Процедура: ' +
                    this['procedure_name'] +
                    '<br>' +
                    'Клієнт: ' +
                    this['client_surname'] + ' ' + this['client_first_name'] +
                    '<br>' +
                    'Статус: ' +
                    (this['status'] ? 'Підтверджено' : 'Не підтверджено') +
                    '<br>'
                );

                $('#mainTable td.appointment').eq(start_index)
                    .attr('rowspan', Math.max(end_index - start_index, 1));
                for(var i = start_index + 1; i < end_index; i++){
                    $('#mainTable td.appointment').eq(i).css('display', 'none');
                }
            });
        }
    });
});
