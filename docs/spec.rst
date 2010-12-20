

Shared Solar Specification
==========================

Version .01
------------------------------

Last updated by Basinger on Mon Dec 20 12:01:23 2010

Chapter 1 Hardware

Proof-of-Concept Build
------------------------------

The Proof-of-Concept build will utilize off the shelf components. The
below subsections describe each of these major components.


SheevaPlug (Linux Box)
------------------------------


The Linux Box will include an 8GB SD card. The field technician will
be able to download logs from the Linux Box via the Ethernet Switch.

Watt's Up Smart Circuit 20 (SC20)
--------------------------------- 


The SC20's are monitored and controlled via their ethernet connection.

Ethernet Switch
------------------------------


Telit Modem (EVK2 + Interface Board + GC864)
---------------------------------------------


The Modem in the proof-of-concept is comprised of the actual modem
module (GC864) as well as the development board (EVK2) and the
interface board. (The TelDuino version will only include the GC864.)

Enclosures and Mounting
-----------------------


TelDuino Build
------------------------------

The full pilot of the SharedSolar Systems will utilize a custom build
Meter. This meter will capture the functionality of the
Proof-of-Concepts Linux Box, SC20, Switch, and Modem. The code name
for the system is “TelDuino” because of its utilization of the Telit
Modem and the Arduino architecture. The TelDuino is comprised of a
Motherboard, Shield, and Daughterboards.



Motherboard
--------------------


Shield
----------

Mains Daughterboard
------------------------------

1.2.4 Meter/Switch Daughterboard

1.2.5 Enclosure

Chapter 2 Applications

2.1 Installing Applications

2.1.1 Meter's First In-Field Start-up

1. The PV System, Meter, and all wiring for consumers' circuits have
been installed.

2. The Field Tech powers up the meter. “Under-the-hood” the Meter and
Gateway do the following:

(a) The Meter loads its configuration files.

(b) The Meter identifies itself to the Gateway, sending its
configuration files to the Gateway.

(c) The Gateway pushes a job to the job Queue to make any updates to
the Meter's configuration files.

i. The default, innitial settings for each circuit (at first start-up)
are for the relay state to be off, and energy credit to be 101 XOF.

(d) The Meter completes the job of updating its configuration files
accordingly.

3. The Field Tech calls the Gateway operator to verify that the Meter
is communicating with the Gateway.

4. The Field Tech tests the first circuit:

