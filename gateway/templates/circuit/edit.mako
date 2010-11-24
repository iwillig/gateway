<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
</%def> 

<%def name="content()"> 
<h3>Circuit  page</h3>

<table>
<form method="POST" id="" 
      action="${request.application_url}/circuit/update/${circuit.uuid}">
  
  % for key,value in fields.iteritems(): 
  
  % if key != "Meter":
     <tr>
       <td><label>${key}</label></td>
       <td><input type="text" 
                  name="${key.lower()}" 
                  value="${value.get("value")}" /></td>
       % endif
       
     </tr>
  % endfor   
     <tr>
       <td></td>
       <td>
         <input type="submit" 
                name="submit" 
                value="Update circuit" /></td>
     </tr>
</form>
</table>

</%def> 
