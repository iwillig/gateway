<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Please log in</title>
  </head>
  <body>
    <h2>Please login</h2>

    ${message} 

    <form method="POST" id=""
          action="${request.application_url}/user/login">

      <input type="text" name="login" value="" />
      <input type="password" name="password" value="" />
      <input type="submit" name="form.submitted" value="Log in" />

    </form>
  </body>
</html>
