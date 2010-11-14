<%inherit file="base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()">

<div id="manage-meter" class="intro-box">
<h4>Manage and edit <strong>meters</strong></h4> 
<p>Edit, remove and manage meters</p>
<p><a href="${request.application_url}/add_meter"> Add a new meter</a></p>

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

<div id="manage-token" class="intro-box"> 
  <h4>Manage and create Tokens</h4>
  <form method="POST" id=""
        action="${request.application_url}/add_tokens">
    <table>
      <tr>
        <td class="hint">Number of tokens to be create</td>
        <td><input type="text" name="amount" value="" /></td>
      </tr>
      <tr>
        <td class="hint">Value for each token</td>
        <td><input type="text" name="value" value="" /></td>
      </tr>
      <tr>
        <td></td>
        <td><input type="submit" name="" value="Add token" /></td>
      </tr>
    </table>
  </form>
</div>

<div id="manage-messages" class="intro-box">
<h4>Manage and send SMS Messages</h4> 
<a href="${request.application_url}/sms/index"> Check all SMS
  messages</a> 
</div>
</%def>

