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
   <table class="message">      
     <tr> 
       <th>Message id</th>
       <th>Message type</th>
       <th>Message</th> 
       <th>Sent?</th>
       <th>Origin</th>
     </tr>
   % for msg in messages: 
     <tr>
       <td>${str(msg.id)}</td>
       <td>${msg._type}</td>
       <td>${str(msg.text)}</td>
       <td>${msg.sent}</td>
       % if msg._type == "incoming_message": 
          <td>${msg.number}</td>
       % elif msg._type == "outgoing_message": 
          <td>${str(msg.get_incoming())}</td>
       % else: 
          <td></td>
       % endif 
     </tr>     
   % endfor 

   </table> 
</%def>
