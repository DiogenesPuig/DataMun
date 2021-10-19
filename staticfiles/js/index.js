document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems,);
});
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.timepicker');
    var instances = M.Timepicker.init(elems,);
});
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems, {
        direction: 'top',
        hoverEnabled: true
    });
});
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.parallax');
    var instances = M.Parallax.init(elems,);
});
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.tabs');
    var instances = M.Tabs.init(elems, {
        
        swipeable: false,
    });
});
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
});


function filter(end_point,callback) {
    $.ajax({
        url: end_point,
        dataType: "json",
        success: function(data){
            return callback(data);
        },
        error: function(error_data){
            console.log("error")
            console.log(error_data)
        },
    })
}

function addDiagnostic(code,name){
    var li = "<li class='collection-item'><div class='row'><div class='col s2'>"
    var end_li= "</a></div></div></li>"
    var div = document.getElementById("diagnostics").innerHTML += li + code +  "</div><div class='col s10'><a  onclick='loading()' href='/diagnostics/" + code +  "'>" + name + end_li;
}

function filterDiagnostic(){
    document.getElementById("diagnostics").innerHTML = "";
    var value = document.getElementById("name").value
    var end_point = "/api/diagnostics/?name__icontains=" + value
    filter(end_point,function(data){
        for (i in data){
            addDiagnostic(data[i].code,data[i].name);
        }
    });
}

function addCenter(code,name,latitude,longitude){
    var li = "<li class='collection-item'><div class='row valign-wrapper center'><div class='col s1'>"
    var end_li= "</div><div class='col s2'><a href='/centers/" + code + "' class='secondary-content btn'>Editar cordenadas<i class='material-icons right'>edit</i></a></div></div></li>"
    var div = document.getElementById("centers").innerHTML += li + code +  "</div><div class='col s3'>" + name +  "</div><div class='col s3'>" + latitude + "</div><div class='col s3'>" + longitude + end_li;
}

function filterCenter(){
    document.getElementById("centers").innerHTML = "";
    var value = document.getElementById("name").value
    var end_point = "/api/centers/?name__icontains=" + value
    filter(end_point,function(data){
        for (i in data){
            addCenter(data[i].code,data[i].name,data[i].latitude,data[i].longitude);
        }
    });
}