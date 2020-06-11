function showSuccess(message) {
    $('#message').html('<div class="alert alert-success" role="alert">' + message + '</div>');
}

function showError(message) {
    $('#message').html('<div class="alert alert-danger" role="alert">' + message + '</div>');
}

function clearMessages() {
    $('#message').html('');
}

function showSuccessBlock(block, message) {
    block.html('<div class="alert alert-success" role="alert">' + message + '</div>');
}

function showErrorBlock(block, message) {
    block.html('<div class="alert alert-danger" role="alert">' + message + '</div>');
}

function clearMessagesBlock(block) {
    block.html('');
}

function initDataTable(table) {
    table.DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.20/i18n/Ukrainian.json"
        }
    });
}

function createIcon(id, className) {
    const span = $('<span></span>');
    span.addClass('table-icon');
    span.addClass(className);
    span.attr('value', id);
    return span;
}

function createIconsTd(id, iconClassNames) {
    const td = $('<td></td>');
    const div = $('<div></div>');
    td.append(div);

    div.css('width', '60px');
    div.addClass('d-flex');
    div.addClass('justify-content-between');

    for (var i = 0; i < iconClassNames.length; i++) {
        div.append(createIcon(id, iconClassNames[i]));
    }

    return td;
}

function createTd(text) {
    const td = $('<td></td>');
    td.html(text);
    return td;
}

function createH5(text) {
    const td = $('<h5></h5>');
    td.html(text);
    return td;
}

function createDateTd(text) {
    const year = text.substring(6);
    const month = text.substring(3, 5);
    const day = text.substring(0, 2);

    const invisible = $('<span></span>');
    invisible.css('display', 'none');
    invisible.html(year + '.' + month + '.' + day);

    const td = $('<td></td>');
    td.append(invisible);
    td.append(text);
    return td;
}

function createDateTimeTd(text) {
    const year = text.substring(6, 10);
    const month = text.substring(3, 5);
    const day = text.substring(0, 2);
    const hour = text.substring(11, 13);
    const min = text.substring(14);

    const invisible = $('<span></span>');
    invisible.css('display', 'none');
    invisible.html(year + '.' + month + '.' + day + ' ' + hour + ':' + min);

    const td = $('<td></td>');
    td.append(invisible);
    td.append(text);
    return td;
}

function createIconTh() {
    const th = $('<th style="width:60px;"></th>');
    th.attr('scope', 'col');
    return th;
}

function createTh(text) {
    const th = $('<th></th>');
    th.attr('scope', 'col');
    th.html(text);
    return th;
}

function createHeaderTable(headers) {
    const table = $('<table></table>');
    table.addClass('table');
    table.addClass('table-bordered');
    table.addClass('table-responsive-lg');

    const thead = $('<thead></thead>');
    const tbody = $('<tbody></tbody>');
    table.append(thead);
    table.append(tbody);

    const tr = $('<tr></tr>');
    thead.append(tr);

    tr.append(createIconTh());
    for (var i = 0; i < headers.length; i++) {
        tr.append(createTh(headers[i]));
    }

    return table;
}

function getDateFromDatetime(datetime) {
    return datetime.substring(0, 10);
}

function getTimeFromDatetime(datetime) {
    return datetime.substring(11, 16);
}

function initDatePicker(element) {
    element.datetimepicker({
        locale: 'ru',
        format: 'L'
    });
}

function initTimePicker(element) {
    element.datetimepicker({
        locale: 'ru',
        format: 'LT'
    });
}

function getCurrentDay() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    return dd + '.' + mm + '.' + yyyy;
}

function getNearestTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();

    if(m !== 0){
        m = 0;
        h++;
    }

    if(h >= 24){
        h %= 24;
    }

    return String(h) + ':' + String(m).padStart(2, '0');
}

function fillSelectWithList(select, list) {
    select.html('');
    for(var i = 0; i < list.length; i++){
        select.append(list[i]);
    }
    select.selectpicker('refresh');
}

