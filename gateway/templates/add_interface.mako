<%inherit file="base.mako"/>

<%namespace name="headers" file="headers.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   ${headers.deformStyles(request)}
</%def>

<%def name="content()"> 
   <br />
   <p>${cls.__doc__}</p>
   ${form.render()}
</%def>
