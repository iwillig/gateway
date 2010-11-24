                <%inherit file="../base.mako"/>

<%def name="header()"> 
   <script type="text/javascript" 
           src="${request.application_url}/static/SlickGrid/lib/jquery.event.drag-2.0.min.js"></script>   
   <script 
      type="text/javascript" 
      src="${request.application_url}/static/SlickGrid/slick.grid.js"></script>
   
   <link rel="stylesheet" 
         href="${request.application_url}/static/css/slick.grid.css" 
         type="text/css" 
         media="screen"  />

   <script type="text/javascript">
     var grid ; 
     var columns = ${grid_header};
     var data = ${data} 

     $(document).ready(function() {
      var options = {
          enableColumnReorder: true, 
      };
     grid = new Slick.Grid($("#sms-grid"), data, columns, options);
      });     

   </script>

   <title>SMS logs</title>
</%def>

<%def name="content()"> 
   <ul>
     <li> 
       <a href="${request.application_url}/sms/remove_all">Remove all
       messages</a> </li>
     <li>
       <a href="${request.application_url}/sms/received">Outgoing
         queue</a> 
     </li>
   </ul>
   <div id="sms-grid" style="height:500px;"></div>
   </table> 
</%def>
