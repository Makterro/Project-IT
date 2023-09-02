//require Map.js

$('#addMarker').on('click', function () {
    $.ajax({
        url: window.location.pathname,
        method: 'post',
        dataType: 'json',
        data: {
            'lat': lat.val(),
            'lon': lon.val(),
            'obj': $('#id_monitoringObject').val()
        },
        headers: {'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')},
        success: function (data) {

        },
    })
});