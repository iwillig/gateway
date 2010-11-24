                <%inherit file="../base.mako"/>

<%def name="header()"> 
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
   <table>
     <tr>
       % for header in table_headers:
       <th> ${header.get("name")} </th>
       % endfor        
     </tr>
     % for msg in messages: 
     <tr>
       <td>${msg.type}</td>
       <td>${msg.id}</td>
       <td>${msg.date}</td>
       <td>${msg.sent}</td>
       <td>${msg.number} </td>
       <td>${msg.uuid}</td>
       <td>${msg.text}</td>
        % if msg.type == "outgoing_message": 
          <td>${msg.get_incoming().text}</td>
        % else: 
          <td></td>
        % endif
     </tr>
     % endfor 
     
   </table>
</%def>
