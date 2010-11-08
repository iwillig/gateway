<%inherit file="base.mako"/>

<%def name="header()">
   <title>home page</title>
</%def>

<%def name="content()">
<h3>Manage and edit the Gateway for the <a href="http://sharedsolar.org">
    Shared Solar</a> Project</h3>

<h4>Manage and edit meters</h4> 
<p>Edit, remove and manage meters</p>
<ol id="">      
  % for meter in meters:
  <li>
    <p>
      <span>Name:</span> <a href="${meter.url}">${meter.name}</a>
    </p>
  </li> 
  % endfor  
</ol>

</%def>

