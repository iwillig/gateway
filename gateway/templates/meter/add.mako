<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()"> 
<h3>Add a new meter to the gateway</h3> 

<form method="POST" id="add-meter" action=".">
  <table class="form" width="" cellspacing="" cellpadding="" border="0">
    <tr>
      <td><label>Meter name: </label></td>
      <td><input type="text" name="name" value="" /> </td>
    </tr>
    <tr>
      <td><label>Meter location: </lable></td>
      <td><input type="text" name="location" value="" /></td>
    </tr>
    <tr>
      <td></td>
      <td>
        <input type="submit" name="" value="Add a new meter" />
      </td>
    </tr>
  </table>
</form>

</%def> 
