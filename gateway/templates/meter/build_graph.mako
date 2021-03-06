
<%inherit file="../base.mako"/>

<%def name="header()">
<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
  <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>

  <script>
  $(document).ready(function() {
    $("#datepicker-from").datepicker();
    $("#datepicker-to").datepicker();
  });
  </script>

    <title>Meter Page</title>
</%def>

<%def name="content()">
<h3>Build Graph For The Meter</h3>

<table class="no-border" border="0">
  <form method="POST" id="" 
        action="${request.application_url}/meter/show_graph/${meter.uuid}">
        
        <h4> Select the Y Axis</h4>
        <input type="radio" name="yaxis" value="power" 
               checked> Power Consumption </input> <br>
        <input type="radio" name="yaxis" 
               value="credit">Credit Balance </input> <br>
        <input type="radio" name="yaxis" 
               value="watt">Watt-Hour Consumption </input> <br>               
        <h4> Select The Date Range</h4>
            <table>
              <tr>
                <td><strong>From</strong>
                  <input type="text" id="datepicker-from" 
                       name="from" /> 
                </td>
                <td> <strong>To</strong>
                  <input type="text" id="datepicker-to" 
                       name="to" /> 
                </td>
            </tr>   
            </table>
        <p>
          <input type="submit" name="ok" value="show graph">
        </p>
    </form>

</table>

</%def>
