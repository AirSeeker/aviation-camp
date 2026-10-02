<figure>
<img src="/images/EASA_SERA/ch16/img_p215_1.png" alt="Figure 215-1" />
<figcaption>Figure 215-1 · PDF p. 215</figcaption>
</figure>

<strong>SECTION</strong><strong> </strong><strong>15</strong><strong> </strong><strong>C</strong><strong>ONTROLLER</strong><strong>-</strong><strong>PILOT DATA LINK COMMUNICATION </strong>
<strong>SERA.15001 Data link initiation and data link initiation failure </strong>
(a) 
The logon address associated with an air traffic services unit shall be published in the national 
aeronautical information publications (AIPs). 
(b) 
Upon receipt of a valid data link initiation request from an aircraft approaching or within the 
data link service area, the air traffic services unit shall accept the request and, if able to correlate 
it with a flight plan, shall establish a connection with the aircraft. 
(c) 
The air traffic services provider shall establish procedures to resolve, as soon as practicable, 
data link initiation failures. 
(d) 
The aircraft operator shall establish procedures to resolve, as soon as practicable, data link 
initiation failures. 
<strong>SERA.15005 Establishment of CPDLC </strong>
(a) 
CPDLC shall be established in sufficient time in advance to ensure that the aircraft 
communicates with the appropriate air traffic control unit. 
(b) 
Information concerning when and, if applicable, where the air or ground systems should 
establish CPDLC shall be published in aeronautical information circulars or publications. 
(c) 
The pilot shall be able to identify the air traffic control unit that provides the air traffic control 
service at any time while the service is being provided. 
<strong>SERA.15010 Transfer of CPDLC </strong>
(a) 
When CPDLC is transferred, the transfer of voice communication and CPDLC shall commence 
concurrently. 
(b) 
When an aircraft is transferred from an air traffic control unit where CPDLC is available to an air 
traffic control unit where CPDLC is not available, the termination of CPDLC shall commence 
concurrently with the transfer of voice communication. 
(c) 
The air traffic controller shall be informed when attempting a transfer of CPDLC resulting in a 
change in data authority if there are data link messages for which a closure response has not 
been received. When the air traffic controller decides to transfer the aircraft without receiving 
pilot responses to the uplink message(s) outstanding, the air traffic controller shall normally 
revert to voice communication to clarify any ambiguity associated with the uplink message(s) 
outstanding. 
<strong>(CPDLC)</strong><strong> PROCEDURES</strong><strong> </strong>
<em>SECTION 15 Controller-pilot data </em>
<em>link communication (CPDLC) </em>
<em>procedures </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
Page 215 of 275| Aug 2025 

<figure>
<img src="/images/EASA_SERA/ch16/img_p215_1.png" alt="Figure 215-1" />
<figcaption>Figure 215-1 · PDF p. 216</figcaption>
</figure>

<strong>SERA.15015 Construction of CPDLC messages </strong>
(a) 
The text of CPDLC messages shall be composed in standard message format, in plain language, 
or in abbreviations and codes. Plain language shall be avoided when the length of the text can 
be reduced by using appropriate abbreviations and codes. Non-essential words and phrases, 
such as expressions of politeness, shall not be used. 
(b) 
The air traffic controller and the pilot shall construct CPDLC messages using standard message 
elements, free text message elements, or a combination of both. The use of free text message 
elements by air traffic controllers or pilots shall, be avoided. 
(c) 
When the implemented CPDLC message set does not provide for specific circumstances, the 
competent authority may determine, in consultation with operators and other air traffic 
services providers, that it is acceptable to use free text message elements. In such cases, the 
competent authority concerned shall define the display format, intended use and attributes for 
each free text message element. 
(d) 
The composition of a CPDLC message shall not exceed five message elements, only two of which 
may contain the route clearance variable. 
(e) 
Construction of multi-element CPDLC messages: 
(1) 
When a multi-element CPDLC message requires a response, the response shall apply to 
all message elements. 
(2) 
When a single message element clearance or any part of a multi-element clearance 
message cannot be complied with, the pilot shall send an “UNABLE” response for the 
whole message. 
(3) 
The controller shall respond with an “UNABLE” message that applies to all elements of 
the request when no element(s) of a single or multi-element clearance request can be 
approved. The current clearance(s) shall not be restated. 
(4) 
When a multi-element clearance request can only be partially accommodated, the 
controller shall respond with an “UNABLE” message applying to all the message elements 
of the request and, if appropriate, include a reason and/or information on when 
clearance may be expected. 
(5) 
When all elements of a single or multi-element clearance request can be accommodated, 
the controller shall respond with clearances corresponding to each element of the 
request. This response shall be a single uplink message. 
(6) 
When a CPDLC message contains more than one message element and the response 
attribute for the message is “Y”, when utilised, the single response message shall contain 
the corresponding number of replies in the same order. 
<strong>SERA.15020 Responding to CPDLC messages </strong>
(a) 
Unless otherwise specified by the competent authority, voice read-back of CPDLC messages 
shall not be required. 
(b) 
Except when correction of the CPDLC message transmitted is needed, when a controller or a 
pilot communicates via CPDLC, the response shall normally be via CPDLC. When a controller or 
a pilot communicates via voice, the response shall normally be via voice. 
<em>SECTION 15 Controller-pilot data </em>
<em>link communication (CPDLC) </em>
<em>procedures </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
Page 216 of 275| Aug 2025 

