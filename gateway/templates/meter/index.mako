<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
${headers.ggRaphael(request)}

<script src="${request.application_url}/static/js/g.raphael/g.line.js" 
        type="text/javascript"></script>

<script type="text/javascript"
        src="${request.application_url}/static/js/site/meterPage.js"></script>

<script type="text/javascript">
  $(function() { 
     loadPage(); 
  });
</script>

<style type="text/css" media="screen">
  #graph { 
    background: #fff ; 
    width:700px;
    margin: 5px; 
    height: 250px;
  } 
</style>

</%def>

<%def name="content()">
<h3>Meter overview page for <span class="underline">${meter.name}</span></h3> 
<table>
  <tr>
    <td>
    <table>
      % for key,value in fields.iteritems(): 
      <tr>
        <td class="hint">Meter ${key}</td>
        <td>${value.get("value")}</td>
      </tr>
      % endfor 
    </table>  
    </td> 
    <td> 
      <div class="buttons"> 
        <ul>
          <li><a href="${meter.edit_url()}">Edit meter information</a></li>
          <li> <a id="addCircuitButton" href="#">Add Circuit</a></li>
          <li><a id="showJobButton" href="#">View active job queue</a></li>
          <li>
            <a href="${request.application_url}/${meter.remove_url()}">
              Remove Meter</a>
          </li>
          <li><a href="${request.application_url}/meter/ping/${meter.slug}"> 
              Ping Meter</a>
          </li>
        </ul>
      </div>
      <div id="graph">
      </div>
    </td>  
    
  </tr>
  <tr> 
</table>
<div id="showJobs" style="display: none">
<ul>
% for job in meter.getJobs(): 
    <li>${str(job)} </li>
% endfor 
</ul>
</div>

<hr /> 
<h4>Circuits associated
  with <span class="underline">${meter.name}</span></h4>

<div id="addCircuit" class="small-form" style="display: none">
  <form method="POST" id=""
        action="${request.application_url}/meter/add_circuit/${meter.slug}">    
  <table>
    <tr>
      <td><label>Account language</label></td>
      <td>
        <select name="lang" id="lang"> 
          <option value="en">English</option>
          <option value="fr">French</option>
        </select>
      </td>
    </tr>
    <tr>
      <td><label>Account Phone</lable></td>
      <td><input type="text" id="phone" name="phone" value="" /></td>      
    </tr>

    <tr>
      <td><label>Ip Address: </label></td>
      <td><input type="text" id="ip_address" name="ip_address" 
                 value="192.168.1.201" /></td>
    </tr>
    <tr>
      <td><label>Circuit pin: </label></td>
      <td><input type="text" id="pin" name="pin" 
                 value="" /></td>
    </tr>
    <tr>
      <td><label>Energy Max: <label></td>
      <td><input type="text" id="energy_max" name="energy_max" value="100"
      /></td>      
    </tr>
    <tr>
      <td><label>Power Max: </label></td>
      <td><input type="text" id="power_max"  name="power_max" value="100"
      /></td>
    </tr>
    <tr>
      <td></td>
      <td><input type="submit" id="add-circuit" name="" value="Add circuit" /></td>
    </tr>
</table>
</form>
</div> 

<table class="circuits">
  <tr>
    <th>Circuit id</th>
    <th>Account</th>
    <th>Account language</th>
    <th>Account phone</th>
    <th>Energy max</th> 
    <th>Power max</th>
  </tr>
  
    % for circuit in meter.get_circuits(): 
  <tr>
    <td><a href="${request.application_url}/circuit/index/${circuit.id}">${circuit.ip_address}</a></td>
    <td>${circuit.pin}</td>
    <td>${circuit.account.lang}</td>
    <td>${circuit.account.phone}</td>
    <td>${circuit.energy_max}</td>
    <td>${circuit.power_max}</td>
  </tr> 
    % endfor 

</table>
<hr /> 

</%def> 
