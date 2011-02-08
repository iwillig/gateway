<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   ${headers.deformStyles(request)}
   <script type="text/javascript">
     $(function() { 
         $('#deformadd_meter').button(); 
     }); 
   </script>
</%def>

<%def name="content()"> 
<h3>Add a new meter to the gateway</h3> 
${form.render()}
<script type="text/javascript">
   deform.load()
</script>

</%def> 
