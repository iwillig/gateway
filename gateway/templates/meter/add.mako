<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   <script type="text/javascript">
     $(function() { 
         $('#add_meter').button(); 
     }); 
   </script>
</%def>

<%def name="content()"> 
<h3>Add a new meter to the gateway</h3> 

<table class="form">
  <form method="POST" id="add-meter" 
        action="${request.application_url}/add_meter">
    <tr>
      <td><label>Meter name: </label></td>
      <td><input type="text" name="name" value="" /> </td>
      <td class="hint">Meter names should be easy to remember. They
      must be unique.</td>
    </tr>
    <tr>
      <td><label>Meter phone: </label></td>
      <td><input type="text" name="phone" value="" /> </td>
      <td class="hint">Meter phone number, this is how the Gateway
      send information to the Meter. This should not be a account
      number</td>
    </tr>
    <tr>
      <td><label>Meter communication: </label></td>
      <td>
        <select name="communication"> 
          <option value="sms">SMS</option> 
          <option value="http">Http/Data</option>
        </select>
      </td>
      <td class="hint">Define how the meter communicates with the
      gateway</td>
    </tr>
    <tr>
      <td><label>Meter location: </label></td>
      <td><input type="text" name="location" value="" /></td>
      <td class="hint">Locations should be the physical locations of
      the meter, or close as possible.</td>
    </tr>
    <tr>
      <td><label>Battery Capacity: </label></td>
      <td><input type="text" name="battery" value="100" /></td>
      <td class="hint">The battery capacity of the meter system.</td>
    </tr>
    <tr>
      <td><label>Panel Capacity: </label></td>
      <td><input type="text" name="panel" value="100" /></td>
      <td class="hint">The battery capacity of the meter system.</td>
    </tr>
    <tr>
      <td></td>
      <td>
      </td>
      <td>
        <input id="add_meter" type="submit" name="" value="Add a new meter" />
      </td>
    </tr>
  </table>
</form>

</%def> 
