<%inherit file="../base.mako"/>


<%def name="header()"> 
  <title>Manage home</title>
  <script type="text/javascript">
    $(function() { 
      $('.manage-menu li').button();
    }); 
  </script>
</%def> 

<%def name="content()"> 

  <ul class="manage-menu">
    <li><a href="#">Meters</a></li>
    <li><a href="#">Tokens</a></li>
    <li><a href="#">Manual Alerts</a></li>
    <li><a href="#">Pricing Models</a></li>
  </ul>

</%def>
