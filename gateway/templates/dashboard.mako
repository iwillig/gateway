<%inherit file="base.mako"/>
<%namespace name="headers" file="headers.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   <style type="text/css" media="screen">
     .widget { margin: 10px; } 
     .widget-header { padding: 5px } 
     .widget-header .ui-icon { float: right; }
     .widget-content { padding: 10px; } 
     .ui-sortable-placeholder { border: 1px dotted black; visibility:
     visible !important; height: 50px !important; }     
     .ui-sortable-placeholder * { visibility: hidden; }
   </style>

   ${headers.load_slickGrid(request)}
   
   <script type="text/javascript" 
           src="${request.application_url}/static/site/dashboard.js">
   </script>
   
   <script type="text/javascript">
     $(function() { 
        LoadPage({}); 
     }); 
     
   </script>

</%def>

<%def name="content()">
<div class="widgets">

  <div id="meter-status" class="widget">
    <div class="widget-header">Meter Status</div>
    <div class="widget-content">      
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae pretium libero. Sed ac purus sapien. Nam at lorem nec nisl ultrices posuere in eu dolor. Etiam ornare, velit in porta convallis, est nibh tempor ante, quis ultrices turpis sapien et risus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi molestie felis nec odio tempus sed gravida neque lobortis. Etiam pretium nulla tortor, ac fringilla nibh. In ac leo sem. Integer tincidunt mi quis orci malesuada at commodo sapien vestibulum. Sed ipsum elit, consequat a rhoncus et, blandit vel metus. Aenean sagittis vulputate metus nec tincidunt. Fusce aliquet pellentesque malesuada. Ut ac nibh lectus, vitae posuere lorem. 
    </div>
  </div>

  <div id="meter-power-chart" class="widget">
    <div class="widget-header">Meter power chart</div>
    <div class="widget-content">      
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae pretium libero. Sed ac purus sapien. Nam at lorem nec nisl ultrices posuere in eu dolor. Etiam ornare, velit in porta convallis, est nibh tempor ante, quis ultrices turpis sapien et risus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi molestie felis nec odio tempus sed gravida neque lobortis. Etiam pretium nulla tortor, ac fringilla nibh. In ac leo sem. Integer tincidunt mi quis orci malesuada at commodo sapien vestibulum. Sed ipsum elit, consequat a rhoncus et, blandit vel metus. Aenean sagittis vulputate metus nec tincidunt. Fusce aliquet pellentesque malesuada. Ut ac nibh lectus, vitae posuere lorem. 
    </div>
  </div>

  <div id="communication-logs" class="widget">
    <div class="widget-header">Communication logs</div>
    <div class="widget-content">      
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae pretium libero. Sed ac purus sapien. Nam at lorem nec nisl ultrices posuere in eu dolor. Etiam ornare, velit in porta convallis, est nibh tempor ante, quis ultrices turpis sapien et risus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi molestie felis nec odio tempus sed gravida neque lobortis. Etiam pretium nulla tortor, ac fringilla nibh. In ac leo sem. Integer tincidunt mi quis orci malesuada at commodo sapien vestibulum. Sed ipsum elit, consequat a rhoncus et, blandit vel metus. Aenean sagittis vulputate metus nec tincidunt. Fusce aliquet pellentesque malesuada. Ut ac nibh lectus, vitae posuere lorem. 
    </div>
  </div>

  <div id="alarms" class="widget">
    <div class="widget-header">Alarms</div>
    <div class="widget-content">      
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae pretium libero. Sed ac purus sapien. Nam at lorem nec nisl ultrices posuere in eu dolor. Etiam ornare, velit in porta convallis, est nibh tempor ante, quis ultrices turpis sapien et risus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi molestie felis nec odio tempus sed gravida neque lobortis. Etiam pretium nulla tortor, ac fringilla nibh. In ac leo sem. Integer tincidunt mi quis orci malesuada at commodo sapien vestibulum. Sed ipsum elit, consequat a rhoncus et, blandit vel metus. Aenean sagittis vulputate metus nec tincidunt. Fusce aliquet pellentesque malesuada. Ut ac nibh lectus, vitae posuere lorem. 
    </div>
  </div>
</div>

</%def>
