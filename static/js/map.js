
function initMap() {
    // Create the map.
    const cordoba ={ lat: -31.4067538, lng:-64.2041696};
    const map = new google.maps.Map(document.getElementById("map"), {
        
        zoom: 11.75,
        center: cordoba,
        mapTypeId: "terrain",
    });
    
    const service = new google.maps.places.PlacesService(map);
    
    
    var i = 1;
    for (const c in centers) {
        const r= Math.round( 255/length *i*2);
        const g=Math.round(  255 - (255/length) *i);
        const b=Math.round( 255/length *i);
        i = i+1;
        const color = 'rgb('+r+','+g+','+b+')';
        console.log(color)
        const plac = {
            query: centers[c].name,
            fields: ["name", "geometry"],
        };
        

        const centerCircle = new google.maps.Circle({
            strokeColor: color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: color,
            fillOpacity: 0.35,
            map,
            center: { lat: centers[c].lat, lng: centers[c].lon },
            radius: Math.sqrt(centers[c].cases) * 100,
            description: centers[c].cases,
        });
        const contentString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h5 id="firstHeading" class="firstHeading">'+centers[c].name+'</h5>' +
        '<div id="bodyContent">' +
        '<p><b>'+centers[c].name+' es el centro N°' +  centers[c].code+ '</b><br>'+
        'Se realizaron ' + centers[c].cases + ' diagnosticos</p>'+
        '<a href="/centers/' + centers[c].code + '" class="secondary-content btn">Editar centro<i class="material-icons right">edit</i></a>' +
        "</div>" +
        "</div>";
        const infowindow = new google.maps.InfoWindow({
            content: contentString,
            maxWidth: 200,
        });

        const marker = new google.maps.Marker({
            position: { lat: centers[c].lat, lng: centers[c].lon },
            map,
            title: centers[c].name,
        });
        centerCircle.addListener("click", () => {
            infowindow.open(map, marker);
        });
        marker.addListener("click", () => {
            infowindow.open(map, marker);
        });
    }
}
function editMarker(){
    const cordoba ={ lat: -31.4067538, lng:-64.2041696};
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: cordoba,
        mapTypeId: "terrain",
    });
    let name = document.getElementById("id_name").value;
    let lat = document.getElementById("id_latitude");
    let lng = document.getElementById("id_longitude");
    let position = { lat: parseFloat(lat.value), lng: parseFloat(lng.value)};
    console.log(position)
    let center_marker = new google.maps.Marker({
        position: position,
        label: name,
        map: map,
    });
    
    // This event listener calls addMarker() when the map is clicked.
    google.maps.event.addListener(map, "click", (event) => {
        center_marker.setPosition(event.latLng)
        
    });
    let button = document.getElementById("ok")
    button.addEventListener("click", function() {
        center_marker.getPosition().toJSON()
        lat.value = center_marker.getPosition().toJSON().lat;
        lng.value = center_marker.getPosition().toJSON().lng;
    });

}
