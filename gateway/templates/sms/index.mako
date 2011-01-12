<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>
<%! 
   import simplejson
   from datetime import datetime
   from gateway.utils import Widget
  
%> 

<%def name="header()"> 
   <title>SMS logs</title>

   <style type="text/css" media="screen">
     a { color: #004276;
         font-weight: bold; }      
   </style>   
   <script type="text/javascript">
     $(function() {
        $('#tabs').tabs();
        $('.widgets').setWidget('.widget');
     });
   </script>             
</%def>

<%def name="content()"> 
<div class="widgets">
<div class="widget">
  <div class="widget-header">Tools and status</div>
  <div class="widget-content">
  <p>Current time on
  server: <strong>${datetime.now().ctime()}</strong> </p>
  <p>Total number of messages: <strong>${count}</strong></p>
  <a href="${request.application_url}/sms/received">
       View outgoing queue</a>
   <form method="GET" id="" 
         action="${request.application_url}/sms/index">
     <input type="text" name="limit" value="${limit}" />
     <input type="submit" name="" value="Limit messages" />
   </form>
   </div>
  </div>

<div class="widget">
  <div class="widget-header">SMS Messages</div>
  <div class="widget-content">
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
          <th>Message id</th>
          <th>Text</th>
          <th>Incoming Message</th>
          <th>Phone number</th>
          <th>Date</th>
          <th>Message Type</th>
        </thead>
        <tbody> 
          % for msg in messages: 
          <tr>
            <td>${msg.id}</td>
            <td><a style="color: #004276; font-weight: bold"
                   href="${request.application_url}/message/index/${msg.id}">${msg.text}
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
      <div class="messages incoming-msgs">
        ${Widget(messages.from_self().filter_by(type='incoming_message')).as_table()} 
      </div>
    </div>

    <div id="tabs-3">
      <p>Outgoing messages are sent to consumers from the gateway</p>
      <div class="messages">
        ${Widget(messages.from_self().filter_by(type='outgoing_message')).as_table()}
      </div>
    </div>

    <div id="tabs-4">
      <p>Job messages are a special kind of outgoing messages that are
      associated with a job to the meter</p>
      <div class="messages">
        ${Widget(messages.from_self().filter_by(type='job_message')).as_table()}
      </div>
    </div>
  </div>
  </div>
</div>
</div>     
</%def>
