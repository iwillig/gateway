<%inherit file="../base.mako"/>


<%!
  import simplejson
%>


<%def name="header()"> 
    <title>Circuit Page</title>
    <script type="text/javascript" src="/static/highcharts/highcharts.js"></script>
    <script type="text/javascript">


      var units = ${y_units};
      //var x_pruned =[1,2,3,4];
      var data = ${simplejson.dumps(data)} ; 
      var to = ${str(to)};
      var origin =${str(origin)}
      var origin_date=new Date(origin);
      var to_date= new Date(to);
      origin_date=Date.UTC(origin_date.getFullYear(),origin_date.getMonth(),origin_date.getDay());
      to_date=Date.UTC(to_date.getFullYear(),to_date.getMonth(),to_date.getDay());
      var chart;
		jQuery(document).ready(function() {
			chart = new Highcharts.Chart({
				chart: {
					renderTo: 'container',
					defaultSeriesType: 'line',
					marginRight: 130,
					marginBottom: 45
				},
				title: {
					text: 'time vs '+units+' chart',
					x: -20 //center
				},
				subtitle: {
					text: 'Shared Solar',
					x: -20
				},
				xAxis: {
					title: {
						text: "Time Line"
					},
					type: 'datetime',
					showLastTickLabel: true,
					maxZoom: 0,
					//categories: x_pruned,
					/*labels: {
            					rotation: 45,
            					style: {
                					font: 'normal 13px Verdana, sans-serif'
            				}
            				}*/
            				plotBands: [{
              						 from: origin_date,
              						 to: to_date
            				}]

					
				},
				yAxis: {
					title: {
						text: units
					},
					plotLines: [{
						value: 0,
						width: 1,
						color: '#808080'
					}]
				},
				tooltip: {
				  formatter: function() {
			            return '<b>'+ this.series.name +'</b><br/>'+ new Date(this.x) +': '+ this.y;
				  }
				},
				legend: {
					layout: 'vertical',
					align: 'right',
					verticalAlign: 'top',
					x: -10,
					y: 100,
					borderWidth: 0
				},
				series: [{
					name: 'Circuit 1',
					type: 'area',
                                        pointInterval: 100 * 3600 * 1000,
					pointStart: origin_date,
                                        pointEnd: to_date,
					data: y
				}]
			});
			
			
		});

    </script>
</%def> 
<%def name="content()"> 
<h2>View graphs here</h2>
<div id="container" style="width: 800px; height: 400px; margin: 0 auto"></div>

</%def> 
