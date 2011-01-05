<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>

   <script type="text/javascript" 
           src="${request.application_url}/static/jquery-1.4.3.min.js"></script>

   <script type="text/javascript"
           src="${request.application_url}/static/jquery-ui-1.8.6.custom.min.js"></script>

   <script type="text/javascript"
           src="${request.application_url}/static/site/functions.js"></script>

   <%namespace name="headers" file="headers.mako"/>
   
    ${headers.styleSheets(request)} 

    ${self.header()}

  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1><a href="/"> SharedSolar Gateway</a></h1>
      </div>
      <div class="navigation">
        <ul class="menu">
          <li class="here"><a href="/">Manage</a></li>
          <li><a href="#">Monitor</a></li>
        </ul>
      </div>
        <ol class="breadcrumbs">

        % if breadcrumbs:
            % for crumb in breadcrumbs: 
                % if crumb.get("url"):
                   <li>&#187; <a href="${crumb.get("url")}"> 
                    ${crumb.get("text")}</a></li>
                % else:
                    <li class="active">&#187; ${crumb.get("text")}</li> 
               % endif
            % endfor 
        % endif 

        </ol>
        <div id="auth">
        % if logged_in: 
              <a href="${request.application_url}/user/logout">Log out</a>
        % else: 
              <a href="${request.application_url}/user/login">Log in</a>
       % endif 
        </div>
        <div class="content">
          ${self.content()}
        </div>
    </div>
  </body>  
</html>

