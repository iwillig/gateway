<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
</%def> 

<%def name="content()"> 
<h3>Circuit overview page</h3>

<table class="no-border" border="0">
  <tr>
    <td>
      <table class="overview">
        <tr>
          <td class="hint">Circuit id</td>
          <td>${str(circuit.id)}</td>
          <td></td>
        </tr>
        <tr>
          <td class="hint">Circuit ip address</td>
          <td>${str(circuit.ip_address)}</td>
          <td></td>
        </tr>
        <tr>
          <td class="hint">Circuit credit</td>
          <td>${str(circuit.credit)}</td>
          <td></td>
        </tr> 
        <tr>
          <td class="hint">Circuit pin :</td>
          <td>${str(circuit.pin)}</td>
          <td class="hint">Circuit pins are used by consumers via sms
            messages</td>
        </tr>
        <tr>
          <td class="hint">Circuit energy max :</td>
          <td>${str(circuit.energy_max)}</td>
          <td></td>
        </tr>
        <tr>
          <td class="hint">Circuit power max :</td>
          <td>${str(circuit.power_max)}</td>
          <td></td>
        </tr>
        <tr>
          <td class="hint">Circuit status :</td>
          <td>${str(circuit.status)}</td>
          <td class="hint">0 means the circuit is off, 1 means its on.</td>
        </tr>

        <tr>
          <td class="hint">Account phone</td>
          <td><a href="${request.application_url}/${circuit.account.url()}">${str(circuit.account.phone)}</a></td>
        </tr>
        <tr>
          <td class="hint">Account language</td>
          <td>${circuit.account.lang}</td>
        </tr>
      </table>
    </td>    
    <td>
      <div class="actions">        
      <ul> 
        <li><a href="${circuit.edit_url()}">Edit circuit information</a></li> 
        <li><a href="${circuit.remove_url()}">Remove circuit</a></li>
        <li><a href="${circuit.toggle_url()}">Toggle on/off</a></li>
        <li>
          <a href="${request.application_url}/circuit/build_graph/${circuit.uuid}">
            Build Graph</a></li>
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
<a 
   href="${request.application_url}/circuit/remove_jobs/${circuit.uuid}">
   Clear job queue</a>
<table class="jobs">
  <tr>
    <th>Job id</th>
    <th>Job description</th>
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
    <td><a href="${request.application_url}/${job.url()}">${job.id}</a></td>
    <td>${job.description}</td>
    <td>${job._type} </td>
    <td>${job.state}</td>
    <td>${str(job.state)}</td>
    <td>${job.start}</td>
    % if job.end: 
       <td>${job.end}</td>
    % else: 
       <td></td>
    % endif 
  </tr> 
  % endfor 
</table>
<hr /> 
<h4>Last 20 logs associated with circuit</h4>
<table border="0">
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
