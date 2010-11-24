<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Edit ${meter.name}</title>
</%def>

<%def name="content()"> 
<h3>Edit ${meter.name}</h3> 
<table class="form">
  <form method="POST" id="add-meter" 
        action="${request.application_url}/meter/update/${meter.uuid}">
    <table>      
    % for k,v in fields.iteritems(): 
        % if k != "id": 
       <tr>     
         <td><label>${k}</label></td>
         <td><input type="${v.get("type")}" name="${k.lower()}"
                value="${v.get("value")}" /></td>
       </tr>
       % endif 
    % endfor 
       <tr>
         <td></td>
         <td><input type="submit" name="submit" value="Update meter" /></td>
       </tr>
    </table>
</form>

</%def> 
