<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Please log in</title>

   <%namespace name="headers" file="headers.mako"/>   
   ${headers.styleSheets(request)} 

   <style type="text/css" media="screen">
     #login-form { 
        margin: 10px auto; 
        width: 500px;
        padding: 10px;
        background: #E5ECF9; 
     } 
     
   </style>

  </head>
  <body>

    <div id="login-form">
    <h2>Please login</h2>
      <div class="error"><p>${message}</p></div>
    <form method="POST" id=""
          action="${request.application_url}/user/login">
      <table width="" cellspacing="" cellpadding="" border="">
        <tr>
          <td><label>Username</label></td>
          <td><input type="text" name="login" value="" /></td>
        </tr>
        <tr>
          <td><label>Password</label>
          <td><input type="password" name="password" value="" /></td>
        <tr>
          <td></td>
          <td> 
            <input type="submit" name="form.submitted" value="Log in"/>
          </td>
      </table>
    </form>
    </div>
  </body>
</html>
