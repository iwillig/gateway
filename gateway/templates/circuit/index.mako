<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
</%def> 

<%def name="content()"> 
<h3>Circuit overview page</h3>

<table class="no-border" border="0">
  <tr>
    <td>
      <table class="overview" border="0">
        <tr>
          <td class="hint">Circuit ip address</td>
          <td>${circuit.ip_address}</td>
          <td></td>
        </tr>
        <tr>
          <td class="hint">Circuit credit</td>
          <td>${circuit.credit}</td>
          <td></td>
        </tr> 
        <tr>
          <td class="hint">Circuit pin :</td>
          <td>${circuit.pin}</td>
          <td class="hint">Circuit pins are used by consumers via sms
            messages</td>
        </tr>
        <tr>
          <td class="hint">Circuit energy max :</td>
          <td>${circuit.energy_max}</td>
          <td></td>
        </tr>
        <tr>
          <td class="hint">Circuit power max :</td>
          <td>${circuit.power_max}</td>
          <td></td>
        </tr>
        <tr>
          <td class="hint">Circuit status :</td>
          <td>${circuit.status}</td>
          <td></td>
        </tr>
      </table>
    </td>    
    <td>
      <div class="actions">        
      <ul> 
        <li><a href="${circuit.edit_url()}">Edit circuit information</a></li> 
        <li><a href="${circuit.remove_url()}">Remove circuit</a></li>
        <hr />
        <li><a href="${circuit.toggle_url()}">Toggle on/off</a></li>
        <li>
          <form method="POST" id=""
                action="${request.application_url}/circuit/add_credit/${circuit.uuid}">
            <label>Amount</label>
            <input type="text" name="amount" value="" />
            <input type="submit" name="submit" value="Add credit" />
          </form>
        </li>
      </ul>
      </div>
    </td>
  </tr>

</table>
<hr />
<h4>Jobs associated with circuit</h4>
<table class="jobs" border="0">
  <tr>
    <th>Job id</th>
    <th>Job description</th>
    <th>Job uuid</th>
    <th>Job type</th> 
    <th>Job active</th>
    <th>Job start time</th>
    <th>Job end time</th>
  </tr>
  % for job in jobs: 
     % if job.state == True:
        <tr class="active"> 
     % else:
        <tr class="not-active">
     % endif 
    <td>${job.id}</td>
    <td>${job.description}</td>
    <td>
      <a href="${request.application_url}/${job.url()}">${job.uuid}</a>
    </td>
    <td>${job._type} </td>
    <td>${job.state}</td>
    <td>${job.start.ctime()}</td>
    % if job.end: 
       <td>${job.end.ctime()}</td>
    % else: 
       <td></td>
    % endif 
  </tr> 
  % endfor 
</table>
<hr /> 
<h4>Last 20 logs associated with circuit</h4>
<table border="">
  <tr>
    <th>Log id</th>
    <th>Log uuid</th>
    <th>Log date</th>
  </tr>
  % for log in circuit.get_logs()[0:20]: 
    <tr>
      <td>${log.id}</td>
      <td> ${log.uuid} </td> 
      <td>${log.date}</td>
    </tr>
  % endfor 
</table>


</%def> 