<%inherit file="base.mako"/>

<%def name="header()">
   <title>home page</title>
</%def>

<%def name="content()">
<ol id="">      
  % for meter in meters:
  <li>
    <p><span>Name:</span>${meter.name}</p>
    <p><span>UUID</span>${meter.uuid}</p>
  </li> 
  % endfor
</ol>
</%def>

