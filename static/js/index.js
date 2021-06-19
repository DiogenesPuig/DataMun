
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





function clearResults(id){

    var results = document.getElementById(id).innerHTML = "";
}
function addCenter(code,name,coordinate){
    
    var li = "<li class='collection-item'>"
    var end_li = '</ul>'
    var div = "<div class='col s4'>"
    var end_div= "</div>"
    
    var div = document.getElementById("centers").innerHTML += li + div + code +end_div +  div + name +end_div + div + coordinate +end_div + end_li;
}

function search(name,fileds) {
    clearResults("centers")
    
    var end_point = "api/search_center/?"+fileds+"=" + name 
    $.ajax({
        url: end_point,
        dataType: "json",
        success: function(data){
            for (i in data){
                addCenter(data[i].code,data[i].name,data[i].coordinate);
            }
        },
        error: function(error_data){
            console.log("error")
            console.log(error_data)
        },
    })
    

}
function searchCenter(){
    var value = document.getElementById("name").value
    search(value,"name__icontains")
}

searchCenter()



    
