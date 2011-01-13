function loadPage() {

  var r; 
  var y = [[1, 20, 40, 60, 80, 100, 125]]; 
  var x = [[1, 20, 40, 60, 80, 100, 120]];

  $('.buttons li').button();
  $('#add-circuit').button(); 
  r = Raphael("graph"); 
    
  var chart = r.g.linechart(30, 10, 650, 220, x, y,
                    {nostroke: false, 
                     axis: "0 0 1 1", symbol: "o", smooth: true});
  chart.hoverColumn(
    function() {console.log(this),
    function() {console.log(this)}})

  $('#showJobButton').click(function() { 
    $('#showJobs').dialog({
      title: "Active jobs",
      modal: true,
      height: 500,
      width: 500
    });           

  }); 
  
  $('#addCircuitButton').click(function() { 
    $('#addCircuit').dialog({
      title: "Add circuit to meter",
      modal: true,
      height: 500,
      width: 500
    });               
  });
}; 
