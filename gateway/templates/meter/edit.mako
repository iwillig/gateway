<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Edit ${meter.name}</title>
</%def>

<%def name="content()"> 
<h3>Edit ${meter.name}</h3> 
<table class="form">
  <form method="POST" id="add-meter" 
        action="${request.application_url}/update_meter">
    <table>      
    % for k,v in form.iteritems(): 
    <tr>     
      <td>${k}</td>
      <td><input type="${v.get("type")}" name="${k}"
                value="${v.get("value")}" /></td>
    </tr>
    % endfor 

    </table>
</form>

</%def> 
