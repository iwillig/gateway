<%inherit file="../base.mako"/>

<%def name="header()">
   <title>${meter.name}  page</title>
</%def>

<%def name="content()">
<h3>Meter overview page for: ${meter.name}</h3> 
<p>Meter name: ${meter.name}</p>
</%def> 
