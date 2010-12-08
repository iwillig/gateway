<%inherit file="base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()">

% if logged_in:
   <div id="manage-meter" class="intro-box">
      <h4>Manage and edit <strong>meters</strong></h4> 
      <p>Edit, remove and manage meters</p>
      <p><a href="${request.application_url}/add_meter"> Add a new meter</a></p>
      <table>
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
    <td>${str(len(meter.get_circuits()))}</td>
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
  <h4>Upload tokens from csv</h4>
  <form method="POST" id=""
        enctype="multipart/form-data"
        action="${request.application_url}/upload_tokens">
    <input type="file" name="csv" value="" />
    <input type="submit" name="submit" value="Upload tokens from csv" />
  </form>
  <h4>Existing token batches</h4>
  <table>    
    <tr>
      <th>Batch uuid</th>
      <th>Batch id</th>
      <th>Batch created on</th>
      <th>Number of tokens in batch</th>
      <th></th>
    </tr>
  % for batch in tokenBatchs:   
    <tr>
      <td><a href="${batch.url()}">${batch.uuid}</a></td>
      <td>${str(batch.id)}</td>
      <td>${batch.created.ctime()}</td>
      <td>${str(batch.get_tokens().count())}</td>
      <td><a href="${request.application_url}/token/refesh/${batch.uuid}">
     Refesh token state</a></td>
    </tr>
  % endfor 
  </table>

</div>

<div id="manage-messages" class="intro-box">
<h4>Manage and send SMS Messages</h4> 
<form method="POST" id=""
      action="${request.application_url}/send_message">
  <input type="text" name="number" value="" />
  <input type="text" name="text" value="" />
  <input type="submit" name="" value="Send Test Message" />
</form>

<a href="${request.application_url}/sms/index"> Check all SMS
  messages</a> 
</div>


<div id="manage-system-logs" class="intro-box">
  <h4>Manage and view system logs</h4>  
  <ul>
  % for log in system_logs[:10]:
      <li>${log.text}</li>     
  % endfor 
  </ul>  
</div>




% else: 
% endif

</div>
</%def>

