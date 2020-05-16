function setCurrentDateVal(inputObj) {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    var dateStr = dd + '.' + mm + '.' + yyyy;
    inputObj.val(dateStr);
}

function setMonthStartVal(inputObj) {
    var today = new Date();
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    var dateStr = '01.' + mm + '.' + yyyy;
    inputObj.val(dateStr);
}