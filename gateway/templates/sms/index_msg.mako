<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()"> 
   <title>Message overview</title>
</%def> 

<%def name="content()"> 
    

    ${message.text}

</%def>
