<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Gateway Interface</title>
  </head>
  <body>
    <h1>Gateway Interface</h1>    
    <ol> 
    % for meter in meters:
       <li>${meter.uuid}</li> 
    % endfor
    </ol>
  </body>
</html>