(a) While physically visiting the “end-of-the-wire” of the first
circuit (i.e., the Consumer's home), the Field Tech places an SMS to
the gateway to switch on the relay of the first circuit.

(b) The Field Tech presents a load to the circuit (i.e., a 40 watt
light bulb) and after 1-2 minutes the Field Tech observes the lights
turn on/off 3 times to warn the Consumer that their energy credit has
fallen below 100 XOF.

(c) The Field Tech places an SMS to the gateway to switch off the
relay of the first circuit.

5. The Field Tech tests the rest of the circuits in the same fashion
as above.

2.2 User Applications

2.3 Server Applications

2.3.1 Payment Gateway

Note on Django, RapidSMS/pygsm, ExtJS

2.3.2 Meter

2.3.2.1 Framework

The primary framework providing for the application logic on the Meter
is a Python Twisted service, named 'ssmeter'.

Brief Overview of Twisted
------------------------------

Twisted is an event-driven network programming framework written in
Python and licensed under the MIT License. Twisted projects variously
support TCP, UDP, SSL/TLS, IP Multicast, Unix domain sockets, a large
number of protocols (including HTTP, XMPP, NNTP, IMAP, SSH, IRC, FTP,
and others), and much more. Twisted is based on the event-driven
programming paradigm, which means that users of Twisted write short
callbacks which are called by the framework.

Protocols, along with auxiliary classes and functions, is where most
of the code is. A Twisted protocol handles data in an asynchronous
manner. What this means is that the protocol never waits for an event,
but rather responds to events as they arrive from the network.

The Circuit Protocol
------------------------------

The Meter's Twisted service includes a Server handling requests for a
resource allocated for the circuits. The Watts Up SC20's are able to
make HTTP POST requests at specified intervals to a particular Host
and Port. This Host runs the Twisted server and forwards all requests
from the Watts Up meters to the appropriate resource handler.

The Gateway Protocol
------------------------------

Along with the Circuit Protocol, our Twisted server provides an
additional one for the Gateway to address.

Brief Overview of PPPD


2.3.2.2 ssmeter
--------------------

ssmeter is the service handling and initiating all requests on the
Meter-end.

2.3.2.3 ssmeterconf.txt

ssmeterconf.txt serves as the configuration file for ssmeter. It
provides for both a meaningful initialization of the metering service,
as well as a means for storing the state of the system at shutdown.

Upon startup, ssmeter loads ssmeterconf.txt and uses it to set the
various parameters associated with the individual circuits as well as
the system as a whole.

On shutdown, ssmeter saves the corresponding parameters to
ssmeterconf.txt. This ensures that any changes to the system are
reflected in the service when it's restarted.

Note: If this configuration file needs to be edited manually, shutdown
ssmeter and restart it when you're done.



A sample ssmeterconf.txt contains::

  { 
    "pmax": 500, "emax": 400, "circuits": [

    { "circuitID": "192.168.1.203", 
      "serialnumber": 1118851242,
      "pricingmodels": [0, 1], 
      "energycredit": 6, 
      "active": 1 },

    { 

      "circuitID": "192.168.1.202", 
      "serialnumber": 3820179626,
      "pricingmodels": [0], 
      "energycredit": 10, 
      "active": 0

    }] } 

WattsUp Circuits Data Storage
------------------------------


All data logged from the circuits are stored in files as
comma-separated values. The files are organized in a directory
structure with the format:

YYYY/MM/DD/HH/CIRCUITID.TXT, where CIRCUITID could be a (formatted)
internal IP address of the circuit.



For instance, the recording on 'Sep 20 16:21:15 2010' of a circuit
with an IP address of 192.168.1.201 would be found in::

   2010/09/20/16/192_168_1_201.txt

The contents of these logs include all the parameters provided by the
WattsUp logging interface. It's a CSV file with the following header::

  id,w,v,a,wh,pcy,frq,va,rnc,sr



Scheduled Tasks
------------------------------

For the proof of concept pilot (tech. shake-down) the meter should
only check the job queue once every 10 minutes.

 Unscheduled Tasks
------------------------------


Pricing
------------------------------

Pricing for the first pilot will be based on the conversion found in
[tab:Pricing-Matrix]. Please note that an approximate exchange rate of
500 XOF to 1 USD is assumed. The base line pricing is assumed to be
500 XOF to 1000 watt-hours (approximately 1kWh=1USD). Pricing values,
conversions, and thresholds should all be update-able dynamically by
the Payment Gateway to the Meter; the prices/values below are a
starting point toward further investigation. There are 3 pricing
regimes, one tied to the time of day, one tied to the power level
(load), one to the daily utilized energy (consumption).



An equation to express the rate of energy credit utilization, during a
given pricing state, is shown in [eq:pricing]::

   a=b\times c\times\left(d_{n}\times p_{n}\times e_{n}\right)

where a is the amount of energy credit spent in units of [XOF], b is
the baseline pricing value in units of \left[\frac{XOF}{kWh}\right], c
is the energy utilized in units of [Wh], d_{n}is the time of day
multiplier as determined by [tab:Pricing-Matrix], p_{n}is the power
multiplier as determined by [tab:Pricing-Matrix], and e_{n}is the
energy multiplier as determined by [tab:Pricing-Matrix].

Below are two examples of possible use scenarios further detailing
pricing. These examples assume the following multiplier values:
d_{1}=1, d_{2}=1.5, p_{1}=1, p_{2}=1.5, p_{3}=2, e_{1}=1, e_{2}=1.5,
and a baseline pricing of b=1\left[\frac{XOF}{Wh}\right].

Daytime low load, base pricing: A consumer used 80 watt hours between
9am and 11am, at a max loading of 40 watts. This then cost them 80 XOF
of credit. (Note, they did not exceed the allowed 200 watt-hour base
energy threshold.)

a=b\times c\times\left(d_{n}\times p_{n}\times e_{n}\right)

a=1\times80\times\left(1\times1\times1\right)=80

Nighttime high load pricing: A consumer used a 600 watt hours between
7pm and 10pm, at a consistant loading of 200 watts. This then will
cost 2400 XOF of energy-credit (for the first 200 watt-hours its
baseline pricing x3, because there is a x2 multiplier for nighttime
pricing plus a x2 multiplier for High load pricing which totals a x5
multiplier; multipliers are additive; during the second two hours of
consumption there is an additional x1 multiplier because the consumer
has exceeded the 200 watt-hour daily base-line limit).

a=b\times c\times\left(d_{n}\times p_{n}\times e_{n}\right)

a=\left[1\times200\times\left(1.5\times2\times1\right)\right]+\left[1\times400\times\left(1.5\times2\times1.5\right)\right]=2400

Chapter 3 Networking
==============================

The are four entities in the system - Meter, Payment Gateway,
Consumer, and Field Technician. Each of these entities send and
receive information between the others. Figure [fig:comm-overview]
provides an overview of these different communication types and
pathways.

The interactions between the Consumers, the Payment Gateway, and the
Meter are through standard SMS Messages. The Field Technicians are
provided access to the Meters via a standard GUI/Desktop Environment
available on Linux (by default, Xfce has been installed on the
linux-boxes.)

Aside from Field Tech interaction, communication occurs through
formatted SMS Messages which convey both the requested actions and the
associated data. We sub-divide these into three types based on the
initiation point: Consumer, Gateway, and Meter. A listing of SMS
action codes are presented in Table [tab:List-of-SMS-Action-Codes].




Consumer Initiated Messaging
------------------------------

The Consumers can query the Gateway for account information and
request actions be performed on the lines associated with them. The
Gateway responds to the queries with the information requested. Each
action request is acknowledged by a receipt of completion which the
user can expect within a reasonable timeframe, which we shall set
initially at 60 mins. If the Consumer does not receive acknowledgement
within 60 mins they are expected to resend the request.

While there is no direct communication between the Consumers and the
Meters, we describe here those actions requested by the Consumers that
are forwarded onto the Meters by the Payment Gateway server. These
requests most likely reflect in a status change on the Meters such as
activating and deactivating a line.

Adding credit to a circuit
------------------------------

The Consumer / Vendor can activate a line by adding Energy Credit
(through a token) and sending an SMS message to the Gateway's phone
number. The Gateway sends the Meter associated with the specified
<circuit-ID> an SMS Message about the pending request. The Meter
performs the requested action and sends the Gateway an acknowledgement
of service completion. When the Gateway server receives the
acknowledgement, it notifies the Consumer by sending a message to the
phone number where the request originated. If the Gateway request to
the Meter times-out, it is removed from the list of pending requests,
the Gateway operator is notified through a dashboard alarm, and the
Consumer is notified of the same by sending the following message to
the phone number where the request originated. In this case, the
Consumer is expected to retry the same request.




1) Consumer to Gateway::

    add.<account-number>.<token>

