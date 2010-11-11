<%inherit file="../base.mako"/>


<%def name="header()"> 
   <title>SMS logs</title>
</%def>

<%def name="content()"> 

  <form method="" id="" action="">
    <table width="" cellspacing="" cellpadding="" border="0">      
      <tr>
        <td>To :</td>
        <td><input type="text" name="to" value="" /></td>
      </tr>
      <tr>
        <td>Message</td>
        <td>
          <textarea name="message" 
                    id="" rows="5" 
                    cols="30" tabindex="">
          </textarea>
        </td>
      </tr>
      <tr>
        <td></td>
        <td><input type="submit" name="" value="Send Message" /></td>
      </tr>
    </table>
  </form>

  <hr /> 
   <table class="message">      
     <tr> 
       <th>To</th> 
       <th>From</th>
       <th>Date</th> 
       <th>Message</th> 
     </tr>
   % for msg in msgs: 
     <tr>      
       <td>${msg.to}</td> 
       <td>${msg.origin}</td>
       <td>${msg.date}</td>
       <td>${msg.text}</td>
     </tr>
   % endfor 

   </table> 

</%def>
