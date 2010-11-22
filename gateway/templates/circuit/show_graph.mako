<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
    <script type="text/javascript" src="/static/highcharts/highcharts.js"></script>
    <script type="text/javascript" src="/static/use.js"></script>
    <script type="text/javascript">
      //var x=[1,2,3,4];
      //var y=[1,2,3,4];		
      var x = ${str(x)} ; 
      var y = ${str(y)} ; 
      var chart;
		jQuery(document).ready(function() {
			chart = new Highcharts.Chart({
				chart: {
					renderTo: 'container',
					defaultSeriesType: 'line',
					marginRight: 130,
					marginBottom: 25
				},
				title: {
					text: 'Circuit Graph',
					x: -20 //center
				},
				subtitle: {
					text: 'Shared Solar',
					x: -20
				},
				xAxis: {
					categories: x
				},
				yAxis: {
					title: {
						text: 'Units'
					},
					plotLines: [{
						value: 0,
						width: 1,
						color: '#808080'
					}]
				},
				tooltip: {
					formatter: function() {
			                return '<b>'+ this.series.name +'</b><br/>'+
							this.x +': '+ this.y;
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
					data: y
				}]
			});
			
			
		});

    </script>
</%def> 
<%def name="content()"> 
<h2>Make graphs here</h2>
<div id="container" style="width: 800px; height: 400px; margin: 0 auto"></div>

</%def> 
