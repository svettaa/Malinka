function clearTabs(ulObject) {
    ulObject.html('')
}

function clearTabsContent(divObject) {
    divObject.html('')
}

function addTab(ulObject, href, title) {
    ulObject.append(
        '<li class="nav-item">' +
        '<a class="nav-link" data-toggle="tab" href="#' + href + '">' + title + '</a>' +
        '</li>'
    );
}

function buildTabContent(divObject, id) {
    var newTabContent = $('<div class="tab-pane fade"></div>');
    newTabContent.attr('id', id);
    divObject.append(newTabContent);
    return newTabContent;
}