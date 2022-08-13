function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(my_func);
    } else {
        x.innerHTML = "Geolocation is not supported.";
    }
}

function my_func(position){
    mapOptions.center = [position.coords.latitude, position.coords.longitude];
    marker = L.marker([position.coords.latitude, position.coords.longitude]);
    mapa()
}

var mapOptions = {
    zoom: 15
}

var marker = L.marker([])


function mapa(){
    var map = new L.map('map', mapOptions);
    var layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
    map.addLayer(layer);
    marker.addTo(map)
}