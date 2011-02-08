
<%def name="load_slickGrid(request)"> 
<link rel="stylesheet" 
      href="${request.application_url}/static/SlickGrid/slick.grid.css" 
      type="text/css" 
      media="screen" charset="utf-8" /> 
<script language="javascript" 
        src="${request.application_url}/static/SlickGrid/lib/jquery.event.drag-2.0.min.js">
</script> 
<script language="javascript" 
        src="${request.application_url}/static/SlickGrid/slick.core.js">
</script> 
<script language="javascript" 
        src="${request.application_url}/static/SlickGrid/slick.grid.js">
</script>
<script src="${request.application_url}/static/SlickGrid/slick.dataview.js">
</script>
</%def>

<%def name="ggRaphael(request)"> 
<script src="${request.application_url}/static/js/raphael/raphael.js" 
        type="text/javascript"></script>
<script src="${request.application_url}/static/js/g.raphael/g.raphael.js" 
        type="text/javascript"></script>
</%def>

<%def name="globalScripts(request)"> 
<script type="text/javascript" 
        src="${request.application_url}/static/jquery-1.4.3.min.js"></script>
<script type="text/javascript"
        src="${request.application_url}/static/jquery-ui-1.8.6.custom.min.js"></script>

<script type="text/javascript"
        src="${request.application_url}/static/site/functions.js"></script>
</%def>


<%def name="styleSheets(request)">
<link rel="stylesheet" 
      href="${request.application_url}/static/css/boilerplate/screen.css" 
      type="text/css" 
      media="screen" />

<link rel="stylesheet" 
      href="${request.application_url}/static/css/gateway-theme/jquery-ui-1.8.6.custom.css" 
      type="text/css" 
      media="screen" />
</%def> 

<%def name="deformStyles(request)">

<link rel="stylesheet" 
      href="${request.application_url}/deform-static/css/form.css" 
      type="text/css" />

<script type="text/javascript"
        src="${request.application_url}/deform-static/scripts/deform.js"></script>

</%def>
