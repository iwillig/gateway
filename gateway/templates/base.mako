<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    ${self.header()}

    <link rel="stylesheet" 
          href="${request.application_url}/static/css/boilerplate/screen.css" 
          type="text/css" 
          media="screen" />

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
      <div class="content">
        ${self.content()}
      </div>
    </div>
  </body>  
</html>

