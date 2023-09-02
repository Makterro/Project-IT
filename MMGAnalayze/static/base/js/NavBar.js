$(document).ready(function () {
    const title = $(document).attr('title');
    const navElement = $(`a:contains("${title}")`)
    if (navElement.length) {
        navElement.removeClass('text-white').addClass('text-secondary');
        navElement.find('a').href = '#';
    }
})