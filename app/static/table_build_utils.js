
    const START_H = 9;
    const START_M = 0;
    const END_H = 20;
    const END_M = 0;
    const interval = 10;
    const edge = 60;

    function buildTimeTable(tableWrapper){
        tableWrapper.html('<thead>' +
            '<tr>' +
            '    <th scope="col" style="width:0px;">Час</th>' +
            '    <th scope="col">Подія</th>' +
            '</tr>' +
            '</thead>' +
            '<tbody></tbody>');
        const table = tableWrapper.find('tbody').eq(0);

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

    function getRow(timeStr){
         time_h = parseInt(timeStr.substring(0, 2));
         time_m = parseInt(timeStr.substring(3));
         while(time_m % interval != 0){
              time_m--;
         }

         var full_h = (time_h - START_H) * (60 / interval) - START_M / interval;
         var more_m = time_m / interval;
         return full_h + more_m;
    }

    function addAppointment(tableWrapper, appointment) {

                start_time = appointment['appoint_start'].substring(11);
                end_time = appointment['appoint_end'].substring(11);

                start_index = getRow(start_time);
                end_index = getRow(end_time);

                tableWrapper.find('.appointment').eq(start_index).append(
                    'Час: ' +
                    appointment['appoint_start'].substring(11) +
                    ' - ' +
                    appointment['appoint_end'].substring(11) +
                    '<br>' +
                    'Процедура: ' +
                    appointment['procedure_name'] +
                    '<br>' +
                    'Клієнт: ' +
                    appointment['client_surname'] + ' ' + appointment['client_first_name'] +
                    '<br>' +
                    'Статус: ' +
                    (appointment['status'] ? 'Підтверджено' : 'Не підтверджено') +
                    '<br>'
                );

                tableWrapper.find('td.appointment').eq(start_index)
                    .attr('rowspan', Math.max(end_index - start_index, 1));
                for(var i = start_index + 1; i < end_index; i++){
                    $('#mainTable td.appointment').eq(i).css('display', 'none');
                }
    }