2) Gateway to Meter::

   (cr&<cid>&<amt>&<jobid>)

3) Meter to Gateway::

   (delete&<cid>&<jobid>&<ts>&<wh>&<status> &<tu>&<ct>&<cr>)

4) Gateway to Consumer::

    Credit has been added to account <account-number>. Remaining credit:
    <energy-credit-balance>. Status: <relay-state>

5) (If Time-out reached) Gateway to Consumer::

    Your request to add credit to account <account-number>
    failed. Remaining credit: <energy-credit-balance>. Status:
    <relay-state>

6) (If Time-out reached) Gateway Operator Component Failure Alarm::

     <time-stamp> / COMPONENT FAILURE / Meter <mid> is unresponsive.

Translations:

ENGLISH::

  add.<account-number>.<token>

FRENCH::

  recharge.<numero_compte>.<code>

ENGLISH::

    Credit has been added to account <account-number>. Remaining
    credit: <energy-credit-balance>. Status: <relay-state>

FRENCH::

    <energy-credit-balance>. Merci ! Le solde de la ligne
    <account-number> est désormais de <energy-credit-balance>. La
    ligne est <relay-state>.

ENGLISH::

    Your request to add credit to account <account-number>
    failed. Remaining credit: <energy-credit-balance>. Status:
    <relay-state>

FRENCH::

      ÉCHEC. L'ajout de crédit sur la ligne <account-number> a
      échoué. Solde restant: <energy-credit-balance>. Statut:
      <relay-state>.

3.1.2 Activating a circuit
------------------------------

The Consumer / Vendor can activate a line by sending and SMS message
to the Gateway's phone number. The Gateway sends the Meter associated
with the specified <circuit-ID> a job about the pending request. The
Meter performs the requested action and sends the Gateway an
acknowledgement of service completion. When the Gateway server
receives the acknowledgement, it notifies the Consumer by sending the
following message to the phone number where the request originated (as
well as the primary & secondary contact numbers). In the situation
where a Consumer tries to activate a circuit when Emax has been hit or
there is zero credit, the Gateway does not accept the Consumer's
request but instead notifies the consumer through one of the following
messages.

MM 1) Consumer to Gateway::

    ON.<account-number>

MM 2) Gateway to Meter::

    (con&<cid>&<jobid>)

MM 3) Meter to Gateway::

    (delete&<cid>&<jobid>&<ts>&<wh>&<status> &<tu>&<ct>&<cr>)

MM 4a) Gateway to Consumer::

     Account <account-number> is <relay-state>. Remaining credit:
     <energy-credit-balance>

MM 4b1) (If Time-out reached) Gateway to Consumer::

     Your request to activate to account <account-number>
     failed. Remaining credit: <energy-credit-balance>. Status:
     <relay-state>

MM 4b2) (If Time-out reached) Gateway Operator Component Failure Alarm::

     <time-stamp> / COMPONENT FAILURE / Meter <mid> is unresponsive.

MM 4c) (If Zero credit) Gateway to Consumer::

     Your request to activate your account <account-number>
     failed. Remaining credit is zero. Please add more credit to your
     account.

MM 4d) (If Emax) Gateway Operator Component Failure Alarm::

    Your request to activate your account <account-number> failed. The
    maximum daily energy has been consumed. You may re-activate your
    account tomorrow.

3.1.2.1 Translations

ENGLISH & FRENCH:

ON.<account-number>

ENGLISH:

Account <account-number> is <relay-state>. Remaining credit: <energy-credit-balance>

FRENCH:

<realy-state>. La ligne <account-number> est <relay-state>. Solde restant: <energy-credit-balance>.

ENGLISH:

Your request to activate your account <account-number> failed. Remaining credit is zero. Please add more credit to your account.

FRENCH:

