<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>
<%! 
   import simplejson

%> 

<%def name="header()"> 
   <title>SMS logs</title>

   ${headers.load_slickGrid(request)}
   
   <script type="text/javascript">
     var grid; 
     var dataView; 

     function comparer(a,b) {
       var x = a[sortcol], y = b[sortcol];
       return (x == y ? 0 : (x > y ? 1 : -1));
     }        


     $(document).ready(function(){ 

       $(".buttons li a").button();        

       
       var columns = [
         {"field": "type", "sortable": true, "id": "type", "name": "Type"},
         {"field": "id", "sortable": true, "id": "id", "name": "Id"},
         {"field": "date", "sortable": true, "id": "date", "name": "Date"},
         {"field": "sent", "sortable": true, "id": "sent", "name": "Sent"},
         {"field": "number", "sortable": true, "id": "number", "name": "Number"},
         {"field": "incoming", 
          "sortable": true, "id": "incoming", "name": "Incoming"},
         {"field": "text", "sortable": true, "id": "text",
          "width": 500,
          "name": "Text"}]; 

       var data = ${simplejson.dumps(messages)}; 

       var options = {
         selectedCellCssClass: "selected",         
         autoHeight: true,
         rowHeight: 64,         
         enableCellNavigation: true,
         enableColumnReorder: true,
         forceFitColumns: true,         
         
       };
        
       dataView = new Slick.Data.DataView();
       
       grid = new Slick.Grid($('#sms-grid'),dataView.rows,columns,options)
        

       grid.onSort.subscribe(function(e, data) {
         console.log("stuff"); 
       }); 

       dataView.onRowCountChanged.subscribe(function(args) {
	 grid.updateRowCount();
         grid.render();
       });

       dataView.onRowsChanged.subscribe(function(rows) {         
         grid.invalidateRows(rows);         
	 grid.render();
       });

       // Load some data into the grid
       dataView.setItems(data);

      });     
   </script>
            
 
</%def>

<%def name="content()"> 
   <ul class="buttons">
     <li> 
       <a href="${request.application_url}/sms/remove_all">Remove all
       messages</a> </li>
     <li>
       <a href="${request.application_url}/sms/received">Outgoing
         queue</a> 
     </li>
   </ul>

  <div id="sms-grid" class="grid">
    
  </div>
     
</%def>
