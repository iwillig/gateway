<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Edit ${meter.name}</title>
   <script type="text/javascript">
     $(function() { 
       $('#update_meter').button(); 
     });
   </script>
</%def>

<%def name="content()"> 
<h3>Edit meter: <span class="underline">${meter.name}</span></h3> 
<table class="form">
  <form method="POST" id="add-meter" 
        action="${request.application_url}/meter/update/${meter.slug}">
    <table>      
    % for k,v in fields.iteritems(): 
        % if k != "Id": 
       <tr>     
         <td><label>${k}</label></td>
         <td><input type="text" name="${v.get("name")}"
                value="${v.get("value")}" /></td>
       </tr>
       % endif 
    % endfor 
       <tr>
         <td></td>
         <td><input id="update_meter" type="submit" name="submit" value="Update meter" /></td>
       </tr>
    </table>
</form>

</%def> 
