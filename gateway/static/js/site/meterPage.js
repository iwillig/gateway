
var _globalChart;
var _logs; 
var _slider; 

function loadPage(options) {
var r,
  chart,
  x = [[1,2]]
  y = [[1,2]],
  start = 50,
  end   = 100;

  var baseUrl = options['url'] + '/meter/logs/' + options['meter']; 
 
  /*
   * Raphel
   */

//  r = Raphael("graph");
  
  /*
   * Load UI interface
   */ 


  $('.buttons li').button();
  $('#add-circuit').button(); 

  // var slider = $("#graphSlider").slider({
  //   range: true,
  //   values: [start,end],
  //   stop: function(event, ui) {       
  //   } 
  // });
  
  // _slider = slider

  $('#showJobButton').click(function() { 
    $('#showJobs').dialog({
      title: "Active jobs",
      modal: true,
      height: 500,
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

/* $.ajax({
    url: baseUrl,
    success: function(data) { 
      _logs = data;
    }
  });
*/

  // chart = r.g.linechart(30, 10, 650, 220, x, y,
  //                       { nostroke: false, 
  //                        axis: "0 0 1 1", 
  //                        symbol: "o", smooth: true});
  // _globalChart = chart;


}; 
