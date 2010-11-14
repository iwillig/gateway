
function loadPage(postURL,getURL) { 
 
  populateTable(); 

  function stuff() { 
    alert("stuff"); 
  }; 

  $("#add-circuit").click(function() { 
    var phone = $("#phone").val();
    var energy_max = $("#energy_max").val(); 
    var power_max = $("#power_max").val(); 
    var ip_address = $("#ip_address").val(); 
    $.ajax({
      type: 'POST',
      url: postURL,
      data: {
        "phone" : phone,
        "ip_address" : ip_address,
        "energy_max" : energy_max,
        "power_max": power_max}, 
      success: function(data) { 
        insertTable(data);
      },
      error: function(data) { console.log("error")},
      dataType: "json"
    });
  }); 

  function populateTable() {
    $.getJSON(getURL, function(data) { 
            $.each(data, function(index,value) { 
                    insertTable(value); 
                })
        })}; 

  function insertTable(value) {
    $(".circuits").buildIn("tr",{"id": value.uuid,"class":"circuit"},
                           ["td",{},value.ip_address],
                           ["td",{}, ["a",{"href" : value.url },value.uuid ]],
                           ["td",{},value.pin],
                           ["td",{},"" + value.power_max + ""],
                           ["td",{},"" + value.energy_max + ""]
                          );
  }; 
  

}
