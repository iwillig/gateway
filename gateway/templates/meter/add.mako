<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   ${headers.deformStyles(request)}
   <script type="text/javascript">
     $(function() { 
         $('#add_meter').button(); 
     }); 
   </script>
</%def>

<%def name="content()"> 
<h3>Add a new meter to the gateway</h3> 

${form.render()}

</%def> 
