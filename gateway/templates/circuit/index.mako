<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
    <script type="text/javascript">
      $(function() { 
         $('.buttons li').button()
      });
      
    </script>
</%def> 

<%def name="content()"> 
<h3>Circuit overview page</h3>

<table class="no-border" border="0">
  <tr>
    <td>
      <table class="overview">
      % for key,value in fields.iteritems(): 
      <tr>
        <td class="hint">Circuit ${key}</td>
        <td>${str(value.get("value"))}</td>
      </tr>
      % endfor 
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
      <div class="buttons">        
      <ul> 
        <li><a 
               href="${request.application_url}${circuit.edit_url()}">
            Edit circuit information</a></li> 
        <li>
          <a href="${request.application_url}/account/edit/${str(circuit.account.id)}">
            Edit account information</a></li>
        <li><a href="${circuit.remove_url()}">Remove circuit</a></li>
        <li>
          <a href="${request.application_url}/circuit/turn_on/${circuit.id}">
            Turn On </a>
        </li>
        <li>
          <a href="${request.application_url}/circuit/turn_off/${circuit.id}">
            Turn Off </a>
        </li>
        <li>
          <a href="${request.application_url}/circuit/ping/${circuit.id}">
            Ping Circuit </a>
        </li>
        <li>
          <form method="POST" id=""
                action="${request.application_url}/circuit/add_credit/${circuit.id}">
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
   href="${request.application_url}/circuit/remove_jobs/${circuit.id}">
   Clear job queue</a>
<table class="jobs">
  <tr>
    <th>Job id</th>
    <th>Job description</th>
    <th>Job type</th> 
    <th>Job start time</th>
    <th>Job end time</th>
    <th>Job message</th>
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
    <td>${str(job.state)}</td>
    <td>${job.start}</td>
    % if job.end: 
       <td>${job.end}</td>
    % else: 
       <td></td>
    % endif 
       % if len(job.job_message) >= 1:   
         <td></td>
       % endif
  </tr> 
  % endfor 
</table>
<hr /> 
<h4>All of the logs associated with circuit</h4>
<table border="0">
  <tr>
    <th>Log id</th>
    <th>Log uuid</th>
    <th>Log date</th>
    <th>Log credit</th>
    <th>Circuit state</th>
  </tr>
  % for log in circuit.get_logs(): 
    <tr>
      <td>${log.id}</td>
      <td> ${log.uuid} </td> 
      <td>${log.date.ctime()}</td>
      <td>${log.credit}</td>
      <td>${log.status}</td>
    </tr>
  % endfor 
</table>


</%def> 
