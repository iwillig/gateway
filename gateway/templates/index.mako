<%inherit file="base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()">

<div id="manage-meter" class="intro-box">
<h4>Manage and edit <strong>meters</strong></h4> 
<p>Edit, remove and manage meters</p>
<p><a href="/meters/add/"> Add a new meter</a></p>

<table border="0">
  <tr>
    <th>Meter uuid</th>
    <th>Meter name</th>
    <th>Meter location</th>
    <th>Number of circuits</th>
  </tr>
  <hr />
  % for meter in meters:
  <tr>
    <td><a href="${meter.url()}">${meter.uuid}</a></td>
    <td>${meter.name}</td>
    <td>${meter.location}</td>
    <td>${len(meter.get_circuits())}</td>
  </tr>
  % endfor
</table>
  
</ul>
</div>


<div id="manage-messages" class="intro-box">
<h4>Manage and send SMS Messages</h4> 
<p>SMS messages are at the core of how the gateway communicates. This
  section of the Gateway allows you to send alerts and monitor
  incoming traffic to the Gateway.</p>
<ul> 
  <li>Send <a href="#">SMS alerts</a> to notify consumers of system downtime</li>
  <li>Monitor <a href="${request.application_url}/sms/index"> all
      SMS</a>  messages</li>
</div>
</%def>