<figure>
<img src="/images/EASA_SERA/ch16/img_p215_1.png" alt="Figure 215-1" />
<figcaption>Figure 215-1 · PDF p. 217</figcaption>
</figure>

<strong>SERA.15025 Correction of CPDLC messages </strong>
(a) 
When a correction to a CPDLC message is deemed necessary or when the contents of such a 
message need to be clarified, the air traffic controller and the pilot shall use the most 
appropriate means available for issuing the correct details or for providing the necessary 
clarification. 
(b) 
When voice communication is used to correct a CPDLC message for which no operational 
response has yet been received, the controller’s or the pilot’s voice transmission shall be 
prefaced by the phrase: “DISREGARD CPDLC (message type) MESSAGE, BREAK” – followed by 
the correct clearance, instruction, information or request. 
(c) 
When referring to and identifying the CPDLC message to be disregarded, caution shall be 
exercised in its phrasing so as to avoid any ambiguity with the issue of the correction to the 
clearance, instruction, information or request. 
(d) 
If a CPDLC message that requires an operational response is subsequently negotiated via voice, 
an appropriate CPDLC message closure response shall be sent to ensure proper synchronisation 
of the CPDLC dialogue. This may be achieved either by explicitly instructing the recipient of the 
message via voice to close the dialogue or by allowing the system to automatically close the 
dialogue. 
<strong>SERA.15030 Controller data link communication procedures for </strong>
<strong>emergencies, hazards, and CPDLC equipment failure </strong>
(a) 
When an air traffic controller or a pilot is alerted that a single controller-pilot data link 
communication message has failed, the air traffic controller or the pilot shall take one of the 
following actions, as appropriate: 
(1) 
via voice, confirm the actions that will be taken with respect to the related dialogue, 
prefacing the information with the phrase: “CPDLC MESSAGE FAILURE”; 
(2) 
via controller-pilot data link communication, reissue the controller-pilot data link 
communication message that failed. 
(b) 
Air traffic controllers that are required to transmit information concerning a complete 
controller-pilot data link communication ground system failure to all stations likely to intercept 
should preface such a transmission by the general call: “ALL STATIONS CPDLC FAILURE” - 
followed by the identification of the calling station. 
(c) 
When controller-pilot data link communication fail and the communication reverts to voice, all 
CPDLC messages outstanding shall be considered not delivered and the entire dialogue involving 
the messages outstanding shall be recommenced by voice. 
(d) 
When controller-pilot data link communication fails but is restored prior to a need to revert to 
voice communication, all messages outstanding shall be considered not delivered and the entire 
dialogue involving the messages outstanding shall be recommenced via CPDLC. 
<em>SECTION 15 Controller-pilot data </em>
<em>link communication (CPDLC) </em>
<em>procedures </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
Page 217 of 275| Aug 2025 

<figure>
<img src="/images/EASA_SERA/ch16/img_p215_1.png" alt="Figure 215-1" />
<figcaption>Figure 215-1 · PDF p. 218</figcaption>
</figure>

<strong>SERA.15035 Intentional shutdown of CPDLC system </strong>
(a) 
When a system shutdown of the communications network or the CPDLC ground system is 
planned, a NOTAM shall be published to inform all affected parties of the shutdown period and, 
if necessary, the details of the voice communication frequencies to be used. 
(b) 
Aircraft in communication with the ATC units shall be informed by voice or CPDLC of any 
imminent loss of the CPDLC service. 
<strong>SERA.15040 Discontinuation of the use of CPDLC requests </strong>
(a) 
When a controller requires all stations or a specific flight to avoid sending CPDLC requests for a 
limited period of time, the following phrase shall be used: ((call sign) or ALL STATIONS) STOP 
SENDING CPDLC REQUESTS [UNTIL ADVISED] [(reason)]. 
(b) 
The resumption of the normal use of CPDLC shall be advised by using the following phrase: ((call 
sign) or ALL STATIONS) RESUME NORMAL CPDLC OPERATIONS. 
<strong>SERA.15045 Use of CPDLC in the event of air-ground voice </strong>
<strong>communication failure </strong>
The existence of a CPDLC connection between an air traffic services unit and an aircraft should not 
prevent the pilot and the air traffic controller concerned from initiating and performing all the 
required actions in the event of air-ground voice communication failure. 
<strong>SERA.15050 Testing of CPDLC </strong>
Where the testing of CPDLC with an aircraft could affect the air traffic services being provided to the 
aircraft, coordination shall be effected prior to such testing. 
<em>SECTION 15 Controller-pilot data </em>
<em>link communication (CPDLC) </em>
<em>procedures </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
<em>Regulation (EU) 2023/1772</em><em> </em>
Page 218 of 275| Aug 2025