ÉCHEC. Vous ne pouvez pas activer la ligne <account-number> car le solde est zéro. Ajoutez des unités d'abord.

ENGLISH:

Your request to activate your account <account-number> failed. The maximum daily energy has been consumed. Your account will be automatically re-activated tomorrow.

FRENCH:

ÉCHEC. Vous ne pouvez pas activer la ligne <account-number> car vous avez dépassé la limite journalière. Vous devrez la réactiver demain.

3.1.3 Putting service on hold

The system allows for Consumers / Vendors to place a circuit on hold so as not to incur any usage on it until it is activated. They can do this by sending the following SMS Message to the Gateway phone number. As in the case of activating a line, the Gateway forwards this request to the appropriate Meter and notifies the Consumer of the resulting status by sending a SMS Message to the phone number where the request originated (as well as the primary & secondary contact numbers). In the case of successful completion, the Gateway responds with.

MM 1) Consumer to Gateway:

OFF.<account-number>

MM 2) Gateway to Meter:

(coff&<cid>&<jobid>)

MM 3) Meter to Gateway:

(delete&<cid>&<jobid>&<ts>&<wh>&<status> &<tu>&<ct>&<cr>)

MM 4a) Gateway to Consumer:

Account <account-number> is <relay-state>. Remaining credit: <energy-credit-balance>

MM 4b1) (If Time-out reached) Gateway to Consumer: 

Your request to put your service on hold for account <account-number> failed. Remaining credit: <energy-credit-balance>. Status: <relay-state>

3.1.3.1 Translations:

ENGLISH & FRENCH:

OFF.<account-number>

ENGLISH:

Account <account-number> is <relay-state>. Remaining credit: <energy-credit-balance>

FRENCH:

<realy-state>. La ligne <account-number> est <relay-state>. Solde restant: <energy-credit-balance>.

ENGLISH:

Your request to put your service on hold for account <account-number> failed. Remaining credit: <energy-credit-balance>. Status: <relay-state>

FRENCH:

ÉCHEC. L'ajout de crédit sur la ligne <account-number> a échoué. Solde restant: <energy-credit-balance>. Statut: <relay-state>.

3.1.4 Balance Inquiry

A Consumer purchases Energy Credit in the form of a token on a scratch-card which is associated with a physical line when activated. They can query the balance on this Energy Credit by sending the following SMS Message to the Gateway phone number. The Gateway responds by sending the following to the phone number it received the request from. Note that the Gateway calculates the balance based on the values in the database per the last communication with the meter; it does not contact the meter to get the very latest information. As such, the time-stamp must reflect this and be for the time/day relative to the information presented.

MM 1) Consumer to Gateway:

bal.<account-number>

MM 2) Gateway to Consumer:

The remaining electricity credit on account <account-number> is <energy-credit-balance> as of <time-stamp>

3.1.4.1 Translations

ENGLISH:

bal.<account-number>

FRENCH:

solde.<numero_compte> 

ENGLISH:

The remaining electricity credit on account <account-number> is <energy-credit-balance> as of <time-stamp>

FRENCH:

<energy-credit-balance> unités. Il restait <energy-credit-balance> unités sur la ligne <account-number> le <time-stamp>.

3.1.5 Energy Usage Statistics

The Consumer can request the energy usage statistics for their registered line. The Consumer sends the following SMS Message to the Gateway phone number. The Gateway responds by sending the following to the phone number it received the request from. Note that the Gateway calculates the statistics based on the values in the database per the last communication with the meter; it does not contact the meter to get the very latest information. As such, the time-stamp must reflect this and be for the time/day relative to the information presented.

MM 1) Consumer to Gateway:

use.<account-number>

MM 2) Gateway to Consumer:

Over the last 30 days, account <account-number> has had the following use: avg wh/d:<avg.watt-hours per day>, avg w:<avg. watts>, max w:<max watts>, min w:<min watts>, avg h/d:<average hours of use per day>

3.1.5.1 Translations

ENGLISH:

use.<account-number>

FRENCH:

conso.<numero_compte> 

ENGLISH:

Over the last 30 days, account <account-number> has had the following use: avg wh/d:<avg.watt-hours per day>, avg w:<avg. watts>, max w:<max watts>, min w:<min watts>, avg h/d:<average hours of use per day>

FRENCH:

Statistiques de la ligne <account-number sur les 30 derniers jours: Moyenne: <avg.watt-hours per day>Wh/j, <avg. watts>W, max: <max watts>W, min: <min watts>W, utilisation moyenne: <average hours of use per day>h/jours.

3.1.6 Primary Contact Number

A Consumer can overwrite/replace their primary contact phone number. The gateway responds to this action by 1) overwriting the previous primary contact number with the new contact number, and 2) sending the following SMS to both the new and old primary contact numbers (as well as the phone number that placed the SMS, if it is different from the other two numbers).

MM 1) Consumer to Gateway:

prim.<account-number>.<primary-contact-number>

MM 2) Gateway to Consumer:

The previous primary contact number <old-primary-contact-number> has been replaced with the number <new-primary-contact-number>.

