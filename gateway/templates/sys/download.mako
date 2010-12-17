<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()">
<ul> 
  <!-- Hard coded links in html bad !-->
    <li><a href="http://localhost:6543/sys/export?model=Account">Download
        Account</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Turnoff">Download
        Turnoff</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Jobs">Download
        Jobs</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Log">Download
        Log</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=SystemLog">Download
        System Log</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=OutgoingMessage">Download
        Outgoing Message</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Alert">Download
        Alert</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=JobMessage">Download
        Job Message</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Token">Download
        Token</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=TokenBatch">Download
        Tokenbatch</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Meter">Download
        Meter</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Circuit">Download
        Circuit</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=AddCredit">Download
        AddCredit</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=IncomingMessage">Download
        Incoming Message</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=Message">Download
        Message</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=PrimaryLog">Download
        Primary Log</a></li> 
    <li><a href="http://localhost:6543/sys/export?model=TurnOn">Download
        Turnon</a></li> 
 
</ul> 


</%def>
