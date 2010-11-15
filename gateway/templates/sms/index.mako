<%inherit file="../base.mako"/>


<%def name="header()"> 
   <title>SMS logs</title>
</%def>

<%def name="content()"> 

   <a href="${request.application_url}/sms/remove_all">Remove all messages</a>
   <table class="message">      
     <h4>Incoming messages</h4>
     <tr> 
       <th>Message uuid</th>
       <th>Message id</th>
       <th>To</th> 
       <th>From</th>
       <th>Date</th> 
       <th>Message</th> 
     </tr>
   % for msg in incoming_msgs: 
     <tr>
       <td><a href="${request.application_url}/${msg.url()}">${msg.uuid}</a></td>
       <td>${msg.id}</td>
       <td>${msg.to}</td> 
       <td>${msg.origin}</td>
       <td>${msg.date.ctime()}</td>
       <td>${msg.text}</td>
     </tr>
   % endfor 

   </table> 
   <table class="message">      
     <h4>Outgoing messages</h4>
     <a href="/sms/received">Active outgoing messages</a>
     <tr> 
       <th>Message uuid</th>
       <th>Message id</th>
       <th>To</th> 
       <th>From</th>
       <th>Date</th> 
       <th>Message</th> 
       <th>Sent</th>
     </tr>
   % for msg in outgoing_msgs: 
     <tr>       
       <td><a href="${request.application_url}">${msg.uuid}</a></td>
       <td>${msg.id}</td>
       <td>${msg.to}</td> 
       <td>${msg.origin}</td>
       <td>${msg.date.ctime()}</td>
       <td>${msg.text}</td>
       <td>${msg.sent}</td>
    </tr>
   % endfor 

   </table> 


</%def>
