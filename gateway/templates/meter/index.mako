<%inherit file="../base.mako"/>

<%def name="header()">


   <script type="text/javascript"
           src="${request.application_url}/static/meter_page.js"></script>

   <script type="text/javascript">
     $(document).ready(function() { 
         loadPage("${request.application_url}/meter/add_circuit/${meter.uuid}",
            "${request.application_url}/meter/get_circuits/${meter.uuid}");}); 
   </script>

</%def>

<%def name="content()">
<h3>Meter overview page</h3> 
<table class="no-border" border="0">
  <tr>
    <td>
    <table class="overview" border="0">
      <tr>
        <td class="hint">Meter name:</td>
        <td>${meter.name}</td>
      </tr>
      <tr>
        <td class="hint">Meter location:</td>
        <td>${meter.location}</td>
      </tr>
      <tr>
        <td class="hint">Meter battery capacity:</td>
        <td>${meter.battery}</td>
      </tr>
    </table>  
    </td> 
    <td> 
      <div class="actions"> 
        <ul>
          <li><a href="${meter.edit_url()}">Edit meter information</a></li>
          <li><a href="/jobs/meter/${meter.name}/">View active job
          queue</a></li>
          <li><a href="#">Toggle on/off</a></li>
          <li>
            <a href="${request.application_url}/${meter.remove_url()}">
              Remove Meter</a>
        </ul>
      </div>
    </td>
  </tr>
</table>

<hr /> 
<h4>Circuits associated with ${meter.name}</h4>

<div class="small-form">
  <table>
    <tr>
      <td><label>Account language</label></td>
      <td>
        <select id="lang"> 
          <option value="en">English</option>
          <option value="fr">French</option>
        </select>
      </td>
    </tr>
    <tr>
      <td><label>Phone</lable></td>
      <td><input type="text" id="phone" name="phone" value="" /></td>      
    </tr>
    <tr>
      <td><label>Ip Address: </label></td>
      <td><input type="text" id="ip_address" name="ip_address" value="192.168.1.201" /></td>
    </tr>
    <tr>
      <td><label>Energy Max: <label></td>
      <td><input type="text" id="energy_max" name="" value="100"
      /></td>      
    </tr>
    <tr>
      <td><label>Power Max: </label></td>
      <td><input type="text" id="power_max"  name="" value="100"
      /></td>
    </tr>
    <tr>
      <td></td>
      <td><input type="submit" id="add-circuit" name="" value="Add circuit" /></td>
    </tr>
</table>
</div> 

<table class="circuits">
  <tr>
    <th><strong>Circuit ip address</strong></th>
    <th><strong>Circuit uuid: </strong></th>
    <th><strong>Circuit pin: </strong></th>
    <th><strong>Circuit power max: </strong></th>
    <th><strong>Circuit energy max: </strong></th>
  </tr>
</table>
<hr /> 

</%def> 
