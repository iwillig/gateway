<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>
<%! 
   import simplejson
   from gateway.utils import Widget
  
%> 

<%def name="header()"> 
   <title>SMS logs</title>

   ${headers.load_slickGrid(request)}
   
   <script type="text/javascript">
     $(function() {
        $(".buttons a").button(); 
        $( "#tabs" ).tabs();
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

  <div id="tabs">
    <ul>
      <li> <a href="#tabs-1">All messages</a></li>
      <li> <a href="#tabs-2">Incoming Messages</a></li>
      <li> <a href="#tabs-3">Outgoing Messages</a></li>
      <li> <a href="#tabs-4">Job Messages</a></li>
    </ul>
    <div id="tabs-1"> 
      <p>All messages, ordered by date.</p>
      <div class="messages">
      <table>
        <thead>
          <th>Text</th>
          <th>Incoming Message</th>
          <th>Phone number</th>
          <th>Date</th>
          <th>Message Type</th>
        </thead>
        <tbody> 
          % for msg in messages: 
          <tr>
            <td><a 
            href="${request.application_url}/message/index/${msg.uuid}">${msg.text}
            </a></td>
            <td> ${msg.get_incoming()} </td>
            <td>${msg.number}</td>
            <td>${msg.date.ctime()}</td>
            <td>${msg.type}</td>
          </tr>
          % endfor           
        </tbody>
      </table>
      </div>
    </div>
    <div id="tabs-2">       
      <p>Incoming messages are messages that are received by the
      gateway from either a consumer or a meter</p>
      <div class="messages">
        ${Widget(messages.filter_by(type='incoming_message')).as_table()} 
      </div>
    </div>

    <div id="tabs-3">
      <p>Outgoing messages are sent to consumers from the gateway</p>
      <div class="messages">
        ${Widget(messages.filter_by(type='outgoing_message')).as_table()}
      </div>
    </div>

    <div id="tabs-4">
      <p>Job messages are a special kind of outgoing messages that are
      associated with a job to the meter</p>
      <div class="messages">
        ${Widget(messages.filter_by(type='job_message')).as_table()}
      </div>
    </div>
  </div>
     
</%def>
