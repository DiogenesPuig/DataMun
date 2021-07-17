
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
    
    var li = "<li class='collection-item'><div class='row'><div class='col s2'><a href='/code'>"
    var end_li= "</div></div></li>"
    
    var div = document.getElementById("diagnostics").innerHTML += li + code +  "</div><div class='col s10'>name</a>" + end_li;

    
    
}

function filterDiagnostic(){
    
    document.getElementById("diagnostics").innerHTML = "";
    var value = document.getElementById("name").value
    var end_point = "api/search_diagnostic/?name__icontains=" + value
    filter(end_point,function(data){
        for (i in data){
            addDiagnostic(data[i].code,data[i].name);
        }
    });
}

document.addEventListener('DOMContentLoaded',function () {
    filterDiagnostic()
    var input = document.getElementById("name");
    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function(event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("btn_search").click();
    }
    }); 
    var end_point = "api/search_diagnostic/"
    
    filter(end_point,function(data){
        var elems = document.querySelectorAll('.autocomplete');
        
        var data_qs = "{"
        for (i in data){
            
            data_qs += "\""+data[i].name.replace("            ","").replace("\"","") + "\":null,\n"
        }
        
        data_qs += "}";
        data_qs = data_qs.replace(",\n}","}")
        
        
        
        var obj = JSON.parse(data_qs)
        
        var instances = M.Autocomplete.init(elems, {data: obj,onAutocomplete:function(){filterDiagnostic()} });
    });
    
});




function addCenter(code,name,coordinate){
    
    var li = "<li class='collection-item'><div class='row valign-wrapper'><div class='col s2'>"
    var end_li= "</div><a href='#!' class='secondary-content btn'>Editar cordenadas<i class='material-icons right'>edit</i></a></div></li>"
    
    var div = document.getElementById("centers").innerHTML += li + code +  "</div><div class='col s5'>" + name +  "</div><div class='col s5'>" + coordinate + end_li;
}

function filterCenter(){
    
    document.getElementById("centers").innerHTML = "";
    var value = document.getElementById("name").value
    var end_point = "api/search_center/?name__icontains=" + value
    filter(end_point,function(data){
        for (i in data){
            addCenter(data[i].code,data[i].name,data[i].coordinate);
        }
    });
}

document.addEventListener('DOMContentLoaded',function () {
    filterCenter()

    var input = document.getElementById("name");
    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function(event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("btn_search").click();
    }
    }); 
    
    var end_point = "api/search_center/"
    
    filter(end_point,function(data){
        var elems = document.querySelectorAll('.autocomplete');
        
        var data_qs = "{"
        for (i in data){
            
            data_qs += "\""+data[i].name + "\":null,"
        }

        data_qs += "}";
        data_qs = data_qs.replace(",}","}")
        
        
        var obj = JSON.parse(data_qs)
        
        var instances = M.Autocomplete.init(elems, {data: obj,onAutocomplete:function(){filterCenter()} });
    });
    
});






    












