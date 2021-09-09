
function initMap() {
    // Create the map.
    const map = new google.maps.Map(document.getElementById("map"), {
        
        zoom: 11.75,
        center: { lat: -31.4067538, lng:-64.2041696},
        mapTypeId: "terrain",
    });
    
    const service = new google.maps.places.PlacesService(map);
    
    
    var i = 1;
    for (const c in centersMap) {
        const r= Math.round( 255/length *i*2);
        const g=Math.round(  255 - (255/length) *i);
        const b=Math.round( 255/length *i);
        i = i+1;
        const color = 'rgb('+r+','+g+','+b+')';
        console.log(color)
        const plac = {
            query: centersMap[c].name,
            fields: ["name", "geometry"],
        };
        
        service.findPlaceFromQuery(plac, (results, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK && results) {
                const centerCircle = new google.maps.Circle({
                    strokeColor: color,
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: color,
                    fillOpacity: 0.35,
                    map,
                    center: results[0].geometry.location,
                    radius: Math.sqrt(centersMap[c].cases) * 100,
                    description: centersMap[c].cases,
                });
                const contentString =
                '<div id="content">' +
                '<div id="siteNotice">' +
                "</div>" +
                '<h5 id="firstHeading" class="firstHeading">'+centersMap[c].name+'</h5>' +
                '<div id="bodyContent">' +
                '<p><b>'+centersMap[c].name+' es el centro N°' +  centersMap[c].cod+ '</b><br>'+
                'Se realizaron ' + centersMap[c].cases + ' diagnosticos</p>'+
                "</div>" +
                "</div>";
                const infowindow = new google.maps.InfoWindow({
                    content: contentString,
                    maxWidth: 200,
                });

                const marker = new google.maps.Marker({
                    position: results[0].geometry.location,
                    map,
                    title: centersMap[c].name,
                });
                centerCircle.addListener("click", () => {
                    infowindow.open(map, marker);
                });
                marker.addListener("click", () => {
                    infowindow.open(map, marker);
                });
            }
        });
    }
}
var polygonArray = [];
function editMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
            
        zoom: 11.75,
        center: { lat: -31.4067538, lng:-64.2041696},
        mapTypeId: "terrain",
    });
    var polygonArray = [];
    const drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.MARKER,
        drawingControl: true,
        drawingControlOptions: {
        position: google.maps.ControlPosition.TOP_CENTER,
        drawingModes: [
            google.maps.drawing.OverlayType.MARKER,
            google.maps.drawing.OverlayType.CIRCLE,
            google.maps.drawing.OverlayType.POLYGON,
            google.maps.drawing.OverlayType.POLYLINE,
            google.maps.drawing.OverlayType.RECTANGLE,
        ],
        },
        markerOptions: {
        icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
        },
        circleOptions: {
        fillColor: "#ffff00",
        fillOpacity: 1,
        strokeWeight: 5,
        clickable: false,
        editable: true,
        zIndex: 1,
        },
    });

    drawingManager.setMap(map);

    google.maps.event.addListener(drawingManager, 'polygoncomplete', function (polygon) {
        // assuming you want the points in a div with id="info"
        document.getElementById('info').innerHTML += "polygon points:" + "<br>";
        for (var i = 0; i < polygon.getPath().getLength(); i++) {
            document.getElementById('info').innerHTML += polygon.getPath().getAt(i).toUrlValue(6) + "<br>";
        }
        polygonArray.push(polygon);
        console.log(polygon)

    });
}