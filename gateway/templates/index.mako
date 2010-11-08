<%inherit file="base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()">
<h3>Manage and edit the Gateway for the <a href="http://sharedsolar.org">
    Shared Solar</a> Project</h3>

<h4>Manage and edit meters</h4> 
<ul>
  <li><p>Edit, remove and manage meters</p></li>
  <li><p><a href="/meters/add/"> Add a new meter</a></p></li>
  <li><p>List of existing configured meters</p></li>
</ul>

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

