<%inherit file="base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>

   <script type="text/javascript">
     $(function() { 
        $('.button').button(); 
        $('.widgets').setWidget('.widget');
     }); 

   </script>

</%def>

<%def name="content()">


% if logged_in:
<div class="widgets"> 

<div id="manage-meter" class="widget">
  <div class="widget-header">Manage meters</div>
  <div class="widget-content">
  <p><a class="button" 
        href="${request.application_url}/add_meter"> 
      Add a new meter</a></p>
  <table>
    <tr>
      <th>Meter name</th>
      <th>Meter location</th>
      <th>Number of circuits</th>
    </tr>
    <hr />
    % for meter in meters:
  <tr>
    <td><a href="${meter.getUrl()}">${meter.name}</a></td>
    <td>${meter.location}</td>
    <td>${str(len(meter.get_circuits()))}</td>
  </tr>
  % endfor
</table>
  
  </ul>
 </div>
</div>

<div id="manage-interface" class="widget">
  <div class="widget-header">Manage Interfaces</div>
  <div class="widget-content">
  <p><a class="button"
        href="${request.application_url}/add?class=KannelInterface">
      Add kannel interface</a></p>
  <p><a class="button"
        href="${request.application_url}/add?class=NetbookInterface">
      Add netbook interface</a></p>  
  <hr />
  <table>
    <tr>
      <th>Name</th>
      <th>Location</th>
    </tr>
    % for interface in interfaces:
    <tr>
      <td><a href="${interface.getUrl()}">${interface.name}</a></td>
      <td>${interface.location}</td>
    </tr>
    % endfor
  </table>

  </div>
</div>

<div id="manage-token" class="widget"> 
  <div class="widget-header">Manage tokens</div>
  <div class="widget-content">
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
        <td><input class="button" 
                   type="submit" 
                   name="" 
                   value="Add token" /></td>
      </tr>
    </table>
  </form>
  <h4>Upload tokens from csv</h4>
  <form method="POST" id=""
        enctype="multipart/form-data"
        action="${request.application_url}/upload_tokens">
    <input type="file" name="csv" value="" />
    <input class="button" 
           type="submit" 
           name="submit" 
           value="Upload tokens from csv" />
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
      <td><a href="${batch.getUrl()}">${batch.uuid}</a></td>
      <td>${str(batch.id)}</td>
      <td>${batch.created.ctime()}</td>
      <td>${str(batch.get_tokens().count())}</td>
      <td><a href="${request.application_url}/token/export_batch/${batch.uuid}">
          Export batch to CSV</a></td>
    </tr>
  % endfor 
  </table>
</div>
</div>

<div id="manage-messages" class="widget">
<div class="widget-header">Manage and send SMS Messages</div>
<div class="widget-content">

<a  href="${request.application_url}/sms/index?limit=100"> Check all SMS
  messages</a> 


<form method="POST" id=""
      action="${request.application_url}/send_message">

  <table>    
    <tr>
      <td><label>Message delivery type</label></td>
      <td>
        <select name="delivery-type"> 
          <option value="KannelOutgoingMessage">Kannel</option> 
          <option value="OutgoingMessage">Netbook</option>
        </select>               
      </td>
    </tr>
    <tr>
      <td><label>Phone Number</label></td>
      <td><input type="text" name="number"value="" /></td>
    </tr> 
    <tr>
      <td> <label>Message body</label></td>
      <td><textarea name="text" id="" rows="10" cols="30"></textarea></td>
    </tr>
    <tr> 
      <td> </td>
      <td><input class="button" type="submit" name="" value="Send Test
      Message" /> </td>
    </tr> 

  </table>
</form>
</div> 
</div>


<div id="manage-system-logs" class="widget">
  <div class="widget-header" >Manage and view system logs</div>
  <div class="widget-content">
    <table >
      <tr>
        <th>Date recorded</th>
        <th>Text</th>
      </tr>
      % for log in system_logs[:20]:
      <tr>
        <td>${log.created}</td>
        <td>${log.text}</td>     
      </tr>
      % endfor 
      
    </table>
  </div>
</div>



% else: 
% endif

</div>
</%def>