3.1.6.1 Translations

ENGLISH:

prim.<account-number>.<primary-contact-number>

FRENCH:

tel.<numero_compte>.<numero_tel>

ENGLISH:

The previous primary contact number <old-primary-contact-number> has been replaced with the number <new-primary-contact-number>.

FRENCH:

Votre numéro de contact est désormais <new-primary-contact-number>. Le numéro <old-primary-contact-number> ne sera plus utilisé.

3.2 Gateway Initiated Messaging

3.2.1 Administrator Alerts

The Gateway sends SMS Messages to the Consumers to notify them of alerts and warnings. These could be in the form of system-wide messages sent out by the administrators for things like service interruption due to maintenance.

These are service advisories sent out by the Gateway administrators to the Consumers. (An example situation is a planned power outage requiring the system to be temporarily turned off for repair or upgrade.) These alerts will be descriptive (but < 160 characters in length) SMS Messages.

3.2.2 Ping Mains

MM 1) Gateway to Meter:

(mping)

MM 2) Meter to Gateway:

(delete&<mid>&<jobid>&<ts>&<wh>&<status>&<tu>&<ct>)

3.2.3 Ping Circuit's Primary Parameters

MM 1) Gateway to Meter:

(cping&<cid>)

MM 2) Meter to Gateway:

(delete&<cid>&<jobid>&<ts>&<wh>&<status>&<tu>&<ct>&<cr>)

3.2.4 Ping SD Card

MM 1) Gateway to Meter:

(sdping)

MM 2) Meter to Gateway:

(delete&<cid>&<jobid>&<ts>&<wh>&<status>&<tu>&<ct>&<cr>)

3.2.5 Updating the Meter Configuration

[NEEDS TO BE CONFIRMED]

MM 1) Gateway to Meter:

(um&<NAME>&<LOW_CREDIT_THRESHOLD>&<GPS_LATITUDE>&<FREQ_COMPONENT_FAILURE_CHECK>&<FREQ_GATEWAY_JOB_REQUEST>&<CACHE_TIME>&<PERSIST_UPDATE_TIME>&<MODE>&<PPPD_PEER>&<FREQ_PRIMARY_PARAMETER_TRANSMISSION>&<LOGS_HOME>&<GPS_LONGITUDE>&<IP_ADDRESS>& <GATEWAY>)

MM 2) Meter to Gateway:

(delete&<mid>&<jobid>&<ts>&<wh>&<status>&<tu>&<ct>)

3.2.6 Updating the Circuit Configuration

[NEEDS TO BE CONFIRMED]

MM 1) Gateway to Meter:

(uc&<PRICING_MODEL>&<IP_ADDRESS>&<NUM_WARNING_SIGNALS>&<ENERGY_MAX>&<POWER_MAX>&<ACTIVE>&<SERIAL>)

MM 2) Meter to Gateway:

(delete&<cid>&<jobid>&<ts>&<wh>&<status>&<tu>&<ct>&<cr>)

3.2.7 Updating the Pricing Model Configuration

[NEEDS TO BE CONFIRMED]

MM 1) Gateway to Meter:

(upm&<BASELINE_RATE>&<POWER_HIGH>&<NAME>&<POWER_LOW>&<POWER_MID_MULT>&<ENERGY_THRESHOLD>&<ENERGY_HIGH_MULT>&<TIME_NIGHT_START>&<ENERGY_LOW_MULT>&<TIME_DAY_START>&<POWER_HIGH_MULT>&<DAY_MULT>&<POWER_LOW_MULT>&<ID>&<NIGHT_MULT>)

MM 2) Meter to Gateway:

(delete&<cid>&<jobid>&<ts>&<wh>&<status>&<tu>&<ct>&<cr>)

3.2.8 Querying Secondary Parameters

[NEED TO DEFINE TIME RANGE OVER WHICH THESE PARAMETERS ARE TAKEN]

The Gateway server can query the Secondary Parameters of circuit(s) associated with a Meter by sending the following SMS:

(sp&<jobID>&<cid1>&<cid2>&<cidN>)

The Meter responds with an SMS for each requested circuit:

(sp&<jobID>&<cid>&<voltage>&<current>&<frequency>&<power-factor>)

3.3 Meter Initiated Messaging

3.3.1 Primary Parameter Transmission

The Meters send the recorded Primary Parameters per circuit to the Gateway server every hour. 

MM 1) Consumer to Gateway:

(pp&<ts>&<mid> (<cid>&<wh>&<status>&<tu>&<ct>&<cr>)(<cid>&<wh>&<status>&<tu>&<ct>&<cr>))

Note that the transmission of the watt-hours (and time used) is the watt-hours (and time used) accumulated THAT DAY up to the point of transmission (as designated by the time stamp), not the total running balance. The meter resets a circuit's watt-hour accumulator (and time used accumulator) at the end of each day.

Note that “tu” (time used) is the number of accumulated minutes during the day in which the meter detected a load (i.e., current was greater than zero).

3.3.2 Low Credit

