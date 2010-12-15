
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
