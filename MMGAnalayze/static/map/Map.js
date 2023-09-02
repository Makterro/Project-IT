const defaultLat = 65.0;
const defaultLon = 100.0;

const map = L.map('map').setView([defaultLat, defaultLon], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>|Leaflet',
    minZoom: 5,
}).addTo(map);

const southWest = L.latLng(41.1856, 19.6384);
const northEast = L.latLng(81.8582, 190.0953);
const bounds = L.latLngBounds(southWest, northEast);
map.setMaxBounds(bounds);

const resetBtn = document.getElementById('resetBtn');
resetBtn.addEventListener('click', function () {
    map.setView([defaultLat, defaultLon], 4);
});

//cursor
let lastCursor = null;
const lat = $('#id_lat');
const lon = $('#id_lon');

function onMapClick(e) {
    SetCursor(e.latlng);
}
map.on('click', onMapClick);
lat.add(lon).on('change paste keyup', function() {
    SetCursor([lat.val(), lon.val()])
});

function SetCursor(coordinates){
    lat.val(coordinates.lat);
	lon.val(coordinates.lng);
    if (lastCursor)
        lastCursor.remove();
    lastCursor = L.marker(coordinates).addTo(map);
}

function SetCursorToDefault(){
    let coordinates = L.latLng(defaultLat, defaultLon);
    SetCursor(coordinates);
}

$('#addMarker').on('click', function () {
    let obj = $('#id_monitoringObject option:selected');
    if (!obj.val()) return;
    const marker = L.marker([lat.val(), lon.val()]).addTo(map);
    marker.bindPopup(obj.text()).openPopup();
    SetCursorToDefault();
});

$(document).ready(SetCursorToDefault)