The Gateway notifies the Consumer when their account is approaching a point of insufficient funds (when their credit falls below a TBD value). The Gateway sends a message to the Consumer's preferred contact number with a short description and the remaining credit on the account, as shown below.

MM 1) Meter to Gateway:

(lcw&<mid>&<cid>&<cr>)

MM 2) Gateway to Consumer:

Your electricity account <account-number> balance is low. Your remaining balance is less than <TBD Value>, as of <time-stamp>.

3.3.2.1 Translations

ENGLISH: 

Your electricity account <account-number> balance is low. Your remaining balance is less than <TBD Value>, as of <time-stamp>.

FRENCH:

SOLDE <TBD Value>. Le solde de votre compte <account-number> est bas. Le <time-stamp>, il vous restait <TBD Value>.

3.3.3 Zero Credit

In the event the Consumer was unable to recharge credit on their line(s) and there is no credit remaining, the Meters turn off service on those line(s) and the Gateway notifies the primary and secondary contact numbers of the same. The message sent would be. Note that even once credit has been added the circuit will stay off, it is the consumer's responsibility to send an “ON” (activation) SMS after (in addition to) adding credit.

MM 1) Meter to Gateway:

(nocw&<mid>&<cid>&<cr>)

MM 2) Gateway to Consumer:

Your electricity account <account-number> has been turned off due to insufficient funds, as of <time-stamp>.

3.3.3.1 Translations

ENGLISH:

Your electricity account <account-number> has been turned off due to insufficient funds, as of <time-stamp>.

FRENCH:

CREDIT INSUFFISANT. La ligne <account-number> a été coupée le <time-stamp> car son solde était insuffisant.

3.3.4 Emax

In the event the Consumer surpassed the daily energy consumption alotment (Emax), the Meters turn off service on those line(s) and the Gateway notifies the primary and secondary contact numbers of the same. The message sent would be. At 12am the following day, their account will be allowed to be re-activated. However, please note that the gateway/meter does not re-activate automatically, it is the consumer's responsibility to send an “ON” (activation) SMS the next day. 

MM 1) Meter to Gateway:

(emax&<mid>&<cid>&<wh>)

MM 2) Gateway to Consumer:

Your electricity account <account-number> has been turned off as of <time-stamp>. The maximum daily energy has been consumed. You may re-activate your account tomorrow.

3.3.4.1 Translations

ENGLISH:

Your electricity account <account-number> has been turned off as of <time-stamp>. The maximum daily energy has been consumed. You may re-activate your account tomorrow.

FRENCH:

LIGNE COUPÉE. La ligne <account-number> a été coupée le <time-stamp> car la elle a dépassée la consomation maximale pour une journée. Vous devrez la réactiver demain.

3.3.5 Pmax

In the event the Consumer surpassed the allowed power draw (Pmax), the Meters turn off service on those line(s) and the Gateway notifies the primary and secondary contact numbers of the same. The message sent would be. If a consumer re-activates their account without reducing their load, they will again have their service put on hold and receive the identical message as above. (Note that similarly to Zero Credit & Emax, the consumer is responsible for re-activatin their account.)

MM 1) Meter to Gateway:

(pmax&<mid>&<cid>&<wh>)

MM 2) Gateway to Consumer:

Your electricity account <account-number> has been turned off as of <time-stamp>. The maximum allowed power has been exceeded. Reduce load and reactivate your account.

3.3.5.1 Translations

ENGLISH:

Your electricity account <account-number> has been turned off as of <time-stamp>. The maximum allowed power has been exceeded. Reduce load and reactivate your account.

FRENCH:

LIGNE COUPÉE. La ligne <account-number> a été coupée le <time-stamp> car la puissance maximale autorisée a été dépassée. Vous devrez la réactiver demain.

3.3.6 Meter Down

MM 1) Meter to Gateway:

(md&<mid>)

3.3.7 SD Card not found

MM 1) Meter to Gateway:

(sdc&<mid>)

3.3.8 Component Failure Notifications

When the Meter does not receive any response from a circuit, it sends a notification to the Gateway server in the form of the request shown below.

The Gateway will innitiate a dashboard alarm to notify the Gateway operator of the communication issue. The alarm will read as follows.

MM 1) Meter to Gateway:

(ce&<mid>&<cid>)

Chapter 4 The Gateway

4.1 Temporary Fix: SMS-Buffer

During the period of deployment before an SMPP contract is obtained with the local Mobile Network Operator (Orange, MaliTel), a stop-gap will need to be implemented. An “SMS-Buffering” device for forwarding SMS to/from the gateway. This SMS-Buffer will be created to 1) receive consumer SMS's and forward them to the Gateway, 2) forward SMS's from the Gateway to the consumer, and 3) send an SMS to the consumer letting them know their message has been received and is being processed. 

4.1.1 Location

Where as the Gateway will be located on a server outside of Mali, the SMS-Buffer will be a local netbook with a modem in Mali.

4.1.2 Acknowledgement SMS

Whenever the SMS-Buffer receives an SMS from a consumer it will immediately reply:

