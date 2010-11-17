<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Edit ${meter.name}</title>
</%def>

<%def name="content()"> 
<h4>Edit ${meter.name}</h4> 
<table class="form">
  <form method="POST" id="add-meter" 
        action="${request.application_url}/update_meter">
    <tr>
      <td><label>Send updated fields to the meter</td>
      <td><input type="checkbox" name="send.to.meter" value="checked" /></td>
    </tr>
    <tr>
      <td><label>Meter name: </label></td>
      <td><input type="text" name="name" value="${meter.name}" /> </td>
      <td class="hint">Meter names should be easy to remember. They
      must be unique.</td>
    </tr>
    <tr>
      <td><label>Meter location: </lable></td>
      <td><input type="text" name="location" value="${meter.location}" /></td>
      <td class="hint">Locations should be the physical locations of
      the meter, or close as possible.</td>
    </tr>
    <tr>
      <td><label>Battery Capacity: </label></td>
      <td><input type="text" name="battery" value="${meter.battery}" /></td>
      <td class="hint">The battery capacity of the meter system.</td>
    </tr>
    <tr>
      <td></td>
      <td>
      </td>
      <td>
        <input type="submit" name="" value="Update ${meter.name}" />
      </td>
    </tr>
  </table>
</form>

</%def> 
