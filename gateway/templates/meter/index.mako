<%inherit file="../base.mako"/>

<%def name="header()">
</%def>

<%def name="content()">
<h3>Meter overview page</h3> 
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
      <div class="actions"> 
        <ul>
          <li><a href="${meter.edit_url()}">Edit meter information</a></li>
          <li><a href="/jobs/meter/${meter.name}/">View active job
          queue</a></li>
          <li>
            <a href="${request.application_url}/${meter.remove_url()}">
              Remove Meter</a>
              <li>
          <a href="${request.application_url}/meter/build_graph/${meter.uuid}">
            Build Graph</a></li>
        </ul>
      </div>
    </td>
  </tr>
</table>

<hr /> 
<h4>Circuits associated with ${meter.name}</h4>

<div class="small-form">
  <form method="POST" id=""
        action="${request.application_url}/meter/add_circuit/${meter.uuid}">    
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
    % for item in circuit_header:
        <th>${item.get("name")}</th>
    % endfor 
  </tr>
  
  % for item in circuit_data: 
  <tr>
    <td>${item["meter_id"]}</td>
    <td>${item["id"]}</td>
    <td>
      <a href="${request.application_url}/circuit/index/${item["uuid"]}">${item["uuid"]}
    </a></td>
    <td>${item["date"]}</td>
    <td>${item["pin"]}</td>
    <td>${item["energy_max"]}</td>
    <td>${item["power_max"]}</td>
    <td>${item["status"]}</td>
    <td>${item["ip_address"]}</td>
    <td>${item["credit"]}</td>
    <td>${item["account_id"]}</td>
  </tr>  
  % endfor 

</table>
<hr /> 

</%def> 
