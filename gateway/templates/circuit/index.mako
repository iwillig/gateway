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
        <li><a href="${circuit.toggle_url()}">Toggle on/off</a></li>
        <li><a href="${circuit.remove_url()}">Remove circuit</a>
      </ul>
      </div>
    </td>
  </tr>


</table>

</%def> 
