<%inherit file="../base.mako"/>

<%def name="header()">
  <title>Interface page</title>
</%def>

<%def name="content()">    
    <table>
      % for key,value in fields.iteritems(): 
      <tr>
        <td class="hint">Interface ${key}</td>
        <td>${value.get("value")}</td>
      </tr>
      % endfor 
    </table>
    <a href="${request.application_url}/interface/remove/${interface.id}">
      Remove</a>
</%def>