Your SMS has been received and will be processed shortly. There may be a brief delay before your request is completed.

This aknowledgement SMS is meant to prevent consumers from sending requests multiple times in the situation where there is a delay between the consumer sending their SMS, the SMS-Buffer receiving their SMS and forwarding it to the Gateway, the Gateway receiving the SMS, and the request being executed.

4.1.3 Buffering During Service Outage

The SMS-Buffer will need to be able to both:

1. Buffer during Internet Outages: retain received SMS's from the consumer during internet outages, keeping a queue of these messages and not dropping them during internet outages, but storing them and finally forwarding them to the gateway once internet connectivity has resumed

2. Buffer during Mobile Network Outages: retain SMS's received from the Gateway during mobile network outages, keeping a queue of these messages and not dropping them during the mobile network outage, but storing them and finally forwarding them to the Consumers once mobile network connectivity has resumed

4.2 Temporary Fix: Crediting Consumer Energy Credit for Air-time Spent

Until the SMPP contract is obtained we will need a “mechanism” for “preventing” consumers from having to pay to SMS the Gateway. A temporary fix will be to give them energy credit equivalent to the cost of the SMS's they send to the Gateway.

During this pre-SMPP contract phase, whenever the consumer sends any SMS to the gateway, the Gateway will need to credit their account an additional 50 CFA.

4.3 Front-end

4.3.1 Operator Alarm System

4.3.1.1 Service Interrupted

<insert>

4.3.1.2 Circuit Meter Communication Lost

<insert>

4.3.1.3 Meter Communication Lost

<insert>

4.3.1.4 SD Card Missing

<insert>

4.3.2 Communication Monitor System

4.3.2.1 Administrative Alert

<insert>

4.3.2.2 Low Account Balance Alert

<insert>

4.3.2.3 Zero Credit Service Hold

<insert>

4.3.2.4 Emax Service Hold

<insert>

4.3.2.5 Pmax Service Hold

<insert>

4.3.2.6 Balance Inquiry Consumer Message

<insert>

4.3.2.7 Use Statistics Inquiry Consumer Message

<insert>

4.3.2.8 Primary Contact Change Consumer Message

<insert>

4.3.2.9 Adding Credit Consumer Message

<insert>

4.3.2.10 Activating Circuit Consumer Message

<insert>

4.3.2.11 Putting Service on Hold Consumer Message

<insert>

4.3.3 Diagnostics System

<insert>

4.3.3.1 Ping a Meter & Circuit (return status)

<insert>

4.3.4 Graphs

A mock-up for the wire-frame is shown in Figure[fig:Graphs-Page-Wireframe]. The first box on the left is labeled “circuits.” Instead of only circuits, it should include Meters and Circuits, and it should be titled “Select Data Source:”, the next box that is labeled “Parameters” in the figure, should actually be labeled “Select Data Type.”



4.3.4.1 Meter Power Consumption

For the first graph to be implemented there should only be Meters in the “Select Data Source:” box, and there should only be “Power” in the “Select Data Type:” box. A user should be able to graph a single meter's power consumption over time. The Y-axis is the power (watts) and the X-axis is time (the interval specified by the user). The power will need to be calculated by taking the watt-hours divided by the “time-used” (TU).

4.3.4.2 Watt-hour Consumption

Y-axis is a consumer's watt-hour consumption (running total), the x-axis is time.

4.3.4.3 Credit Balance

Y-axis is the consumer's credit balance, the x-axis is time.

4.3.4.4 Credit Addition

The Y-axis is the magnitude of the credit added, the x-axis is time. Instead of “scatter” type plot, this could be a “bar-chart” showing the magnitude and occurance of each credit purchase.

4.3.4.5 Circuit On/Off



4.3.4.6 System Energy Allocation

same as circuit on/off but instead of just green = on and red = off... now one extreme color (red) equals the consumer has maxed out their energy allocation, and the other extreme color (green) means they have not used any. Anything in between is appropriately scaled between the two colors.

4.4 Back-end

4.4.1 Meter Database Fields

4.4.1.1 dbid

(Meter.id) The dbid is the unique ID number utilized primarily by the Gateway database. (Note that the dbid is related to one unique SC20 serial number and a circuit-ID which is not unique but repeated every meter.)

4.4.1.2 meter-ID

(Meter.???) The meter-ID is the IP address of the meter. The last three digits are unique to the system, and can span the values 100 through 199.

4.4.1.3 Name

(Meter.name) This is a string that names the meter.

4.4.1.4 SC20 serial number

(Meter.???) The serial number is a unique ID associated with the actual SC20 hardware.

4.4.1.5 Phone Number

(Meter.phone) This is the actual phone number associated with the SIM card contained in the meter.

4.4.1.6 Relay State

(Meter.status???) This is the relay state of the circuit (on/off). It can be changed at the gateway. (If the gateway operator manually changes the status, then an SMS alert should be automatically sent to the Consumer indicating this change.)

4.4.1.7 Location

