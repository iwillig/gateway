<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
</%def> 

<%def name="content()"> 
<h3>Edit account ${account.phone}</h3>

<table class="form">
<form method="POST" id="" 
      action="${request.application_url}/account/update/${account.id}">
  
  % for key,value in fields.iteritems(): 
  
  % if key != "Lang":
     <tr>
       <td><label>${key}</label></td>
       <td><input type="text" 
                  name="${key.lower()}" 
                  value="${value.get("value")}" /></td>
       % endif
       
     </tr>
  % endfor   
     <tr>
       <td><label>Language</labe></td>
       <td>
         <select name="lang"> 
           <option value="en">English</option>
           <option value="fr">French</option>
         </select>
       </td>
     </tr>
     <tr>
       <td></td>
       <td>
         <input type="submit" 
                name="submit" 
                value="Update account" /></td>
     </tr>
</form>
</table>

</%def> 
