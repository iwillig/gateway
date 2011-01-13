<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()"> 
   <title>Message overview</title>
</%def> 

<%def name="content()"> 
  <table>
    <tr>
      <td>Message number</td>
      <td>${message.number}</td>
    </tr>
    <tr>
      <td>Message date</td>
      <td>${message.date}</td>
    </tr>
    <tr>
      <td>Message Text</td>
      <td>${message.text}</td>
    </tr>
  </table>
</%def>