(Meter.location) This is a string that describes the physical location of the meter (likely the community or village name).

4.4.1.8 Total Circuits

(Meter.???) This is the total number of circuits that are physically connected to this meter.

4.4.1.9 Active Circuits

(Meter.???) This is the total number of active (on) circuits that are physically connected to this meter. The number of Active Circuits is less than or equal to the number of Total Circuits.

4.4.1.10 Panel Capacity

(Meter.panel_capacity) This is a string that describes the amount of installed Solar PV panel capacity. It is in units of kW, and may have a decimal value (i.e., “1.5 kW”).

4.4.1.11 Battery Capacity

(Meter.battery) This is a string that describes the amount of installed energy storage (battery) capacity and is in units of kWh.

4.4.1.12 GPS Lat

(Meter.gps_lat) This is the Latitude associated with the physical location of the meter.

4.4.1.13 GPS Long

(Meter.gps_long) This is the Longitude assocaited with the physical location of the meter.

4.4.1.14 Communication Timestamp

(Meter.???) This is the date and time at which the last successful transmission was received from the Meter. The format is YYYY/MM/DD/HH/SS.

4.4.2 Circuit Database Fields

4.4.2.1 dbid

(Circuit.id) The dbid is the unique ID number utilized primarily by the Gateway database. (Note that the dbid is related to one unique SC20 serial number and a circuit-ID which is not unique but repeated every meter.)

4.4.2.2 Meter Name

(Circuit.meter) This is a string that names the meter, which the circuit is associated with.

4.4.2.3 Terminal#

(Circuit.slot) This is the number that describes the physical connection point that a field technician attaches a wire to. The possible values are 1 through 20. It is directly related to the circuit-ID as described below. 

4.4.2.4 circuit-ID

(Circuit.serialid) This is the IP address associated with the specific circuit. It will end in 201 through 220. It corresponds to the Terminal#, in that a Terminal# with a value of 3 should have a circuit-ID of xxx.xx.xxx.203.

4.4.2.5 account-number

(Circuit.???) The account number is a unique ID associated with a consumer's account. (Note that the dbid is related to one unique serial number and a circuit-ID which is not unique but repeated every meter.)

4.4.2.6 Emax

(Circuit.emax) This is the maximum energy available to the consumer in a given day (midnight to midnight). 

4.4.2.7 Pmax

(Circuit.pmax) This is the maximum power that a consumer can draw at any given instant. 

4.4.2.8 Pricing Model

(Circuit.???) This is the name of the pricing model that has been assigned to this circuit. (Note that pricing models are selected through this field, but defined through a separate UI.)

4.4.2.9 GPS Lat

(Circuit.gps_lat) This is the Latitude associated with the physical location of the meter.

4.4.2.10 GPS Long

(Circuit.gps_long) This is the Longitude assocaited with the physical location of the meter.

4.4.2.11 Primary Contact Number

(Circuit.primary_contact) This is the phone number that is used to send alerts to, etc., associated with this circuit.

4.4.2.12 Additional Contact Numbers

(Circuit.additional_contacts) These are optional phone numbers that can be associated with a circuit, and will also receive alerts.

4.4.2.13 Relay State

(Circuit.status???) This is the relay state of the circuit (on/off). It can be changed at the gateway. (If the gateway operator manually changes the status, then an SMS alert should be automatically sent to the Consumer indicating this change.)

4.4.2.14 Account State

(Circuit.???) The Gateway Operator can over-ride DB values, but it is their responsibility to change those DB values back to their appropriate values after they have over-ridden them. For example, perhaps a circuit needs to be tested, so the operator sets the DB values for the account credit, Emax, and Pmax, to be very high; after the testing they are responsible to manually change the settings back.

The meter logic however, has a higher priority than the consumer messaging on/off control, as shown in [fig:Relay-ON/OFF-Account]below.



4.4.2.15 Energy-credit

(Circuit.credit) This is the available energy-credit associated with the account associated with this circuit. It should be accurate per the last communication with the Meter (as noted by the Communication Timestamp).

4.4.2.16 Total Watt-hours

(Circuit.???) This is the total energy consumed by this circuit since it was installed. It is the grand running total.

4.4.2.17 30 day watt-hours

(Circuit.???) This is the total energy consumed by this circuit during the last 30 days.

4.4.2.18 Yesterday watt-hours

(Circuit.???) This is the total energy consumed by this circuit during the previous calendar day (midnight to midnight).

4.4.2.19 Past 24 hour watt-hours

(Circuit.???) This is the total energy consumed by the circuit during the previous 24 hours (calculated based on current time viewed).

4.4.2.20 1 hour watt-hours

(Circuit.???) This is the total energy consumed by the circuit during the last hour (this is the value passed from the Meter to the gateway during the last scheduled hourly transmission; if transmission was unsuccessful, then an “unknown” value is displayed).

4.4.2.21 Communication Timestamp

(Circuit.???) This is the date and time at which the last successful transmission was received from the Meter, and included information on the specific status of this circuit. The format is YYYY/MM/DD/HH/SS.





