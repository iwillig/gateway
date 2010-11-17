<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()"> 
<h3>Add a new meter to the gateway</h3> 
<table class="form" width="" cellspacing="" cellpadding="" border="0">
  <form method="POST" id="add-meter" 
        action="${request.application_url}/add_meter">
    <tr>
      <td><label>Meter name: </label></td>
      <td><input type="text" name="name" value="" /> </td>
      <td class="hint">Meter names should be easy to remember. They
      must be unique.</td>
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
      <td></td>
      <td>
      </td>
      <td>
        <input type="submit" name="" value="Add a new meter" />
      </td>
    </tr>
  </table>
</form>

</%def> 
