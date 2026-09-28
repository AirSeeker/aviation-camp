Chapter 9
Navigation
Systems
P|
Introduction
This chapter provides the basic radio principles applicable to
navigation equipment, as well as an operational knowledge
of how to use these systems in instrument flight. This
information provides the framework for all instrument
procedures, including standard instrument departure
procedures (SIDS), departure procedures (DPs), holding
patterns, and approaches, because each of these maneuvers
consists mainly of accurate attitude instrument flying and
accurate tracking using navigation systems.
9-1

Basic Radio Principles
A radio wave is an electromagnetic (EM) wave with
frequency characteristics that make it useful. The wave
travels long distances through space (in or out of the
atmosphere) without losing too much strength. An antenna
is used to convert electric current into a radio wave so it can
travel through space to the receiving antenna, which converts
it back into an electric current for use by a receiver.
How Radio Waves Propagate
All matter has a varying degree of conductivity or resistance
to radio waves. The Earth itself acts as the greatest resistor
to radio waves. Radiated energy that travels near the ground
induces a voltage in the ground that subtracts energy from the
wave, decreasing the strength of the wave as the distance from
the antenna becomes greater. Trees, buildings, and mineral
deposits affect the strength to varying degrees. Radiated
energy in the upper atmosphere is likewise affected as the
energy of radiation is absorbed by molecules of air, water,
and dust. The characteristics of radio wave propagation vary
according to the signal frequency and the design, use, and
limitations of the equipment.
Ground Wave
A ground wave travels across the surface of the Earth. You
can best imagine a ground wave’s path as being in a tunnel
or alley bounded by the surface of the Earth and by the
ionosphere, which keeps the ground wave from going out
into space. Generally, the lower the frequency, the farther
the signal travels.
Ground waves are usable for navigation purposes because
they travel reliably and predictably along the same route
day after day and are not influenced by too many outside
factors. The ground wave frequency range is generally from
the lowest frequencies in the radio range (perhaps as low as
100 Hz) up to approximately 1,000 kHz (1 MHz). Although
there is a ground wave component to frequencies above this,
up to 30 MHz, the ground wave at these higher frequencies
loses strength over very short distances.
Sky Wave
The sky wave, at frequencies of 1 to 30 MHz, is good for
long distances because these frequencies are refracted or
“bent” by the ionosphere, causing the signal to be sent back
to Earth from high in the sky and received great distances
away. [Figure 9-1] Used by high frequency (HF) radios in
aircraft, messages can be sent across oceans using only 50
to 100 watts of power. Frequencies that produce a sky wave
are not used for navigation because the pathway of the signal
from transmitter to receiver is highly variable. The wave is
9-2
Not refracted
Space wave
Ionosphere
Sky wave
Ground wave
i
,
~~
P|
ij
Figure 7-1. Ground, space, and sky wave propagation.
Figure 9-1. Ground, space, and sky wave propogation.
“bounced” off of the ionosphere, which is always changing
due to the varying amount of the sun’s radiation reaching it
(night/day and seasonal variations, sunspot activity, etc.). The
sky wave is, therefore, unreliable for navigation purposes.
For aeronautical communication purposes, the sky wave
(HF) is about 80 to 90 percent reliable. HF is being gradually
replaced by more reliable satellite communication.
Space Wave
When able to pass through the ionosphere, radio waves
of 15 MHz and above (all the way up to many GHz), are
considered space waves. Most navigation systems operate
with signals propagating as space waves. Frequencies above
100 MHz have nearly no ground or sky wave components.
They are space waves, but (except for global positioning
system (GPS)) the navigation signal is used before it reaches
the ionosphere so the effect of the ionosphere, which can
cause some propagation errors, is minimal. GPS errors
caused by passage through the ionosphere are significant
and are corrected for by the GPS receiver system.
Space waves have another characteristic of concern to users.
Space waves reflect off hard objects and may be blocked if
the object is between the transmitter and the receiver. Site
and terrain error, as well as propeller/rotor modulation error
in very high omnidirectional range (VOR) systems, is caused
by this bounce. Instrument landing system (ILS) course
distortion is also the result of this phenomenon, which led
to the need for establishment of ILS critical areas.

Generally, space waves are “line of sight” receivable, but
those of lower frequencies “bend” somewhat over the
horizon. The VOR signal at 108 to 118 MHz is a lower
frequency than distance measuring equipment (DME) at 962
to 1213 MHz. Therefore, when an aircraft is flown “over the
horizon” from a VOR/DME station, the DME is normally
the first to stop functioning.
Disturbances to Radio Wave Reception
Static distorts the radio wave and interferes with normal
reception of communications and navigation signals. Low-
frequency airborne equipment, such as automatic direction
finder (ADF) and LORAN (LOng RAnge Navigation)
,are particularly subject to static disturbance. Using very
high frequency (VHF) and ultra-high frequency (UHF)
frequencies avoids many of the discharge noise effects.
Static noise heard on navigation or communication radio
frequencies may be a warning of interference with navigation
instrument displays. Some of the problems caused by
precipitation static (P-static) are:
•
Complete loss of VHF communications.
•
Erroneous magnetic compass readings.
•
Aircraft flying with one wing low while using
the autopilot.
•
High-pitched squeal on audio.
•
Motorboat sound on audio.
•
Loss of all avionics.
•
Inoperative very-low frequency (VLF) navigation
system.
•
Erratic instrument readouts.
•
Weak transmissions and poor radio reception.
•
St. Elmo’s Fire.
Traditional Navigation Systems
Nondirectional Radio Beacon (NDB)
The nondirectional radio beacon (NDB) is a ground-based
radio transmitter that transmits radio energy in all directions.
The ADF, when used with an NDB, determines the bearing
from the aircraft to the transmitting station. The indicator
may be mounted in a separate instrument in the aircraft
panel. [Figure 9-2] The ADF needle points to the NDB
ground station to determine the relative bearing (RB) to the
transmitting station. It is the number of degrees measured
clockwise between the aircraft’s heading and the direction
from which the bearing is taken. The aircraft’s magnetic
heading (MH) is the direction the aircraft is pointed with
respect to magnetic north. The magnetic bearing (MB) is the
direction to or from a radio transmitting station measured
relative to magnetic north.
|an’
eal
l an \
a
N
a
W
=
_
E
S
HDG
~~
ADF
KR 87 TSD
ADF
FRQ
J
VOL
-
|
-
|
~
|
~
|
yy
FRQ
FLT
SET
ADF
BFO
OFF
ET
RST
Figure 9-2. ADF indicator instrument and receiver.
Figure 7-2. ADF indicator instrument and receiver.
NDB Components
The ground equipment, the NDB, transmits in the frequency
range of 190 to 535 kHz. Most ADFs also tune the AM
broadcast band frequencies above the NDB band (550 to
1650 kHz). However, these frequencies are not approved
for navigation because stations do not continuously identify
themselves, and they are much more susceptible to sky wave
propagation especially from dusk to dawn. NDB stations
are capable of voice transmission and are often used for
transmitting the Automated Weather Observing System
(AWOS). The aircraft must be in operational range of the
NDB. Coverage depends on the strength of the transmitting
station. Before relying on ADF indications, identify the
station by listening to the Morse code identifier. NDB stations
are usually two letters or an alpha-numeric combination.
ADF Components
The airborne equipment includes two antennas: a receiver
and the indicator instrument. The “sense” antenna (non-
directional) receives signals with nearly equal efficiency
from all directions. The “loop” antenna receives signals
better from two directions (bidirectional). When the loop
and sense antenna inputs are processed together in the ADF
radio, the result is the ability to receive a radio signal well in
all directions but one, thus resolving all directional ambiguity.
The indicator instrument can be one of four kinds: fixed-
card ADF, rotatable compass-card ADF, or radio magnetic
9-3

indicator (RMI) with either one needle or dual needle. Fixed-
|a’
eal
card ADF (also known as the relative bearing indicator (RBI))
l an \
a
always indicates zero at the top of the instrument, with the
needle indicating the RB to the station. Figure 9-3 indicates
N
E
an RB of 135°; if the MH is 045°, the MB to the station is
—_
180°. (MH + RB = MB to the station.)
|a’
al
l an \
=
N
=
_
W
S
HDG
W
E
_
~~
Figure 7-4. Relative bearing (RB) on a movable-card indicator.
Figure 9-4. Relative bearing (RB) on a movable-card indicator. By
placing the aircraft’s magnetic heading (MH) of 045° under the
top index, the RB of 135° to the right is also the magnetic bearing
S
~~
(no wind conditions), which takes you to the transmitting station.
|an’
el
al
l an \
P~
ADF needle
Figure 9-3. Relative bearing (RB) on a fixed-card indicator. Note
Figure 7-3. Relative bearing (RB) on a fixed-card indicator.
N
that the card always indicates 360° or north. In this case, the RB
to the station is 135° to the right. If the aircraft were on a magnetic
heading of 360°, then the magnetic bearing (MB) would also be 135°.
VOR needle
The movable-card ADF allows the pilot to rotate the aircraft’s
present heading to the top of the instrument so that the head
W
E
=
_
of the needle indicates MB to the station and the tail indicates
MB from the station. Figure 9-4 indicates a heading of 045°,
MB to the station of 180°, and MB from the station of 360°.
The RMI differs from the movable-card ADF in that it
automatically rotates the azimuth card (remotely controlled
S
by a gyrocompass) to represent aircraft heading. The RMI
~~
~~
has two needles, which can be used to indicate navigation
information from either the ADF or the VOR receiver. When
a needle is being driven by the ADF, the head of the needle
Figure 7-5. Radio magnetic indicator (RMI).
indicates the MB TO the station tuned on the ADF receiver.
Figure 9-5. Radio magnetic indicator (RMI). Because the aircraft’s
The tail of the needle is the bearing FROM the station. When
magnetic heading (MH) is automatically changed, the relative
a needle of the RMI is driven by a VOR receiver, the needle
bearing (RB), in this case 095°, indicates the magnetic bearing
indicates where the aircraft is radially with respect to the
(095°) to the station (no wind conditions) and the MH that takes
VOR station. The needle points the bearing TO the station
you there.
as read on the azimuth card. The tail of the needle points to
Function of ADF
the radial of the VOR the aircraft is currently on or crossing.
The ADF can be used to plot your position, track inbound
Figure 9-5 indicates a heading of 360°, the MB to the station
and outbound, and intercept a bearing. These procedures
is 005°, and the MB from the station is 185°.
9-4

are used to execute holding patterns and nonprecision
instrument approaches.
Orientation
The ADF needle points TO the station, regardless of aircraft
heading or position. The RB indicated is thus the angular
relationship between the aircraft heading and the station,
measured clockwise from the nose of the aircraft. Think of
the nose/tail and left/right needle indications, visualizing the
ADF dial in terms of the longitudinal axis of the aircraft.
When the needle points to 0°, the nose of the aircraft points
directly to the station; with the pointer on 210°, the station
is 30° to the left of the tail; with the pointer on 090°, the
station is off the right wingtip. The RB alone does not indicate
aircraft position. The RB must be related to aircraft heading
in order to determine direction to or from the station.
Station Passage
When you are near the station, slight deviations from
the desired track result in large deflections of the needle.
Therefore, it is important to establish the correct drift
correction angle as soon as possible. Make small heading
corrections (not over 5°) as soon as the needle shows a
deviation from course, until it begins to rotate steadily toward
a wingtip position or shows erratic left/right oscillations. You
are abeam a station when the needle points 90° off your track.
Hold your last corrected heading constant and time station
passage when the needle shows either wingtip position or
settles at or near the 180° position. The time interval from
the first indications of station proximity to positive station
passage varies with altitude—a few seconds at low levels to
3 minutes at high altitude.
Homing
The ADF may be used to “home” in on a station. Homing
is flying the aircraft on any heading required to keep the
needle pointing directly to the 0° RB position. To home in
on a station, tune the station, identify the Morse code signal,
and then turn the aircraft to bring the ADF azimuth needle to
the 0° RB position. Turns should be made using the heading
indicator. When the turn is complete, check the ADF needle
and make small corrections as necessary.
Figure 9-6 illustrates homing starting from an initial MH of
050° and an RB of 310°, indicating a 50° left turn is needed
to produce an RB of zero. Turn left, rolling out at 50° minus
50° equals 360°. Small heading corrections are then made
to zero the ADF needle.
If there is no wind, the aircraft homes to the station on a direct
track over the ground. With a crosswind, the aircraft follows
a circuitous path to the station on the downwind side of the
direct track to the station.
Tracking
Tracking uses a heading that maintains the desired track
to or from the station regardless of crosswind conditions.
Interpretation of the heading indicator and needle is done to
maintain a constant MB to or from the station.
To track inbound, turn to the heading that produces a zero
RB. Maintain this heading until off-course drift is indicated
by displacement of the needle, which occurs if there is a
crosswind (needle moving left = wind from the left; needle
moving right = wind from the right). A rapid rate of bearing
change with a constant heading indicates either a strong
crosswind or close proximity to the station or both. When
there is a definite (2° to 5°) change in needle reading, turn in
the direction of needle deflection to intercept the initial MB.
The angle of interception must be greater than the number
of degrees of drift, otherwise the aircraft slowly drifts due to
the wind pushing the aircraft. If repeated often enough, the
track to the station appears circular and the distance greatly
increased as compared to a straight track. The intercept angle
depends on the rate of drift, the aircraft speed, and station
proximity. Initially, it is standard to double the RB when
turning toward your course.
For example, if your heading equals your course and the
needle points 10° left, turn 20° left, twice the initial RB.
[Figure 9-7] This is your intercept angle to capture the
RB. Hold this heading until the needle is deflected 20° in
the opposite direction. That is, the deflection of the needle
equals the interception angle (in this case 20°). The track has
been intercepted, and the aircraft remains on track as long
as the RB remains the same number of degrees as the wind
correction angle (WCA), the angle between the desired track
and the heading of the aircraft necessary to keep the aircraft
tracking over the desired track. Lead the interception to avoid
overshooting the track. Turn 10° toward the inbound course.
You are now inbound with a 10° left correction angle.
NOTE: In Figure 9-7, for the aircraft closest to the station,
the WCA is 10° left and the RB is 10° right. If those values
do not change, the aircraft tracks directly to the station. If you
observe off-course deflection in the original direction, turn
again to the original interception heading. When the desired
course has been re-intercepted, turn 5° toward the inbound
course, proceeding inbound with a 15° drift correction. If the
initial 10° drift correction is excessive, as shown by needle
deflection away from the wind, turn to parallel the desired
course and let the wind drift you back on course. When the
needle is again zeroed, turn into the wind with a reduced
drift correction angle.
9-5

| |
310°
Station
;
HDG 310°
X
f~
_
_
—
—
=
W
yy
N
i
>
2I
\
y
S
I5
I2
E
i
\
ADF
dj
-
|
320°
HDG 320°
f~
al
al
=
_
_
N
W
-
a
>
2I
\
_
E
I2
S
I5
-
-
WIND
ADF
| |
330°
HDG 330°
f~
-
=
_
_
N
A
W
y |
wa
\
f
2I
_
E
N
J
-
-
-_
=
-
I2
-
I5
S
GS
W
E
-
NAV
S
OBS
i
ss
|
ADF
_-
ss
Instrument view is from
the pilot’s perspective,
and the movable card is
f
reset after each turn
360°
HDG 360°
al
f~
—
—
=
N
a
a
W
E
I2
I5
2I
S
ADF
|
,
|
y
050°
HDG 050°
‘
f~
al
_
—
—
=
-
E
N
YA
\
I2
N
I5
Y
2I
S
W
+
ADF
Figure 9-6. ADF homing with a crosswind.
9-6

|
Station
350°
HDG 350°
f~
al
a
—
—
N
j
—
—_|
W
A
E
I2
2I
I5
S
f
\
J
-
J
-_
-
N
-—
-_
*
GS
W
E
NAV
S
OBS
ADF
__s
ss
__s
i
|
Instrument view is from
the pilot’s perspective,
340°
HDG 340°
and the movable card is
f~
-
J
_
reset after each turn
—
—
N
>
er
W
_—|
—
E
2I
I2
I5
S
ADF
|
340°
HDG 340°
f~
il
a
—
—
N
>
_|
W
—
\
——
E
2I
I2
I5
—
S
WIND
ADF
|
360°
HDG 360°
f~
al
al
_
_
N
EE
nl
—
WCA = 10° LEFT
W
E
I2
RB = 10° RIGHT
I5
2I
S
ADF
:
005°
|
005°
HDG 005°
f~
al
a
—_
—
N
—— _—_—
———
—
E
W
I2
I5
}
2I
S
ADF
Figure 9-7. ADF tracking inbound.
9-7

To track outbound, the same principles apply: needle moving
left = wind from the left, needle moving right = wind from the
right. Wind correction is made toward the needle deflection.
The only exception is while the turn to establish the WCA is
being made, the direction of the azimuth needle deflections is
reversed. When tracking inbound, needle deflection decreases
while turning to establish the WCA, and needle deflection
increases when tracking outbound. Note the example of
course interception and outbound tracking in Figure 9-8.
Intercepting Bearings
ADF orientation and tracking procedures may be applied to
intercept a specified inbound or outbound MB. To intercept
an inbound bearing of 355°, the following steps may be used.
[Figure 9-9]
1.
Determine your position in relation to the station by
paralleling the desired inbound bearing. In this case,
turn to a heading of 355°. Note that the station is to
the right front of the aircraft.
2.
Determine the number of degrees of needle deflection
from the nose of the aircraft. In this case, the needle’s
RB from the aircraft’s nose is 40° to the right. A rule
of thumb for interception is to double this RB amount
as an interception angle (80°).
3.
Turn the aircraft toward the desired MB the number of
degrees determined for the interception angle, which
as indicated (in two above) is twice the initial RB (40°)
or, in this case, 80°. Therefore, the right turn is 80°
from the initial MB of 355° or a turn to 075° magnetic
(355° + 80° + 075°).
4.
Maintain this interception heading of 075° until the
needle is deflected the same number of degrees “left”
from the zero position as the angle of interception 080°
(minus any lead appropriate for the rate at which the
bearing is changing).
5.
Turn left 80° and the RB (in a no wind condition and
with proper compensation for the rate of the ADF
needle movement) should be 0° or directly off the
nose. Additionally, the MB should be 355° indicating
proper interception of the desired course.
NOTE: The rate of an ADF needle movement, or any bearing
pointer for that matter, is faster as aircraft position becomes
closer to the station or waypoint (WP).
Interception of an outbound MB can be accomplished by the
same procedures as for the inbound intercept, except that
it is necessary to substitute the 180° position for the zero
position on the needle.
9-8
Operational Errors of ADF
Some of the common pilot-induced errors associated with
ADF navigation are listed below to help you avoid making
the same mistakes. The errors are:
1.
Failure to keep the heading indicator set so that it
agrees with the corrected magnetic compass reading.
Initiating an ADF approach without verifying that the
heading indicator agrees with the corrected compass
indicator reading may cause the pilot to believe that
he is on course but still impact the terrain (CFIT).
2.
Improper tuning and station identification. Many pilots
have made the mistake of homing or tracking to the
wrong station.
3.
Positively identifying any malfunctions of the RMI
slaving system or ignoring the warning flag.
4.
Dependence on homing rather than proper tracking.
This commonly results from sole reliance on the
ADF indications rather than correlating them with
heading indications.
5.
Poor orientation due to failure to follow proper steps
in orientation and tracking.
6.
Careless interception angles, very likely to happen if
you rush the initial orientation procedure.
7. Overshooting and undershooting predetermined
MBs, often due to forgetting the course interception
angles used.
8.
Failure to maintain selected headings. Any heading
change is accompanied by an ADF needle change.
The instruments must be read in combination before
any interpretation is made.
9.
Failure to understand the limitations of the ADF and
the factors that affect its use.
10. Overcontrolling track corrections close to the station
(chasing the ADF needle) due to failure to understand
or recognize station approach.
Very High Frequency Omnidirectional Range
(VOR)
VOR is the primary navigational aid (NAVAID) used by civil
aviation in the National Airspace System (NAS). The VOR
ground station is oriented to magnetic north and transmits
azimuth information to the aircraft, providing 360 courses
TO or FROM the VOR station. When DME is installed with
the VOR, it is referred to as a VOR/DME and provides both
azimuth and distance information. When military tactical air
navigation (TACAN) equipment is installed with the VOR,
it is known as a VORTAC and provides both azimuth and
distance information.

[|
350°
HDG 350°
\
an \
al
330°
a
—_
—
N
q
W
E
|
I2
——
2I
——
I5
—
S
[|
ADF
340°
HDG 340°
an \
~~
al
a
_
_
N
W
‘
-|
_
E
\
2I
I2
I5
——
S
a—
| |
\
ADF
330°
HDG 330°
.
-
an \
~ |
~ |
=
N
W
-
@
>
\
2I
_
E
I2
I5
|
S
i
[|
ADF
330°
HDG 330°
|
an \
~~
>
a
—
_
N
>
W
\
=
|
2I
-
E
I2
I5
S
|
ADF
015°
HDG 015°
z
—
|
j
—
ADF
~—_—
al
an \
—
—
=
N
E
Station
I2
W
I5
|
2I
WIND
S
015°
HDG 015°
z
—
——
j
i
.—_—
{
N
=
a
nal
J
a
J
GS
W
E
NAV
S
OBS
ADF
__s
__s
ss
ss
an \
al
—
—
P~
N
Instrument view is from
E
the pilot’s perspective,
I2
W
i
I5
and the movable card is
2I
015°
S
reset after each turn
Figure 9-8. ADF interception and tracking outbound.
9-9

f~
|
a
oY
~ |
~ |
E
I2
I5
N
360°
S
2I
Station
Magnetic North
W
075°
HDG 075°
J
al
J
J
J
N
GS
W
E
NAV
S
OBS
355°
Instrument view is from
the pilot’s perspective,
and the movable card is
reset after each turn
A
ADF
i
INBOUND
:
355°
.
>
—
75°
—
——
B
.
¥
i
—_
ti
————
—
aan
~
INTERCEPTION
—
A-1
~\
f~
al
al
-_
-_
N
180°
,
-
225°
W
E
Magnetic South
I2
2I
I5
S
355°
Figure 7-10. VOR radials.
HDG 355°
Figure 9-10. VOR radials.
:
355°
well as voice transmissions for communication and relay of
weather and other information.
ADF
VORs are classified according to their operational uses. The
standard VOR facility has a power output of approximately
Figure 9-9. Interception of bearing.
200 watts, with a maximum usable range depending upon
The courses oriented FROM the station are called radials. The
the aircraft altitude, class of facility, location of the facility,
VOR information received by an aircraft is not influenced
terrain conditions within the usable area of the facility, and
by aircraft attitude or heading. [Figure 9-10] Radials can
other factors. Above and beyond certain altitude and distance
be envisioned to be like the spokes of a wheel on which the
limits, signal interference from other VOR facilities and a
aircraft is on one specific radial at any time. For example,
weak signal make it unreliable. Coverage is typically at least
aircraft A (heading 180°) is inbound on the 360° radial; after
40 miles at normal minimum instrument flight rules (IFR)
crossing the station, the aircraft is outbound on the 180°
altitudes. VORs with accuracy problems in parts of their
radial at A1. Aircraft B is shown crossing the 225° radial.
service volume are listed in Notices to Airmen (NOTAMs)
Similarly, at any point around the station, an aircraft can be
and in the Airport/Facility Directory (A/FD) under the name
located somewhere on a specific VOR radial. Additionally,
of the NAVAID.
a VOR needle on an RMI always points to the course that
takes you to the VOR station where conversely the ADF
VOR Components
needle points to the station as a RB from the aircraft. In
The ground equipment consists of a VOR ground station,
the example above, the ADF needle at position A would be
which is a small, low building topped with a flat white disc,
pointed straight ahead, at A1 to the aircraft’s 180° position
upon which are located the VOR antennas and a fiberglass
(tail) and at B to the aircraft’s right.
cone-shaped tower. [Figure 9-11] The station includes an
automatic monitoring system. The monitor automatically
The VOR receiver measures and presents information to
turns off defective equipment and turns on the standby
indicate bearing TO or FROM the station. In addition to the
transmitter. Generally, the accuracy of the signal from the
navigation signals transmitted by the VOR, a Morse code
ground station is within 1°.
signal is transmitted concurrently to identify the facility, as
9-10

Omnibearing Selector (OBS)
The desired course is selected by turning the omnibearing
selector (OBS) knob until the course is aligned with the
course index mark or displayed in the course window.
Course Deviation Indicator (CDI)
—
|
The course deviation indicator (CDI) is composed of an
instrument face and a needle hinged to move laterally across
the instrument face. The needle centers when the aircraft is
on the selected radial or its reciprocal. Full needle deflection
from the center position to either side of the dial indicates the
aircraft is 12° or more off course, assuming normal needle
sensitivity. The outer edge of the center circle is 2° off course;
with each dot representing an additional 2°.
Figure 9-11. VOR transmitter (ground station).
Figure 7-11. VOR transmitter ground station.
TO/FROM Indicator
VOR facilities are aurally identified by Morse code, or
The TO/FROM indicator shows whether the selected course,
voice, or both. The VOR can be used for ground-to-air
if intercepted and flown, takes the aircraft TO or FROM the
communication without interference with the navigation
station. It does not indicate whether the aircraft is heading
signal. VOR facilities operate within the 108.0 to 117.95 MHz
to or from the station.
frequency band and assignment between 108.0 and 112.0
MHz is in even-tenth increments to preclude any conflict
Flags or Other Signal Strength Indicators
with ILS localizer frequency assignment, which uses the
The device that indicates a usable or an unreliable signal may
odd tenths in this range.
be an “OFF” flag. It retracts from view when signal strength
is sufficient for reliable instrument indications. Alternately,
The airborne equipment includes an antenna, a receiver, and
insufficient signal strength may be indicated by a blank or
the indicator instrument. The receiver has a frequency knob to
OFF in the TO/FROM window.
select any of the frequencies between 108.0 to 117.95 MHz.
The ON/OFF/volume control turns on the navigation receiver
The indicator instrument may also be a horizontal situation
and controls the audio volume. The volume has no effect on
indicator (HSI), which combines the heading indicator
the operation of the receiver. You should listen to the station
and CDI. [Figure 9-13] The combination of navigation
identifier before relying on the instrument for navigation.
information from VOR/Localizer (LOC) with aircraft heading
information provides a visual picture of the aircraft’s location
VOR indicator instruments have at least the essential
and direction. This decreases pilot workload especially
components shown in the instrument illustrated in Figure 9-12.
with tasks such as course intercepts, flying a back-course
approach, or holding pattern entry. (See Chapter 5, Flight
Course index
el
Pa
Instruments, for operational characteristics.) [Figure 9-14]
N
Ff»
Function of VOR
*
Unreliable signal flag
Orientation
N
TO
A
The VOR does not account for the aircraft heading. It only
V
CDI needle
relays the aircraft direction from the station and has the same
TO indicator
indications regardless of which way the nose is pointing. Tune
W
E
the VOR receiver to the appropriate frequency of the selected
FROM indicator
VOR ground station, turn up the audio volume, and identify
Approximately 2 degrees
in the VOR mode
the station’s signal audibly. Then, rotate the OBS to center
FR
the CDI needle and read the course under or over the index.
In Figure 9-12, 360° TO is the course indicated, while in
S
OBS
Figure 9-15, 180° TO is the course. The latter indicates that
the aircraft (which may be heading in any direction) is, at
OBS knob
this moment, located at any point on the 360° radial (line
from the station) except directly over the station or very
Figure 9-12. The VOR indicator instrument.
9-11

Lubber line
Compass warning flag
Heading select bug
T
-_
Course select pointer
Ss
HDG
Symbolic aircraft
_
_
NAV warning flag
O
Compass card
>
G
a
NAV
S
Glideslope pointer
a
I2
I5
2I
|
Heading select knob
Course select knob
Course deviation bar (CDI)
Course deviation scale
Figure 9-13. A typical horizontal situation indicator (HSI).
a
WPT _ _ _ _ _ _ DIS _ _ ._ NM DTK _ _ _° TRK 270°
NAV1 108.00 113.00
134.000 118.000 COM1
a
fe}
a
oO
a
NAV2 108.00 110.60
123.800 118.000 COM2
oO
(e)
a
>
Oo
oO
J
ri
Heading
—
Heading select bug
Lubber line
270°
Selected heading box
HDG 270°
CRS 270°
>
Compass card
Course select pointer
TAS 106KT
OAT 6°C
Course deviation scale
VOR 1
y
y
>
>
Course deviation indicator (CDI)
,
,
XPDR 5537 IDNT LCL10:12:34
INSET
PFD
CDI
XPDR
IDENT TMR/REF
NRST
ALERTS
Oo
oO
a
>
Figure 9-14. An HSI display as seen on the pilot’s primary flight display (PFD) on an electronic flight instrument. Note that only attributes
related to the HSI are labeled.
9-12

~~
f
>
~S
215°
-
~
S
HDG 215°
CRS 180°
r |
>
*
|
-
TO
VOR
E
TO
W
N
OBS
360°
VOR
340°
20°
330°
30°
320°
40°
310°
50°
300°
60°
290°
70°
280°
80°
—
90°
270°
260°
100°
250°
110°
240°
120°
230°
130°
220°
140°
210°
150°
200°
160°
190°
170°
180°
-
+
-
\
|
-
al
~~
330°
S
r |
HDG 330°
CRS 180°
*
*a
E
W
VOR
FROM
FR
N
OBS
VOR
ELECTRONIC FLIGHT
ANALOG SYSTEMS
INSTRUMENTS
Figure 9-15. CDI interpretation. The CDI as typically found on analog systems (right) and as found on electronic flight instruments (left).
9-13

close to it, as in Figure 9-15. The CDI deviates from side
to side as the aircraft passes over or nearly over the station
because of the volume of space above the station where the
zone of confusion exists. This zone of confusion is caused
by lack of adequate signal directly above the station due to
the radiation pattern of the station’s antenna, and because
the resultant of the opposing reference and variable signals
is small and constantly changing.
The CDI in Figure 9-15 indicates 180°, meaning that the
aircraft is on the 180° or the 360° radial of the station. The TO/
FROM indicator resolves the ambiguity. If the TO indicator is
showing, then it is 180° TO the station. The FROM indication
indicates the radial of the station the aircraft is presently on.
Movement of the CDI from center, if it occurs at a relatively
constant rate, indicates the aircraft is moving or drifting off
the 180°/360° line. If the movement is rapid or fluctuating,
this is an indication of impending station passage (the aircraft
is near the station). To determine the aircraft’s position
relative to the station, rotate the OBS until FROM appears
in the window, and then center the CDI needle. The index
indicates the VOR radial where the aircraft is located. The
inbound (to the station) course is the reciprocal of the radial.
If the VOR is set to the reciprocal of the intended course, the
CDI reflects reverse sensing. To correct for needle deflection,
turn away from the needle. To avoid this reverse sensing
situation, set the VOR to agree with the intended course.
A single NAVAID allows a pilot to determine the aircraft’s
position relative to a radial. Indications from a second
NAVAID are needed in order to narrow the aircraft’s position
down to an exact location on this radial.
Tracking TO and FROM the Station
To track to the station, rotate the OBS until TO appears,
then center the CDI. Fly the course indicated by the index.
If the CDI moves off center to the left, follow the needle by
correcting course to the left, beginning with a 20° correction.
When flying the course indicated on the index, a left deflection
of the needle indicates a crosswind component from the left.
If the amount of correction brings the needle back to center,
decrease the left course correction by half. If the CDI moves
left or right now, it should do so much more slowly, and smaller
heading corrections can be made for the next iteration.
Keeping the CDI centered takes the aircraft to the station.
To track to the station, the OBS value at the index is not
changed. To home to the station, the CDI needle is periodically
centered, and the new course under the index is used for the
aircraft heading. Homing follows a circuitous route to the
station, just as with ADF homing.
9-14
To track FROM the station on a VOR radial, you should
first orient the aircraft’s location with respect to the station
and the desired outbound track by centering the CDI needle
with a FROM indication. The track is intercepted by either
flying over the station or establishing an intercept heading.
The magnetic course of the desired radial is entered under the
index using the OBS and the intercept heading held until the
CDI centers. Then the procedure for tracking to the station
is used to fly outbound on the specified radial.
Course Interception
If the desired course is not the one being flown, first orient
the aircraft’s position with respect to the VOR station and the
course to be flown, and then establish an intercept heading.
The following steps may be used to intercept a predetermined
course, either inbound or outbound. Steps 1–3 may be omitted
when turning directly to intercept the course without initially
turning to parallel the desired course.
1.
Determine the difference between the radial to be
intercepted and the radial on which the aircraft is
located (205° – 160° = 045°).
2.
Double the difference to determine the interception
angle, which will not be less than 20° nor greater
than 90° (45° × 2 = 090°). 205° + 090° = 295° for
the intercept).
3.
Rotate the OBS to the desired radial or inbound course.
4.
Turn to the interception heading.
5.
Hold this heading constant until the CDI center, which
indicates the aircraft is on course. (With practice in
judging the varying rates of closure with the course
centerline, pilots learn to lead the turn to prevent
overshooting the course.)
6.
Turn to the MH corresponding to the selected course,
and follow tracking procedures inbound or outbound.
Course interception is illustrated in Figure 9-16.
VOR Operational Errors
Typical pilot-induced errors include:
1.
Careless tuning and identification of station.
2.
Failure to check receiver for accuracy/sensitivity.
3.
Turning in the wrong direction during an orientation.
This error is common until visualizing position rather
than heading.
4.
Failure to check the ambiguity (TO/FROM) indicator,
particularly during course reversals, resulting in reverse
sensing and corrections in the wrong direction.

-
After needle centers
.
«
track inbound on
205° radial.
025°
HDG 025°
CRS 025°
VOR1
ze
025°
Maintain heading of
,
-
~
~
A
295°
—
_
_
-
N
F
r
TO
295°
E
HDG 295°
CRS 025°
I2
W
I5
2I
S
OBS
VOR 1
al
=
=
N
~~
z
*
TO
A
/
,
E
—
2I
=
y |
=
W
_
I5
f
I2
J
-
J
-_
-
N
S
aa
=
OBS
A
GS
295°
W
E
NAV
S
OBS
-
ss
~~
=~
es
ss
_—
y
i
Z
Instrument view is from
the pilot’s perspective,
and the movable card is
NOTES
reset after each turn
J
As VOR needle
centers, lead the turn
to track inbound.
Zz
205°
-
Present position,
-
inboundon 160°
radial.
340°
HDG 340°
CRS 340°
VOR 1
+
>
|
\
-
- |
—
=
—_
—_
N
\
r
TO
W
E
oe
2I
I2
I5
S
OBS
.
160°
Figure 9-16. Course interception (VOR).
9-15

5.
Failure to parallel the desired radial on a track
interception problem. Without this step, orientation
to the desired radial can be confusing. Since pilots
think in terms of left and right of course, aligning the
aircraft position to the radial/course is essential.
6. Overshooting and undershooting radials on
interception problems.
7.
Overcontrolling corrections during tracking, especially
close to the station.
8.
Misinterpretation of station passage. On VOR
receivers not equipped with an ON/OFF flag, a
voice transmission on the combined communication
and navigation radio (NAV/COM) in use for VOR
may cause the same TO/FROM fluctuations on the
ambiguity meter as shown during station passage.
Read the whole receiver—TO/FROM, CDI, and
OBS—before you make a decision. Do not utilize a
VOR reading observed while transmitting.
9.
Chasing the CDI, resulting in homing instead of
tracking. Careless heading control and failure to
bracket wind corrections make this error common.
VOR Accuracy
The effectiveness of the VOR depends upon proper use and
adjustment of both ground and airborne equipment.
The accuracy of course alignment of the VOR is generally
plus or minus 1°. On some VORs, minor course roughness
may be observed, evidenced by course needle or brief flag
alarm. At a few stations, usually in mountainous terrain,
the pilot may occasionally observe a brief course needle
oscillation similar to the indication of “approaching station.”
Pilots flying over unfamiliar routes are cautioned to be on
the alert for these vagaries, and in particular, to use the TO/
FROM indicator to determine positive station passage.
Certain propeller revolutions per minute (rpm) settings or
helicopter rotor speeds can cause the VOR CDI to fluctuate
as much as plus or minus 6°. Slight changes to the RPM
setting normally smooths out this roughness. Pilots are urged
to check for this modulation phenomenon prior to reporting
a VOR station or aircraft equipment for unsatisfactory
operation.
VOR Receiver Accuracy Check
VOR system course sensitivity may be checked by noting
the number of degrees of change as the OBS is rotated to
move the CDI from center to the last dot on either side. The
course selected should not exceed 10° or 12° either side. In
addition, Title 14 of the Code of Federal Regulations (14
CFR) part 91 provides for certain VOR equipment accuracy
9-16
checks, and an appropriate endorsement, within 30 days prior
to flight under IFR. To comply with this requirement and to
ensure satisfactory operation of the airborne system, use the
following means for checking VOR receiver accuracy:
1.
VOR test facility (VOT) or a radiated test signal from
an appropriately rated radio repair station.
2.
Certified checkpoints on the airport surface.
3.
Certified airborne checkpoints.
VOR Test Facility (VOT)
The Federal Aviation Administration (FAA) VOT transmits
a test signal that provides users a convenient means to
determine the operational status and accuracy of a VOR
receiver while on the ground where a VOT is located.
Locations of VOTs are published in the A/FD. Two
means of identification are used: one is a series of dots
and the other is a continuous tone. Information concerning
an individual test signal can be obtained from the local
flight service station (FSS.) The airborne use of VOT is
permitted; however, its use is strictly limited to those areas/
altitudes specifically authorized in the A/FD or appropriate
supplement.
To use the VOT service, tune in the VOT frequency 108.0
MHz on the VOR receiver. With the CDI centered, the
OBS should read 0° with the TO/FROM indication showing
FROM or the OBS should read 180° with the TO/FROM
indication showing TO. Should the VOR receiver operate an
RMI, it would indicate 180° on any OBS setting.
A radiated VOT from an appropriately rated radio repair
station serves the same purpose as an FAA VOT signal, and
the check is made in much the same manner as a VOT with
some differences.
The frequency normally approved by the Federal
Communications Commission (FCC) is 108.0 MHz;
however, repair stations are not permitted to radiate the
VOR test signal continuously. The owner or operator of the
aircraft must make arrangements with the repair station to
have the test signal transmitted. A representative of the repair
station must make an entry into the aircraft logbook or other
permanent record certifying to the radial accuracy and the
date of transmission.
Certified Checkpoints
Airborne and ground checkpoints consist of certified radials
that should be received at specific points on the airport surface
or over specific landmarks while airborne in the immediate
vicinity of the airport. Locations of these checkpoints are
published in the A/FD.

Should an error in excess of ±4° be indicated through use of
a ground check, or ±6° using the airborne check, IFR flight
shall not be attempted without first correcting the source of
the error. No correction other than the correction card figures
supplied by the manufacturer should be applied in making
these VOR receiver checks.
If a dual system VOR (units independent of each other except
for the antenna) is installed in the aircraft, one system may
be checked against the other. Turn both systems to the same
VOR ground facility and note the indicated bearing to that
station. The maximum permissible variation between the two
indicated bearings is 4°.
Distance Measuring Equipment (DME)
When used in conjunction with the VOR system, DME makes
it possible for pilots to determine an accurate geographic
position of the aircraft, including the bearing and distance TO
or FROM the station. The aircraft DME transmits interrogating
radio frequency (RF) pulses, which are received by the DME
antenna at the ground facility. The signal triggers ground
receiver equipment to respond to the interrogating aircraft. The
airborne DME equipment measures the elapsed time between
the interrogation signal sent by the aircraft and reception of the
reply pulses from the ground station. This time measurement is
converted into distance in nautical miles (NM) from the station.
Some DME receivers provide a groundspeed in knots by
monitoring the rate of change of the aircraft’s position relative
to the ground station. Groundspeed values are accurate only
when tracking directly to or from the station.
DME Components
VOR/DME, VORTAC, ILS/DME, and LOC/DME
navigation facilities established by the FAA provide course
and distance information from collocated components under
a frequency pairing plan. DME operates on frequencies
in the UHF spectrum between 962 MHz and 1213 MHz.
Aircraft receiving equipment that provides for automatic
DME selection assures reception of azimuth and distance
information from a common source when designated VOR/
DME, VORTAC, ILS/DME, and LOC/DME are selected.
Some aircraft have separate VOR and DME receivers, each
of which must be tuned to the appropriate navigation facility.
The airborne equipment includes an antenna and a receiver.
The pilot-controllable features of the DME receiver include:
Channel (Frequency) Selector
Many DMEs are channeled by an associated VHF radio, or
there may be a selector switch so a pilot can select which
VHF radio is channeling the DME. For a DME with its own
frequency selector, use the frequency of the associated VOR/
DME or VORTAC station.
ON/OFF/Volume Switch
The DME identifier is heard as a Morse code identifier with
a tone somewhat higher than that of the associated VOR or
LOC. It is heard once for every three or four times the VOR
or LOC identifier is heard. If only one identifier is heard about
every 30 seconds, the DME is functional, but the associated
VOR or LOC is not.
Mode Switch
The mode switch selects between distance (DIST) or distance
in NMs, groundspeed, and time to station. There may also be
one or more HOLD functions that permit the DME to stay
channeled to the station that was selected before the switch
was placed in the hold position. This is useful when you make
an ILS approach at a facility that has no collocated DME,
but there is a VOR/DME nearby.
Altitude
Some DMEs correct for slant-range error.
Function of DME
A DME is used for determining the distance from a ground
DME transmitter. Compared to other VHF/UHF NAVAIDs,
a DME is very accurate. The distance information can be
used to determine the aircraft position or flying a track that
is a constant distance from the station. This is referred to as
a DME arc.
DME Arc
There are many instrument approach procedures (IAPs) that
incorporate DME arcs. The procedures and techniques given
here for intercepting and maintaining such arcs are applicable
to any facility that provides DME information. Such a facility
may or may not be collocated with the facility that provides
final approach guidance.
As an example of flying a DME arc, refer to Figure 9-17 and
follow these steps:
1.
Track inbound on the OKT 325° radial, frequently
checking the DME mileage readout.
2. A 0.5 NM lead is satisfactory for groundspeeds of
150 knots or less; start the turn to the arc at 10.5
miles. At higher groundspeeds, use a proportionately
greater lead.
3.
Continue the turn for approximately 90°. The roll-out
heading is 055° in a no wind condition.
4.
During the last part of the intercepting turn, monitor
the DME closely. If the arc is being overshot (more
than 1.0 NM), continue through the originally planned
roll-out heading. If the arc is being undershot, roll-out
of the turn early.
9-17

With an RMI, in a no wind condition, pilots should
theoretically be able to fly an exact circle around the facility
.
325°
by maintaining an RB of 90° or 270°. In actual practice,
a series of short legs are flown. To maintain the arc in
\
Figure 9-18, proceed as follows:
\
y
i
1.
With the RMI bearing pointer on the wingtip reference
|
wh
>
(90° or 270° position) and the aircraft at the desired
10 DME arc
—
DME range, maintain a constant heading and allow the
—
055°
bearing pointer to move 5°– 10° behind the wingtip.
~
This causes the range to increase slightly.
Lead points 10.5 NM
2.
Turn toward the facility to place the bearing pointer
5°– 10° ahead of the wingtip reference, and then
maintain heading until the bearing pointer is again
Lead points 9.5 NM
yy
behind the wingtip. Continue this procedure to
>
i
\
maintain the approximate arc.
y |
A
3.
If a crosswind causes the aircraft to drift away from
v4
the facility, turn the aircraft until the bearing pointer is
ahead of the wingtip reference. If a crosswind causes
325°
the aircraft to drift toward the facility, turn until the
bearing is behind the wingtip.
OKT VORTAC
4.
As a guide in making range corrections, change the
Figure 7-16. DME arc interception.
RB 10°– 20° for each half-mile deviation from the
Figure 9-17. DME arc interception.
desired arc. For example, in no-wind conditions, if the
The procedure for intercepting the 10 DME when outbound
aircraft is ½ to 1 mile outside the arc and the bearing
is basically the same, the lead point being 10 NM minus 0.5
pointer is on the wingtip reference, turn the aircraft
NM or 9.5 NM.
20° toward the facility to return to the arc.
When flying a DME arc with wind, it is important to keep a
Without an RMI, orientation is more difficult since there is
continuous mental picture of the aircraft’s position relative to
no direct azimuth reference. However, the procedure can be
the facility. Since the wind-drift correction angle is constantly
flown using the OBS and CDI for azimuth information and
changing throughout the arc, wind orientation is important.
the DME for arc distance.
In some cases, wind can be used in returning to the desired
track. High airspeeds require more pilot attention because of
Intercepting Lead Radials
the higher rate of deviation and correction.
A lead radial is the radial at which the turn from the arc to the
inbound course is started. When intercepting a radial from a
Maintaining the arc is simplified by keeping slightly inside
DME arc, the lead varies with arc radius and groundspeed.
the curve; thus, the arc is turning toward the aircraft and
For the average general aviation aircraft, flying arcs such
interception may be accomplished by holding a straight
as those depicted on most approach charts at speeds of 150
course. When outside the curve, the arc is “turning away”
knots or less, the lead is under 5°. There is no difference
and a greater correction is required.
between intercepting a radial from an arc and intercepting it
from a straight course.
To fly the arc using the VOR CDI, center the CDI needle upon
completion of the 90° turn to intercept the arc. The aircraft’s
With an RMI, the rate of bearing movement should be
heading is found very near the left or right side (270° or 90°
monitored closely while flying the arc. Set the course of the
reference points) of the instrument. The readings at that side
radial to be intercepted as soon as possible and determine
location on the instrument give primary heading information
the approximate lead. Upon reaching this point, start the
while on the arc. Adjust the aircraft heading to compensate
intercepting turn. Without an RMI, the technique for radial
for wind and to correct for distance to maintain the correct
interception is the same except for azimuth information,
arc distance. Recenter the CDI and note the new primary
which is available only from the OBS and CDI.
heading indicated whenever the CDI gets 2°– 4° from center.
9-18

al
|a
E
20°
S
N
W
HDG
.
|
|
i
a
11 DME arc
~
—
“ts
i
|
20°
\
,
|
q
|
q
,
10°
a
——
Desired arc
:
10 DME
eal
|a
E
al
|a
N
E
i
10°
N
S
a
W
HDG
9 DME arc
S
W
.
|
HDG
.
|
f
N
J
J
J
-_
J
_
GS
W
E
NAV
S
OBS
J
__s
St
J
>
005° Radial
Instrument view is from
the pilot’s perspective,
and the movable card is
reset after each turn
Figure 7-17. Using DME and RMI to maintain arc.
Figure 9-18. Using DME and RMI to maintain an arc.
The technique for intercepting a localizer from a DME arc
DME signals are line-of-sight; the mileage readout is the
is similar to intercepting a radial. At the depicted lead radial
straight line distance from the aircraft to the DME ground
(LR 223 or LR 212 in Figures 9-19, 9-20, and 9-21), a
facility and is commonly referred to as slant range distance.
pilot having a single VOR/LOC receiver should set it to the
Slant range refers to the distance from the aircraft’s antenna
localizer frequency. If the pilot has dual VOR/LOC receivers,
to the ground station (A line at an angle to the ground
one unit may be used to provide azimuth information and the
transmitter. GPS systems provide distance as the horizontal
other set to the localizer frequency. Since these lead radials
measurement from the WP to the aircraft. Therefore, at 3,000
provide 7° of lead, a half-standard rate turn should be used
feet and 0.5 miles the DME (slant range) would read 0.6 NM
until the LOC needle starts to move toward center.
while the GPS distance would show the actual horizontal
distance of .5 DME. This error is smallest at low altitudes and/
DME Errors
or at long ranges. It is greatest when the aircraft is closer to
the facility, at which time the DME receiver displays altitude
A DME/DME fix (a location based on two DME lines of
(in NM) above the facility. Slant range error is negligible if
position from two DME stations) provides a more accurate
the aircraft is one mile or more from the ground facility for
aircraft location than using a VOR and a DME fix.
each 1,000 feet of altitude above the elevation of the facility.
9-19

ae~~
cay
Figure 9-19. An aircraft is displayed heading southwest to intercept the localizer approach, using the 16 NM DME arc off of ORM.a
ww2
112.58
199.70
=
"
.
[135.975 - 128.050
cor
GS 120KT XTK 8.15NM ETE 08:28 ESA 3100FT
NAV1 108.00 113.00
134.000 118.000 COM1
i
oO
a
Co
a
NAV2 108.00 110.60
123.800 118.000 COM2
MAP - NAVIGATION MAP
W880
117.88
[135975
119.625
oe
oO
me |1970™
=
oO
>
a
=
(e)
oO
J
,
¥\
a
A
,
aN
:
oo
,
,
,
,
wa
sz
sz
re
oO
oO
INSET
MAP
DCLTR
nse
[SE TE
a
|
>
a
BB
-
B
ese
——————
|
fe ee
wes 104 AHN es ae
Sees
a
S E - 3 , 3 1 A U G 2 0 0 6 t o 2 8 S E P 2 0 0 6
IAP
Figure 7-18a. Localizer interception from DME arc.
9-20

ee
OTpepe
ee
a
localizer. a
ween (1 12.60)
los
fart
ere,
8,
136.975 + 126.050) corn
a
GS 120KT XTK 8.15NM ETE 08:28 ESA 3100FT
wou 12,56)
os
1K
ere!
A.
136.975 > [128.858 oon
oe
|
NAV1 108.00 113.00
134.000 118.000 COM1
uz188.06
117.95
119.625 one
a
|
wave 108.00
117.95
136.975
119.625 cue
bre
|
oO
a
Oo
a
NAV2 108.00 110.60
123.800 118.000 COM2
MAP - NAVIGATION MAP
(2
TER]
—=_)
a
ra
|
+ 2060™
sea
di
2060")
ct
—
oO
oO
-+_*
>
a
=. | ol
me
nn
en - |ee
ounce
*
reeeey
ae
¥
®
romero
|
ae
ee
=
Ee
ee
ay
one
ON
MA a
ey)
aN.)
oO
oO
>
, |
a
ca
ee,
os
ay
a
ve
Se\
atN
ES
¥
=
x
ee
a
is
a
ea ee
ute
&
=
—
boo ate
=
OT is
a
86 OT
=
&
,
,
,
,
E
aaa
ua
IC
g
aes
fo
beans
©
sz
sz
nH
opATT
pe
cl
pyle
fe]
sa
sows oo [ror cul
near
a
Ee
ars
furscue
a
oO
oO
INSET
PFD
CDI
DCLTR
SEE
T
TCU
ge
>
a
B
re a
——————
Bi
growlon 5
*Sreenee
tam
te |< todbhees
mcoe..|INGamTORT——— “ewes
Meet
terve slid oAROKSINES
Ham
Om
Figure 9-20. The same aircraft illustrated in Figure 9-19 shown on the ORM radial near TIGAE intersection turning inbound for the
Figure 7-18b. Localizer interception from DME arc.
9-21

a -
epee
oeee
er
‘oa
Bee
wn 112.68
is
at
Ea
Ea
195.75 ~ 20.050 ca
an
1 12.60
is
re
esa
135.975 <> 120.050 on
;
a
GS 120KT XTK 8.15NM ETE 08:28 ESA 3100FT
NAV1 108.00 113.00
134.000 118.000 COM1
a
vain 1860
117.95
135.975 _ 119.625 ena
sad
oO
a
Oo
a
NAV2 108.00 110.60
123.800 118.000 COM2
wz 198.08
117.95,
136.975
119.625ral
—-|
MAP - NAVIGATION MAP
(2
=.)
(2
‘
Oo
(e)
TS
*
2tie™)
ww.
* 2110""
fe “*
a
a
=
ae
run | EES)
on
ee
cs:
Th
“ta
eal
|<.
hea)
=
Ta eee"
a
a
~ | ae
Wey wou
=
a
on Te
eau
(e)
oO
J
a
FA
outa
2)
i
a
+a
-
wise
oe
GF
¥
aA
leary es
mG
EL aT
aoe
&
EL Ory ca
\ EEE
&
>
—-
=e
Src
es
’
CNG,
ie
88 0872 ws
oon
Fone acon
=
5 Ts
vera
fear seh
We
,
,
,
,
967 oma
DM ercn
‘
C
267 vrs 89
Edoter
=e
,
,
near
strpnstean
all
ac
wes
[reorrsns|
ra
a9
wes
lwursoe
cig
teenwe
ra
f
Oo
oO
ENGINE
MAP
DCLTR
SDE
a
Tak
'
a
a
ri
,
a —
KSwa |
B
—
ee
=4
Figure 9-21. Aircraft is illustrated inbound on the localizer course.
Area Navigation (RNAV)
input from more than one RNAV source, thereby providing
a very accurate and reliable navigation source.
Area navigation (RNAV) equipment includes VOR/DME,
LORAN, GPS, and inertial navigation systems (INS). RNAV
VOR/DME RNAV
equipment is capable of computing the aircraft position,
actual track, groundspeed, and then presenting meaningful
VOR RNAV is based on information generated by the present
information to the pilot. This information may be in the form
VORTAC or VOR/DME system to create a WP using an
of distance, cross-track error, and time estimates relative to
airborne computer. As shown in Figure 9-22, the value of
Figure 7-18c. Localizer interception from DME arc.
the selected track or WP. In addition, the RNAV equipment
side A is the measured DME distance to the VOR/DME. Side
installations must be approved for use under IFR. The Pilot’s
B, the distance from the VOR/DME to the WP, and angle 1
Operating Handbook/Airplane Flight Manual (POH/AFM)
(VOR radial or the bearing from the VORTAC to the WP)
should always be consulted to determine what equipment is
are values set in the flight deck control. The bearing from
installed, the operations that are approved, and the details of
the VOR/DME to the aircraft, angle 2, is measured by the
equipment use. Some aircraft may have equipment that allows
VOR receiver. The airborne computer continuously compares
9-22

2.
MODE select switch used to select VOR/DME
NX,
mode, with:
Waypoint
a. Angular course width deviation (standard VOR
operation); or
_
B
b. Linear cross-track deviation as standard (±5 NM
full scale CDI).
C
3.
RNAV mode, with direct to WP with linear cross-track
ANGLE 1
deviation of ±5 NM.
~*~
308°
4.
RNAV/APPR (approach mode) with linear deviation
_—
VOR/DME
A
of ±1.25 NM as full scale CDI deflection.
N
G
L
E
a
248°
5.
WP select control. Some units allow the storage of more
ANGLE 2
_—
A
than one WP; this control allows selection of any WP
a
;
_
__
in storage.
6.
Data input controls. These controls allow user input
}
of WP number or ident, VOR or LOC frequency, WP
radial and distance.
Figure 9-22. RNAV computation.
Figure 7-19. RNAV computation.
While DME groundspeed readout is accurate only when
angles 1 and 2 and determines angle 3 and side C, which is
tracking directly to or from the station in VOR/DME mode,
the distance in NMs and magnetic course from the aircraft
in RNAV mode the DME groundspeed readout is accurate
to the WP. This is presented as guidance information on the
on any track.
flight deck display.
Function of VOR/DME RNAV
VOR/DME RNAV Components
The advantages of the VOR/DME RNAV system stem from
the ability of the airborne computer to locate a WP wherever it
Although RNAV flight deck instrument displays vary among
is convenient, as long as the aircraft is within reception range
manufacturers, most are connected to the aircraft CDI with a
of both nearby VOR and DME facilities. A series of these
switch or knob to select VOR or RNAV guidance. There is
WPs make up an RNAV route. In addition to the published
usually a light or indicator to inform the pilot whether VOR
routes, a random RNAV route may be flown under IFR if
or RNAV is selected. [Figure 9-23] The display includes the
it is approved by air traffic control (ATC). RNAV DPs and
WP, frequency, mode in use, WP radial and distance, DME
standard terminal arrival routes (STARs) are contained in
distance, groundspeed, and time to station.
the DP and STAR booklets.
WEE 3s
25s | \ Heal a
eS
VOR/DME RNAV approach procedure charts are also
available. Note in the VOR/DME RNAV chart excerpt shown
KICT
ea
amt
232° ogaaas Meet
in Figure 9-24 that the WP identification boxes contain the
foal
~
following information: WP name, coordinates, frequency,
; tod
identifier, radial distance (facility to WP), and reference facility
elevation. The initial approach fix (IAF), final approach fix
Figure 9-23. Onboard RNAV receivers have changed significantly.
(FAF), and missed approach point (MAP) are labeled.
Originally, RNAV receivers typically computed combined data
from VOR, VORTAC, and/or DME. That is generally not the case
To fly a route or to execute an approach under IFR, the RNAV
now. Today, GPS such as the GNC 300 and the Bendix King KLS
equipment installed in the aircraft must be approved for the
88 LORAN receivers compute waypoints based upon embedded
appropriate IFR operations.
databases and aircraft positional information.
In vertical navigation (VNAV) mode, vertical guidance is
Most VOR/DME RNAV systems have the following
provided, as well as horizontal guidance in some installations.
airborne controls:
A WP is selected at a point where the descent begins,
1.
OFF/ON/Volume control to select the frequency of the
and another WP is selected where the descent ends. The
VOR/DME station to be used.
9-23

E C - 1 ,
16 DEC 2010 to 13 JAN 2011
Figure 9-24. VOR/DME RNAV RWY 25 approach (excerpt).
Figure 7-21. VOR/DME RNAV Rwy 25 approach (excerpt).
RNAV equipment computes the rate of descent relative to
the groundspeed; on some installations, it displays vertical
guidance information on the GS indicator. When using this
type of equipment during an instrument approach, the pilot
must keep in mind that the vertical guidance information
provided is not part of the nonprecision approach. Published
nonprecision approach altitudes must be observed and
complied with, unless otherwise directed by ATC.
To fly to a WP using RNAV, observe the following procedure
[Figure 9-25]:
1.
Select the VOR/DME frequency.
2.
Select the RNAV mode.
3.
Select the radial of the VOR that passes through the
WP (225°).
4.
Select the distance from the DME to the WP (12 NM).
5.
Check and confirm all inputs, and center the CDI needle
with the TO indicator showing.
6.
Maneuver the aircraft to fly the indicated heading plus or
minus wind correction to keep the CDI needle centered.
7.
The CDI needle indicates distance off course of 1 NM
per dot; the DME readout indicates distance in NM
from the WP; the groundspeed reads closing speed
(knots) to the WP; and the time to station (TTS) reads
time to the WP.
VOR/DME RNAV Errors
The limitation of this system is the reception volume.
Published approaches have been tested to ensure this is not
9-24
16 DEC 2010 to 13 JAN 2011
E C - 1 ,
J
y
~\
a
S
7 *|
W
TO
J
yo
_
E
>
N
y
OBS
12 NM
, 4
225°
Waypoint
~
135°
a
E
S
TO
fo
N
-
_
J
GS
W
E
NAV
S
OBS
J
>»
-
N
W
—_
—_
|
I
I2
OBS
I5
Instrument view is
2I
from the pilot’s
perspective, and
the movable card is
reset after each turn
Figure 9-25. Aircraft/DME/waypoint relationship.
a problem. Descents/approaches to airports distant from the
VOR/DME facility may not be possible because, during
the approach, the aircraft may descend below the reception
altitude of the facility at that distance.
Advanced Technologies
Global Navigation Satellite System (GNSS)
The Global Navigation Satellite System (GNSS) is a
constellation of satellites providing a high-frequency signal
that contains time and distance that is picked up by a receiver

thereby. [Figure 9-26] The receiver that picks up multiple
signals from different satellites is able to triangulate its
position from these satellites.
=
i)
_—
as
ob
‘om |
Figure 9-26. A typical example (GNS 480) of a stand-alone GPS
receiver and display.
Three GNSSs exist today: the GPS, a United States system; the
Russian GNSS (GLONASS); and Galileo, a European system.
1.
GLONASS is a network of 24 satellites that can be
picked up by any GLONASS receiver, allowing the
user to pinpoint their position.
2.
Galileo planned to be a network of 30 satellites that
continuously transmit high-frequency radio signals
containing time and distance data that can be picked
up by a Galileo receiver with operational expectancy
by 2013.
3.
The GPS came on line in 1992 with 24 satellites and
today utilizes 30 satellites.
Global Positioning System (GPS)
The GPS is a satellite-based radio navigation system that
broadcasts a signal that is used by receivers to determine
precise position anywhere in the world. The receiver tracks
multiple satellites and determines a measurement that is then
used to determine the user location. [Figure 9-27]
The Department of Defense (DOD) developed and deployed
GPS as a space-based positioning, velocity, and time system.
The DOD is responsible for operation of the GPS satellite
constellation, and constantly monitors the satellites to ensure
proper operation. The GPS system permits Earth-centered
coordinates to be determined and provides aircraft position
referenced to the DOD World Geodetic System of 1984
(WGS-84). Satellite navigation systems are unaffected
by weather and provide global navigation coverage that
fully meets the civil requirements for use as the primary
means of navigation in oceanic airspace and certain remote
areas. Properly certified GPS equipment may be used as a
supplemental means of IFR navigation for domestic en route,
terminal operations and certain IAPs. Navigational values,
Figure 9-27. Typical GPS satellite array.
such as distance and bearing to a WP and groundspeed, are
computed from the aircraft’s current position (latitude and
longitude) and the location of the next WP. Course guidance
is provided as a linear deviation from the desired track of a
Great Circle route between defined WPs.
GPS may not be approved for IFR use in other countries.
Prior to its use, pilots should ensure that GPS is authorized
by the appropriate countries.
GPS Components
GPS consists of three distinct functional elements: space,
control, and user.
The space element consists of over 30 Navstar satellites. This
group of satellites is called a constellation. The space element
consists of 24 Navigation System using Timing and Ranging
(NAVSTAR) satellites in 6 orbital planes. The satellites in
each plane are spaced 60° apart for complete coverage and
are located (nominally) at about 11,000 miles above the
Earth. The planes are arranged so that there are always five
satellites in view at any time on the Earth. Presently, there are
at least 31 Block II/IIA/IIR and IIR-M satellites in orbit with
the additional satellites representing replacement satellites
(upgraded systems) and spares. Recently, the Air Force
received funding for procurement of 31 Block IIF satellites.
The GPS constellation broadcasts a pseudo-random code
timing signal and data message that the aircraft equipment
processes to obtain satellite position and status data. By
knowing the precise location of each satellite and precisely
matching timing with the atomic clocks on the satellites, the
9-25

aircraft receiver/processor can accurately measure the time
each signal takes to arrive at the receiver and, therefore,
determine aircraft position.
The control element consists of a network of ground-based
GPS monitoring and control stations that ensure the accuracy
of satellite positions and their clocks. In its present form, it
has five monitoring stations, three ground antennas, and a
master control station.
The user element consists of antennas and receiver/processors
on board the aircraft that provide positioning, velocity,
and precise timing to the user. GPS equipment used while
operating under IFR must meet the standards set forth in
Technical Standard Order (TSO) C-129 (or equivalent); meet
the airworthiness installation requirements; be “approved” for
that type of IFR operation; and be operated in accordance with
the applicable POH/AFM or flight manual supplement.
An updatable GPS database that supports the appropriate
operations (e.g., en route, terminal, and instrument
approaches) is required when operating under IFR. The
aircraft GPS navigation database contains WPs from the
geographic areas where GPS navigation has been approved
for IFR operations. The pilot selects the desired WPs from
the database and may add user-defined WPs for the flight.
Equipment approved in accordance with TSO C-115a, visual
flight rules (VFR), and hand-held GPS systems do not meet
the requirements of TSO C-129 and are not authorized for
IFR navigation, instrument approaches, or as a principal
instrument flight reference. During IFR operations, these
units (TSO C-115a) may be considered only an aid to
situational awareness.
Prior to GPS/WAAS IFR operation, the pilot must review
appropriate NOTAMs and aeronautical information. This
information is available on request from an flight service
station (FSS). The FAA does provide NOTAMs to advise
pilots of the status of the WAAS and level of service
available.
Function of GPS
GPS operation is based on the concept of ranging and
triangulation from a group of satellites in space that act
as precise reference points. The receiver uses data from a
minimum of four satellites above the mask angle (the lowest
angle above the horizon at which it can use a satellite).
The aircraft GPS receiver measures distance from a satellite
using the travel time of a radio signal. Each satellite transmits
a specific code, called a course/acquisition (CA) code, which
contains information about satellite position, the GPS system
9-26
time, and the health and accuracy of the transmitted data.
Knowing the speed at which the signal traveled (approximately
186,000 miles per second) and the exact broadcast time,
the distance traveled by the signal can be computed from
the arrival time. The distance derived from this method of
computing distance is called a pseudo-range because it is not
a direct measurement of distance, but a measurement based
on time. In addition to knowing the distance to a satellite, a
receiver needs to know the satellite’s exact position in space,
its ephemeris. Each satellite transmits information about its
exact orbital location. The GPS receiver uses this information
to establish the precise position of the satellite.
Using the calculated pseudo-range and position information
supplied by the satellite, the GPS receiver/processor
mathematically determines its position by triangulation
from several satellites. The GPS receiver needs at least four
satellites to yield a three-dimensional position (latitude,
longitude, and altitude) and time solution. The GPS receiver
computes navigational values (distance and bearing to
a WP, groundspeed, etc.) by using the aircraft’s known
latitude/longitude and referencing these to a database built
into the receiver.
The GPS receiver verifies the integrity (usability) of the
signals received from the GPS constellation through receiver
autonomous integrity monitoring (RAIM) to determine if a
satellite is providing corrupted information. RAIM needs
a minimum of five satellites in view or four satellites and
a barometric altimeter baro-aiding to detect an integrity
anomaly. For receivers capable of doing so, RAIM needs
six satellites in view (or five satellites with baro-aiding)
to isolate a corrupt satellite signal and remove it from the
navigation solution.
Generally, there are two types of RAIM messages. One
type indicates that there are not enough satellites available
to provide RAIM and another type indicates that the RAIM
has detected a potential error that exceeds the limit for the
current phase of flight. Without RAIM capability, the pilot
has no assurance of the accuracy of the GPS position.
Aircraft using GPS navigation equipment under IFR for
domestic en route, terminal operations, and certain IAPs,
must be equipped with an approved and operational alternate
means of navigation appropriate to the flight. The avionics
necessary to receive all of the ground-based facilities
appropriate for the route to the destination airport and any
required alternate airport must be installed and operational.
Ground-based facilities necessary for these routes must also
be operational. Active monitoring of alternative navigation
equipment is not required if the GPS receiver uses RAIM for
integrity monitoring. Active monitoring of an alternate means

of navigation is required when the RAIM capability of the
GPS equipment is lost. In situations where the loss of RAIM
capability is predicted to occur, the flight must rely on other
approved equipment, delay departure, or cancel the flight.
GPS Substitution
IFR En Route and Terminal Operations
GPS systems, certified for IFR en route and terminal
operations, may be used as a substitute for ADF and DME
receivers when conducting the following operations within
the United States NAS.
1. Determining the aircraft position over a DME fix.
This includes en route operations at and above 24,000
feet mean sea level (MSL) (FL 240) when using GPS
for navigation.
2.
Flying a DME arc.
3.
Navigating TO/FROM an NDB/compass locator.
4.
Determining the aircraft position over an NDB/
compass locator.
5.
Determining the aircraft position over a fix defined
by an NDB/compass locator bearing crossing a VOR/
LOC course.
6.
Holding over an NDB/compass locator.
GPS Substitution for ADF or DME
Using GPS as a substitute for ADF or DME is subject to the
following restrictions:
1.
This equipment must be installed in accordance with
appropriate airworthiness installation requirements and
operated within the provisions of the applicable POH/
AFM or supplement.
2.
The required integrity for these operations must be
provided by at least en route RAIM or equivalent.
3.
WPs, fixes, intersections, and facility locations to be
used for these operations must be retrieved from the
GPS airborne database. The database must be current.
If the required positions cannot be retrieved from the
airborne database, the substitution of GPS for ADF and/
or DME is not authorized
4.
Procedures must be established for use when RAIM
outages are predicted or occur. This may require the
flight to rely on other approved equipment or require
the aircraft to be equipped with operational NDB and/or
DME receivers. Otherwise, the flight must be rerouted,
delayed, canceled, or conducted under VFR.
5.
The CDI must be set to terminal sensitivity (1
NM) when tracking GPS course guidance in the
terminal area.
6.
A non-GPS approach procedure must exist at the
alternate airport when one is required. If the non-GPS
approaches on which the pilot must rely require DME
or ADF, the aircraft must be equipped with DME or
ADF avionics as appropriate.
7.
Charted requirements for ADF and/or DME can be met
using the GPS system, except for use as the principal
instrument approach navigation source.
NOTE: The following provides guidance that is not specific
to any particular aircraft GPS system. For specific system
guidance, refer to the POH/AFM, or supplement, or contact
the system manufacturer.
To Determine Aircraft Position Over a DME Fix:
1.
Verify aircraft GPS system integrity monitoring is
functioning properly and indicates satisfactory integrity.
2.
If the fix is identified by a five-letter name that is
contained in the GPS airborne database, select either
the named fix as the active GPS WP or the facility
establishing the DME fix as the active GPS WP. When
using a facility as the active WP, the only acceptable
facility is the DME facility that is charted as the one
used to establish the DME fix. If this facility is not in
the airborne database, it is not authorized for use.
3.
If the fix is identified by a five-letter name that is not
contained in the GPS airborne database, or if the fix
is not named, select the facility establishing the DME
fix or another named DME fix as the active GPS WP.
4.
When selecting the named fix as the active GPS WP,
a pilot is over the fix when the GPS system indicates
the active WP.
5.
If selecting the DME providing facility as the active
GPS WP, a pilot is over the fix when the GPS distance
from the active WP equals the charted DME value, and
the aircraft is established on the appropriate bearing
or course.
To Fly a DME Arc:
1.
Verify aircraft GPS system integrity monitoring is
functioning properly and indicates satisfactory integrity.
2.
Select from the airborne database the facility providing
the DME arc as the active GPS WP. The only
acceptable facility is the DME facility on which the arc
is based. If this facility is not in your airborne database,
you are not authorized to perform this operation.
3.
Maintain position on the arc by reference to the GPS
distance instead of a DME readout.
9-27

To Navigate TO or FROM an NDB/Compass
Locator:
1.
Verify aircraft GPS system integrity monitoring is
functioning properly and indicates satisfactory integrity.
2.
Select the NDB/compass locator facility from the
airborne database as the active WP. If the chart depicts
the compass locator collocated with a fix of the same
name, use of that fix as the active WP in place of the
compass locator facility is authorized.
3.
Select and navigate on the appropriate course to or
from the active WP.
To Determine Aircraft Position Over an NDB/
Compass Locator:
1.
Verify aircraft GPS system integrity monitoring is
functioning properly and indicates satisfactory integrity.
2.
Select the NDB/compass locator facility from the
airborne database. When using an NDB/compass
locator, the facility must be charted and be in the
airborne database. If the facility is not in the airborne
database, pilots are not authorized to use a facility WP
for this operation.
3.
A pilot is over the NDB/compass locator when the
GPS system indicates arrival at the active WP.
To Determine Aircraft Position Over a Fix Made up
of an NDB/Compass Locator Bearing Crossing a
VOR/LOC Course:
1.
Verify aircraft GPS system integrity monitoring is
functioning properly and indicates satisfactory integrity.
2.
A fix made up by a crossing NDB/compass locator
bearing is identified by a five-letter fix name. Pilots
may select either the named fix or the NDB/compass
locator facility providing the crossing bearing to
establish the fix as the active GPS WP. When using
an NDB/compass locator, that facility must be charted
and be in the airborne database. If the facility is not
in the airborne database, pilots are not authorized to
use a facility WP for this operation.
3.
When selecting the named fix as the active GPS WP,
pilot is over the fix when the GPS system indicates
the pilot is at the WP.
4.
When selecting the NDB/compass locator facility
as the active GPS WP, pilots are over the fix when
the GPS bearing to the active WP is the same as
the charted NDB/compass locator bearing for the
fix flying the prescribed track from the non-GPS
navigation source.
9-28
To Hold Over an NDB/Compass Locator:
1.
Verify aircraft GPS system integrity monitoring is
functioning properly and indicates satisfactory integrity.
2.
Select the NDB/compass locator facility from the
airborne database as the active WP. When using a
facility as the active WP, the only acceptable facility
is the NDB/compass locator facility which is charted.
If this facility is not in the airborne database, its use
is not authorized.
3.
Select nonsequencing (e.g., “HOLD” or “OBS”) mode
and the appropriate course in accordance with the
POH/AFM or supplement.
4.
Hold using the GPS system in accordance with the
POH/AFM or supplement.
IFR Flight Using GPS
Preflight preparations should ensure that the GPS is properly
installed and certified with a current database for the type
of operation. The GPS operation must be conducted in
accordance with the FAA-approved POH/AFM or flight
manual supplement. Flightcrew members must be thoroughly
familiar with the particular GPS equipment installed in the
aircraft, the receiver operation manual, and the POH/AFM
or flight manual supplement. Unlike ILS and VOR, the
basic operation, receiver presentation to the pilot and some
capabilities of the equipment can vary greatly. Due to these
differences, operation of different brands or even models
of the same brand of GPS receiver under IFR should not be
attempted without thorough study of the operation of that
particular receiver and installation. Using the equipment in
flight under VFR conditions prior to attempting IFR operation
allows for further familiarization.
Required preflight preparations should include checking
NOTAMs relating to the IFR flight when using GPS as a
supplemental method of navigation. GPS satellite outages
are issued as GPS NOTAMs both domestically and
internationally. Pilots may obtain GPS RAIM availability
information for an airport by specifically requesting GPS
aeronautical information from an FSS during preflight
briefings. GPS RAIM aeronautical information can be
obtained for a 3-hour period: the estimated time of arrival
(ETA), and 1 hour before to 1 hour after the ETA hour, or
a 24-hour time frame for a specific airport. FAA briefers
provide RAIM information for a period of 1 hour before to 1
hour after the ETA, unless a specific timeframe is requested
by the pilot. If flying a published GPS departure, the pilot
should also request a RAIM prediction for the departure
airport. Some GPS receivers have the capability to predict
RAIM availability. The pilot should also ensure that the

required underlying ground-based navigation facilities and
related aircraft equipment appropriate to the route of flight,
terminal operations, instrument approaches for the destination,
and alternate airports/heliports are operational for the ETA.
If the required ground-based facilities and equipment are
not available, the flight should be rerouted, rescheduled,
canceled, or conducted under VFR.
Except for programming and retrieving information from
the GPS receiver, planning the flight is accomplished in a
similar manner to conventional NAVAIDs. Departure WP,
DP, route, STAR, desired approach, IAF, and destination
airport are entered into the GPS receiver according to the
manufacturer’s instructions. During preflight, additional
information may be entered for functions such as ETA, fuel
planning, winds aloft, etc.
When the GPS receiver is turned on, it begins an internal
process of test and initialization. When the receiver is
initialized, the user develops the route by selecting a WP
or series of WPs, verifies the data, and selects the active
flight plan. This procedure varies widely among receivers
made by different manufacturers. GPS is a complex system,
offering little standardization between receiver models. It is
the pilot’s responsibility to be familiar with the operation of
the equipment in the aircraft.
The GPS receiver provides navigational values such as track,
bearing, groundspeed, and distance. These are computed from
=
|
-
16 DEC 2010 to 13 JAN 2011
aif
Ral
Figure 9-28. A GPS stand-alone approach.
the aircraft’s present latitude and longitude to the location of
the next WP. Course guidance is provided between WPs. The
pilot has the advantage of knowing the aircraft’s actual track
over the ground. As long as track and bearing to the WP are
matched up (by selecting the correct aircraft heading), the
aircraft is going directly to the WP.
GPS Instrument Approaches
There is a mixture of GPS overlay approaches (approaches
with “or GPS” in the title) and GPS stand-alone approaches
in the United States.
NOTE: GPS instrument approach operations outside the United
States must be authorized by the appropriate country authority.
While conducting these IAPs, ground-based NAVAIDs are
not required to be operational and associated aircraft avionics
need not be installed, operational, turned on, or monitored;
however, monitoring backup navigation systems is always
recommended when available.
Pilots should have a basic understanding of GPS approach
procedures and practice GPS IAPs under visual meteorological
conditions (VMC) until thoroughly proficient with all
aspects of their equipment (receiver and installation) prior
to attempting flight in instrument meteorological conditions
(IMC). [Figure 9-28]
Figure 7-26. GPS approach.
SE-3, 16 DEC 2010 to 13 JAN 2011
9-29

All IAPs must be retrievable from the current GPS database
supplied by the manufacturer or other FAA-approved
source. Flying point to point on the approach does not
assure compliance with the published approach procedure.
The proper RAIM sensitivity is not available and the CDI
sensitivity does not automatically change to 0.3 NM. Manually
setting CDI sensitivity does not automatically change
the RAIM sensitivity on some receivers. Some existing
nonprecision approach procedures cannot be coded for use
with GPS and are not available as overlays.
GPS approaches are requested and approved by ATC using
the GPS title, such as “GPS RWY 24” or “RNAV RWY 35.”
Using the manufacturer’s recommended procedures, the
desired approach and the appropriate IAF are selected from
the GPS receiver database. Pilots should fly the full approach
from an initial approach waypoint (IAWP) or feeder fix unless
specifically cleared otherwise. Randomly joining an approach
at an intermediate fix does not ensure terrain clearance.
When an approach has been loaded in the flight plan, GPS
receivers give an “arm” annunciation 30 NM straight
line distance from the airport/heliport reference point.
The approach mode should be “armed” when within 30
NM distance so the receiver changes from en route CDI
(±5 NM) and RAIM (±2 NM) sensitivity to ±1 NM terminal
sensitivity. Where the IAWP is within 30 NM, a CDI
sensitivity change occurs once the approach mode is armed
and the aircraft is within 30 NM. Where the IAWP is beyond
the 30 NM point, CDI sensitivity does not change until the
aircraft is within 30 NM even if the approach is armed earlier.
Feeder route obstacle clearance is predicated on the receiver
CDI and RAIM being in terminal CDI sensitivity within 30 NM
of the airport/heliport reference point; therefore, the receiver
should always be armed no later than the 30 NM annunciation.
Pilots should pay particular attention to the exact operation of
their GPS receivers for performing holding patterns and in the
case of overlay approaches, operations such as procedure turns.
These procedures may require manual intervention by the pilot
to stop the sequencing of WPs by the receiver and to resume
automatic GPS navigation sequencing once the maneuver
is complete. The same WP may appear in the route of flight
more than once and consecutively (e.g., IAWP, final approach
waypoint (FAWP), missed approach waypoint (MAWP) on a
procedure turn). Care must be exercised to ensure the receiver
is sequenced to the appropriate WP for the segment of the
procedure being flown, especially if one or more fly-over WPs
are skipped (e.g., FAWP rather than IAWP if the procedure
turn is not flown). The pilot may need to sequence past one or
more fly-overs of the same WP in order to start GPS automatic
sequencing at the proper place in the sequence of WPs.
9-30
When receiving vectors to final, most receiver operating
manuals suggest placing the receiver in the nonsequencing
mode on the FAWP and manually setting the course. This
provides an extended final approach course in cases where
the aircraft is vectored onto the final approach course outside
of any existing segment that is aligned with the runway.
Assigned altitudes must be maintained until established on a
published segment of the approach. Required altitudes at WPs
outside the FAWP or step-down fixes must be considered.
Calculating the distance to the FAWP may be required in
order to descend at the proper location.
When within 2 NM of the FAWP with the approach mode
armed, the approach mode switches to active, which results
in RAIM and CDI sensitivity changing to the approach
mode. Beginning 2 NM prior to the FAWP, the full scale
CDI sensitivity changes smoothly from ±1 NM to ±0.3 NM
at the FAWP. As sensitivity changes from ±1 NM to ±0.3
NM approaching the FAWP, and the CDI not centered,
the corresponding increase in CDI displacement may give
the impression the aircraft is moving further away from
the intended course even though it is on an acceptable
intercept heading. If digital track displacement information
(cross-track error) is available in the approach mode, it may
help the pilot remain position oriented in this situation.
Being established on the final approach course prior to the
beginning of the sensitivity change at 2 NM helps prevent
problems in interpreting the CDI display during ramp-down.
Requesting or accepting vectors, which causes the aircraft
to intercept the final approach course within 2 NM of the
FAWP, is not recommended.
Incorrect inputs into the GPS receiver are especially critical
during approaches. In some cases, an incorrect entry can
cause the receiver to leave the approach mode. Overriding an
automatically selected sensitivity during an approach cancels
the approach mode annunciation. If the approach mode is
not armed by 2 NM prior to the FAWP, the approach mode
does not become active at 2 NM prior to the FAWP and
the equipment will flag. In these conditions, the RAIM and
CDI sensitivity do not ramp down, and the pilot should not
descend to minimum descent altitude (MDA) but fly to the
MAWP and execute a missed approach. The approach active
annunciator and/or the receiver should be checked to ensure
the approach mode is active prior to the FAWP.
A GPS missed approach requires pilot action to sequence the
receiver past the MAWP to the missed approach portion of
the procedure. The pilot must be thoroughly familiar with the
activation procedure for the particular GPS receiver installed
in the aircraft and must initiate appropriate action after the
MAWP. Activating the missed approach prior to the MAWP

causes CDI sensitivity to change immediately to terminal
(±1 NM) sensitivity, and the receiver continues to navigate
to the MAWP. The receiver does not sequence past the
MAWP. Turns should not begin prior to the MAWP. If the
missed approach is not activated, the GPS receiver displays
an extension of the inbound final approach course and the
along track distance (ATD) increases from the MAWP until
it is manually sequenced after crossing the MAWP.
Missed approach routings in which the first track is via a course
rather than direct to the next WP require additional action
by the pilot to set the course. Being familiar with all of the
required inputs is especially critical during this phase of flight.
Departures and Instrument Departure Procedures
(DPs)
The GPS receiver must be set to terminal (±1 NM) CDI
sensitivity and the navigation routes contained in the database
in order to fly published IFR charted departures and DPs.
Terminal RAIM should be provided automatically by the
receiver. (Terminal RAIM for departure may not be available
unless the WPs are part of the active flight plan rather than
proceeding direct to the first destination.) Certain segments
of a DP may require some manual intervention by the pilot,
especially when radar vectored to a course or required to
intercept a specific course to a WP. The database may not
contain all of the transitions or departures from all runways
and some GPS receivers do not contain DPs in the database.
It is necessary that helicopter procedures be flown at 70 knots
or less since helicopter departure procedures and missed
approaches use a 20:1 obstacle clearance surface (OCS),
which is double the fixed-wing OCS. Turning areas are based
on this speed also. Missed approach routings in which the
first track is via a course rather than direct to the next WP
require additional action by the pilot to set the course. Being
familiar with all of the required inputs is especially critical
during this phase of flight.
GPS Errors
Normally, with 30 satellites in operation, the GPS
constellation is expected to be available continuously
worldwide. Whenever there are fewer than 24 operational
satellites, GPS navigational capability may not be available
at certain geographic locations. Loss of signals may also
occur in valleys surrounded by high terrain, and any time
the aircraft’s GPS antenna is “shadowed” by the aircraft’s
structure (e.g., when the aircraft is banked).
Certain receivers, transceivers, mobile radios, and portable
receivers can cause signal interference. Some VHF
transmissions may cause “harmonic interference.” Pilots
can isolate the interference by relocating nearby portable
receivers, changing frequencies, or turning off suspected
causes of the interference while monitoring the receiver’s
signal quality data page.
GPS position data can be affected by equipment characteristics
and various geometric factors, which typically cause errors
of less than 100 feet. Satellite atomic clock inaccuracies,
receiver/processors, signals reflected from hard objects
(multi-path), ionospheric and tropospheric delays, and
satellite data transmission errors may cause small position
errors or momentary loss of the GPS signal.
System Status
The status of GPS satellites is broadcast as part of the data
message transmitted by the GPS satellites. GPS status
information is also available by means of the United States
Coast Guard navigation information service: (703) 313-5907
or on the internet at www.navcen.uscg.gov. Additionally,
satellite status is available through the NOTAM system.
The GPS receiver verifies the integrity (usability) of the
signals received from the GPS constellation through RAIM
to determine if a satellite is providing corrupted information.
At least one satellite, in addition to those required for
navigation, must be in view for the receiver to perform
the RAIM function; thus, RAIM needs a minimum of five
satellites in view or four satellites and a barometric altimeter
(baro-aiding) to detect an integrity anomaly. For receivers
capable of doing so, RAIM needs six satellites in view (or
five satellites with baro-aiding) to isolate the corrupt satellite
signal and remove it from the navigation solution.
RAIM messages vary somewhat between receivers; however,
there are two most commonly used types. One type indicates
that there are not enough satellites available to provide RAIM
integrity monitoring and another type indicates that the RAIM
integrity monitor has detected a potential error that exceeds the
limit for the current phase of flight. Without RAIM capability,
the pilot has no assurance of the accuracy of the GPS position.
Selective Availability. Selective availability is a method
by which the accuracy of GPS is intentionally degraded.
This feature is designed to deny hostile use of precise GPS
positioning data. Selective availability was discontinued on
May 1, 2000, but many GPS receivers are designed to assume
that selective availability is still active. New receivers may
take advantage of the discontinuance of selective availability
based on the performance values in ICAO Annex 10 and do
not need to be designed to operate outside of that performance.
GPS Familiarization
Pilots should practice GPS approaches under VMC until
thoroughly proficient with all aspects of their equipment
9-31

(receiver and installation) prior to attempting flight by IFR in
IMC. Some of the tasks which the pilot should practice are:
1. Utilizing the RAIM prediction function;
2. Inserting a DP into the flight plan, including setting
terminal CDI sensitivity, if required, and the conditions
under which terminal RAIM is available for departure
(some receivers are not DP or STAR capable);
3. Programming the destination airport;
4. Programming and flying the overlay approaches
(especially procedure turns and arcs);
5. Changing to another approach after selecting
an approach;
6. Programming and flying “direct” missed approaches;
7. Programming and flying “routed” missed approaches;
8. Entering, flying, and exiting holding patterns,
particularly on overlay approaches with a second WP
in the holding pattern;
9. Programming and flying a “route” from a holding
pattern;
10. Programming and flying an approach with radar vectors
to the intermediate segment;
11. Indication of the actions required for RAIM failure
both before and after the FAWP; and
12. Programming a radial and distance from a VOR (often
used in departure instructions).
Differential Global Positioning Systems (DGPS)
Differential global positioning systems (DGPS) are designed
to improve the accuracy of GNSS by measuring changes in
variables to provide satellite positioning corrections.
Because multiple receivers receiving the same set of satellites
produce similar errors, a reference receiver placed at a known
location can compute its theoretical position accurately and
can compare that value to the measurements provided by the
navigation satellite signals. The difference in measurement
between the two signals is an error that can be corrected by
providing a reference signal correction.
As a result of this differential input accuracy of the
satellite system can be increased to meters. The Wide
Area Augmentation System (WAAS) and Local Area
Augmentation System (LAAS) are examples of differential
global positioning systems.
Wide Area Augmentation System (WAAS)
The WAAS is designed to improve the accuracy, integrity,
and availability of GPS signals. WAAS allows GPS to be
used as the aviation navigation system from takeoff through
9-32
Category I precision approaches. ICAO has defined Standards
for satellite-based augmentation systems (SBAS), and Japan
and Europe are building similar systems that are planned
to be interoperable with WAAS: EGNOS, the European
Geostationary Navigation Overlay System, and MSAS,
the Japanese Multifunctional Transport Satellite (MTSAT)
Satellite-based Augmentation System. The result will be a
worldwide seamless navigation capability similar to GPS but
with greater accuracy, availability, and integrity.
Unlike traditional ground-based navigation aids, WAAS
will cover a more extensive service area in which surveyed
wide-area ground reference stations are linked to the WAAS
network. Signals from the GPS satellites are monitored by
these stations to determine satellite clock and ephemeris
corrections. Each station in the network relays the data to a
wide-area master station where the correction information is
computed. A correction message is prepared and uplinked to
a geostationary satellite (GEO) via a ground uplink and then
broadcast on the same frequency as GPS to WAAS receivers
within the broadcast coverage area. [Figure 9-29]
In addition to providing the correction signal, WAAS
provides an additional measurement to the aircraft receiver,
improving the availability of GPS by providing, in effect,
an additional GPS satellite in view. The integrity of GPS is
improved through real-time monitoring, and the accuracy
is improved by providing differential corrections to reduce
errors. [Figure 9-30] As a result, performance improvement
is sufficient to enable approach procedures with GPS/WAAS
glidepaths. At this time the FAA has completed installation of
25 wide area ground reference systems, two master stations,
and four ground uplink stations.
General Requirements
WAAS avionics must be certified in accordance with
TSO-C145A, Airborne Navigation Sensors Using the GPS
Augmented by the WAAS; or TSO-146A for stand-alone
systems. GPS/WAAS operation must be conducted in
accordance with the FAA-approved aircraft flight manual
(AFM) and flight manual supplements. Flight manual
supplements must state the level of approach procedure that
the receiver supports.
Instrument Approach Capabilities
WAAS receivers support all basic GPS approach functions
and provide additional capabilities with the key benefit to
generate an electronic glidepath, independent of ground
equipment or barometric aiding. This eliminates several
problems, such as cold temperature effects, incorrect
altimeter setting, or lack of a local altimeter source, and
allows approach procedures to be built without the cost

above for properly equipped aircraft. [Figures 9-31 and 9-32]_
Be
Wide Area Augmentation System (WAAS)
Wide
Area
Augmentation
System
GPS
ors
GPS
Satellites
Satellites
.
as
fag,
&
Sey
Ferm
a
Ta
ei
&
ei
HC
ae ee
PRES
metic
eee
25 ™
Nae
WRG,
Wide Area Reference Station
Si
Wide Area Reference Station
EN
Sy
@
Wide Area
Augmentation
System
Si
receives GPS signal
Wide Area Reference Station
data is sent to a Wide Area
Master Station for correction
a0 sree
80 sents
The information Collected by theWide Area Reference Stations is Sent to.
theWide Area Master Stations Who Will Calculate the Correction Message
GEO Synchronous
mae
—
ts 200% Paciora) Aviation Acemimteteation. Aj) Reine Rewerveee
GEO Synchronous
Satellites
Satellites
comvelsie
&
ei
@
PY
By
a
: i
NUT].
vite
retrence Suton [ICO
Wide Area Reference Station
Sy
Si
et
3)
72d
Widereaianie
tation
[UMM Sead
@
Wide Area Master station
Wide Area Reference Station
ad
&
Si
GUS
&
Wide Area Master station uplinks corrected
GEO Synchronous Satellites sends updated
signal to GEO Synchronous Satellites
WAAS signal to aircraft equipped with WAAS
&
receivers
toAlera and Other Users In the Service Area
GUS
‘The WAAS GEO Satelites Broadcast the WAAS-Corrected Signal
Figure 7-27a. LAAS representation.
Figure 9-29. WAAS satellite representation.
Local Area Augmentation System (LAAS)
of installing ground stations at each airport. A new class
of approach procedures, which provide vertical guidance
LAAS is a ground-based augmentation system that uses a
requirements for precision approaches, has been developed
GPS-reference facility located on or in the vicinity of the
to support satellite navigation use for aviation applications.
airport being serviced. This facility has a reference receiver
These new procedures called Approach with Vertical
that measures GPS satellite pseudo-range and timing and
Guidance (APV) include approaches such as the LNAV/
retransmits the signal. Aircraft landing at LAAS-equipped
VNAV procedures presently being flown with barometric
airports are able to conduct approaches to Category I level and
vertical navigation.
9-33

WAAS Accuracy
/
GPS Accuracy
~~
You are here
-_
10 ft.
50 ft.
Figure 9-30. WAAS provides performance enhancement for GPS
Figure 7-27b. WAAS satellite representation
approach procedures through real-time monitoring.
Inertial Navigation System (INS)
Inertial Navigation System (INS) is a system that navigates
precisely without any input from outside of the aircraft. It is
fully self-contained. The INS is initialized by the pilot, who
enters into the system the exact location of the aircraft on the
ground before the flight. The INS is also programmed with
WPs along the desired route of flight.
INS Components
INS is considered a stand-alone navigation system, especially
when more than one independent unit is onboard. The
airborne equipment consists of an accelerometer to measure
acceleration—which, when integrated with time, gives
velocity—and gyros to measure direction.
Later versions of the INS, called inertial reference systems
(IRS), utilize laser gyros and more powerful computers;
therefore, the accelerometer mountings no longer need to
be kept level and aligned with true north. The computer
system can handle the added workload of dealing with the
computations necessary to correct for gravitational and
directional errors. Consequently, these newer systems are
sometimes called strap down systems, as the accelerometers
and gyros are strapped down to the airframe rather than being
mounted on a structure that stays fixed with respect to the
horizon and true north.
INS Errors
The principal error associated with INS is degradation of
position with time. INS computes position by starting with
accurate position input which is changed continuously as
accelerometers and gyros provide speed and direction inputs.
Both accelerometers and gyros are subject to very small
errors; as time passes, those errors probably accumulate.
9-34
GPS
Reference
GPS
Receiver
Reference
Receiver
i
ris
GPS reference receivers, which are serving the local area
(such as an airport) receive the GPS signal from the GPS
constellation (one or more satellites).
GPS
Reference
LAAS
Receiver
Ground
Facility
The local area augmentation system (LAAS) ground facility
receives the data from the GPS ground reference receivers.
VHF Data
Broadcast
LAAS
Ground
vay
Facility
;
ia
a oe
The corrected signal is then sent and transmitted as a VHF
signal, called a VHF data broadcast.
VHF Data
Broadcast
The broadcast signal is received by appropriately equipped
aircraft which provide the pilot with highly refined GPS
guidance.
Figure 7-28a. LAAS representation.
Figure 9-31. LAAS representation.

2.
A glideslope (GS) providing vertical (up/down)
GPS Satellites
guidance toward the runway touchdown point, usually
p=
p=
at a 3° slope.
=
=
3.
Marker beacons providing range information along
the approach path.
VHF Transmitter
4.
Approach lights assisting in the transition from
instrument to visual flight.
_
The following supplementary elements, though not specific
components of the system, may be incorporated to increase
safety and utility:
—_
LAAS Facility
1. Compass locators providing transition from en route
Reference Receiver
NAVAIDs to the ILS system and assisting in holding
procedures, tracking the localizer course, identifying
the marker beacon sites, and providing a FAF for
ADF approaches.
Figure 9-32. The LAAS system working with GPS satellites,
Figure 7-28. LAAS representation.
2.
DME collocated with the GS transmitter providing
reference receivers and radio transmitters which are located on
positive distance-to-touchdown information or DME
or in the vicinity of the airport.
associated with another nearby facility (VOR or stand-
While the best INS/IRS display errors of 0.1 to 0.4 NM after
alone), if specified in the approach procedure.
flights across the North Atlantic of 4 to 6 hours, smaller and
less expensive systems are being built that show errors of 1
ILS approaches are categorized into three different types of
to 2 NM per hour. This accuracy is more than sufficient for
approaches based on the equipment at the airport and the
a navigation system that can be combined with and updated
experience level of the pilot. Category I approaches provide
by GPS. The synergy of a navigation system consisting of an
for approach height above touchdown of not less than 200 feet.
INS/IRS unit in combination with a GPS resolves the errors
Category II approaches provide for approach to a height above
and weaknesses of both systems. GPS is accurate all the time
touchdown of not less than 100 feet. Category III approaches
it is working but may be subject to short and periodic outages.
provide lower minimums for approaches without a decision
INS is made more accurate because it is continually updated
height minimum. While pilots need only be instrument rated
and continues to function with good accuracy if the GPS has
and the aircraft be equipped with the appropriate airborne
moments of lost signal.
equipment to execute Category I approaches, Category II
and III approaches require special certification for the pilots,
Instrument Approach Systems
ground equipment, and airborne equipment.
Most navigation systems approved for en route and terminal
operations under IFR, such as VOR, NDB, and GPS, may also
ILS Components
be approved to conduct IAPs. The most common systems in
Ground Components
use in the United States are the ILS, simplified directional
The ILS uses a number of different ground facilities. These
facility (SDF), localizer-type directional aid (LDA), and
facilities may be used as a part of the ILS system, as well as
microwave landing system (MLS). These systems operate
part of another approach. For example, the compass locator
independently of other navigation systems. There are new
may be used with NDB approaches.
systems being developed, such as WAAS and LAAS. Other
systems have been developed for special use.
Localizer
The localizer (LOC) ground antenna array is located on the
Instrument Landing Systems (ILS)
extended centerline of the instrument runway of an airport,
The ILS system provides both course and altitude guidance
located at the departure end of the runway to prevent it from
to a specific runway. The ILS system is used to execute a
being a collision hazard. This unit radiates a field pattern,
precision instrument approach procedure or precision approach.
which develops a course down the centerline of the runway
[Figure 9-33] The system consists of the following components:
toward the middle markers (MMs) and outer markers
1.
A localizer providing horizontal (left/right) guidance
(OMs) and a similar course along the runway centerline in
along the extended centerline of the runway.
the opposite direction. These are called the front and back
9-35

-
[
all
=~
N
_
f
r
GS
W
E
NAV
S
,
OBS
a
=
Point of intersection
|
runway and glideslope
=a
N
extended.
r
[og
GS
W
E
£
NAV
S
OBS
(-
af
90Hz 150Hz
se
*
eal
=
N
«|
GS
W
E
=a
N
*
NAV
,
S
OBS
GS
W
E
|
NAV
oe
S
OBS
–
al
_
N
«|
GS
W
E
a
NAV
–
a
S
OBS
KNOTS
KNOTS
KNOTS
—_
KNOTS
II0
I00
I00
I40 I20
I80
I20
I30
I00
KNOTS
I20
I50
I60
I00
I60 I40 I20
Figure 7-29. Instrument landing systems.
Figure 9-33. Instrument landing systems.
courses, respectively. The localizer provides course guidance,
“fly-left” (CDI needle fully deflected to the left) and a full
transmitted at 108.1 to 111.95 MHz (odd tenths only),
“fly-right” indication (CDI needle fully deflected to the right).
throughout the descent path to the runway threshold from a
Each localizer facility is audibly identified by a three-letter
distance of 18 NM from the antenna to an altitude of 4,500
designator transmitted at frequent regular intervals. The ILS
feet above the elevation of the antenna site. [Figure 9-34]
identification is preceded by the letter “I” (two dots). For
example, the ILS localizer at Springfield, Missouri, transmits
The localizer course width is defined as the angular
the identifier ISGF. The localizer includes a voice feature on
displacement at any point along the course between a full
9-36

al
18 NM
=
10 NM
—_—
10°
a
—
10°
35 °
a
—
35°
Figure 9-34. Localizer coverage limits.
Figure 7-30. Localizer coverage limits.
its frequency for use by the associated ATC facility in issuing
Unlike the localizer, the GS transmitter radiates signals only
approach and landing instructions.
in the direction of the final approach on the front course. The
system provides no vertical guidance for approaches on the back
The localizer course is very narrow, normally 5°. This
course. The glidepath is normally 1.4° thick. At 10 NM from
results in high needle sensitivity. With this course width,
the point of touchdown, this represents a vertical distance of
a full-scale deflection shows when the aircraft is 2.5° to
approximately 1,500 feet, narrowing to a few feet at touchdown.
either side of the centerline. This sensitivity permits accurate
orientation to the landing runway. With no more than one-
Marker Beacons
quarter scale deflection maintained, the aircraft will be
Two VHF marker beacons, outer and middle, are normally
aligned with the runway.
used in the ILS system. [Figure 9-35] A third beacon, the
inner, is used where Category II operations are certified. A
Glideslope (GS)
marker beacon may also be installed to indicate the FAF on
GS describes the systems that generate, receive, and indicate
the ILS back course.
the ground facility radiation pattern. The glidepath is the
straight, sloped line the aircraft should fly in its descent from
where the GS intersects the altitude used for approaching the
Outer Marker Beacons
FAF to the runway touchdown zone. The GS equipment is
Middle Marker Beacons
housed in a building approximately 750 to 1,250 feet down
2.5°
as
as
the runway from the approach end of the runway and between
2.5°
400 and 600 feet to one side of the centerline.
´
´
The course projected by the GS equipment is essentially the
same as would be generated by a localizer operating on its
side. The GS projection angle is normally adjusted to 2.5°
to 3.5° above horizontal, so it intersects the MM at about
Figure 7-31. Localizer receiver indications and aircraft
Figure 9-35. Localizer receiver indications and aircraft displacement.
200 feet and the OM at about 1,400 feet above the runway
displacement.
elevation. At locations where standard minimum obstruction
clearance cannot be obtained with the normal maximum GS
The OM is located on the localizer front course 4–7 miles
angle, the GS equipment is displaced farther from the approach
from the airport to indicate a position at which an aircraft, at
end of the runway if the length of the runway permits; or the GS
the appropriate altitude on the localizer course, will intercept
angle may be increased up to 4°.
the glidepath. The MM is located approximately 3,500 feet
9-37

from the landing threshold on the centerline of the localizer
front course at a position where the GS centerline is about 200
feet above the touchdown zone elevation. The inner marker
(IM), where installed, is located on the front course between
the MM and the landing threshold. It indicates the point at
which an aircraft is at the decision height on the glidepath
during a Category II ILS approach. The back-course marker,
where installed, indicates the back-course FAF.
Compass Locator
Compass locators are low-powered NDBs and are received
and indicated by the ADF receiver. When used in conjunction
with an ILS front course, the compass locator facilities are
collocated with the outer and/or MM facilities. The coding
identification of the outer locator consists of the first two
letters of the three-letter identifier of the associated LOC.
For example, the outer locator at Dallas/Love Field (DAL) is
identified as “DA.” The middle locator at DAL is identified
by the last two letters “AL.”
Approach Lighting Systems (ALS)
Normal approach and letdown on the ILS is divided into two
distinct stages: the instrument approach stage using only radio
guidance, and the visual stage, when visual contact with the
ground runway environment is necessary for accuracy and
safety. The most critical period of an instrument approach,
particularly during low ceiling/visibility conditions, is the
point at which the pilot must decide whether to land or
execute a missed approach. As the runway threshold is
approached, the visual glidepath separates into individual
lights. At this point, the approach should be continued by
reference to the runway touchdown zone markers. The
approach lighting system (ALS) provides lights that will
penetrate the atmosphere far enough from touchdown to
give directional, distance, and glidepath information for safe
visual transition.
Visual identification of the ALS by the pilot must be
instantaneous, so it is important to know the type of ALS
before the approach is started. Check the instrument approach
chart and the A/FD for the particular type of lighting facilities
at the destination airport before any instrument flight. With
reduced visibility, rapid orientation to a strange runway can
be difficult, especially during a circling approach to an airport
with minimum lighting facilities or to a large terminal airport
located in the midst of distracting city and ground facility
lights. Some of the most common ALS systems are shown
in Figure 9-36.
A high-intensity flasher system, often referred to as “the
rabbit,” is installed at many large airports. The flashers consist
of a series of brilliant blue-white bursts of light flashing in
sequence along the approach lights, giving the effect of a ball
9-38
of light traveling towards the runway. Typically, “the rabbit”
makes two trips toward the runway per second.
Runway end identifier lights (REIL) are installed for rapid and
positive identification of the approach end of an instrument
runway. The system consists of a pair of synchronized
flashing lights placed laterally on each side of the runway
threshold facing the approach area.
The visual approach slope indicator (VASI) gives visual
descent guidance information during the approach to a
runway. The standard VASI consists of light bars that
project a visual glidepath, which provides safe obstruction
clearance within the approach zone. The normal GS angle
is 3°; however, the angle may be as high as 4.5° for proper
obstacle clearance. On runways served by ILS, the VASI
angle normally coincides with the electronic GS angle.
Visual left/right course guidance is obtained by alignment
with the runway lights. The standard VASI installation
consists of either 2-, 3-, 4-, 6-, 12-, or 16-light units arranged
in downwind and upwind light bars. Some airports serving
long-bodied aircraft have three-bar VASIs that provide two
visual glidepaths to the same runway. The first glidepath
encountered is the same as provided by the standard VASI.
The second glidepath is about 25 percent higher than the first
and is designed for the use of pilots of long-bodied aircraft.
The basic principle of VASI is that of color differentiation
between red and white. Each light projects a beam having
a white segment in the upper part and a red segment in the
lower part of the beam. From a position above the glidepath
the pilot sees both bars as white. Lowering the aircraft with
respect to the glidepath, the color of the upwind bars changes
from white to pink to red. When on the proper glidepath,
the landing aircraft will overshoot the downwind bars and
undershoot the upwind bars. Thus the downwind (closer)
bars are seen as white and the upwind bars as red. From
a position below the glidepath, both light bars are seen as
red. Moving up to the glidepath, the color of the downwind
bars changes from red to pink to white. When below the
glidepath, as indicated by a distinct all-red signal, a safe
obstruction clearance might not exist. A standard two-bar
VASI is illustrated in Figure 9-37.
ILS Airborne Components
Airborne equipment for the ILS system includes receivers
for the localizer, GS, marker beacons, ADF, DME, and the
respective indicator instruments.
The typical VOR receiver is also a localizer receiver with
common tuning and indicating equipment. Some receivers
have separate function selector switches, but most switch
between VOR and LOC automatically by sensing if odd

ALSF-2
ALSF-1
SSALR/MALSR
MALSF
ODALS
THRESHOLD
REIL
a
>
_
i
nT
Figure 9-36. Precision and nonprecision ALS configuration.
tenths between 108 and 111.95 MHz have been selected.
Below glidepath
On glidepath
Above glidepath
Otherwise, tuning of VOR and localizer frequencies is
-
F
-
accomplished with the same knobs and switches, and the CDI
indicates “on course” as it does on a VOR radial.
Far Bar
Far Bar
Far Bar
Though some GS receivers are tuned separately, in a typical
Near Bar
Near Bar
Near Bar
installation the GS is tuned automatically to the proper
frequency when the localizer is tuned. Each of the 40 localizer
channels in the 108.10 to 111.95 MHz band is paired with a
corresponding GS frequency.
When the localizer indicator also includes a GS needle, the
instrument is often called a cross-pointer indicator. The
Figure 7-33. Standard 2-bar VASI.
crossed horizontal (GS) and vertical (localizer) needles are
Figure 9-37. Standard two-bar VASI.
9-39

free to move through standard five-dot deflections to indicate
position on the localizer course and glidepath.
When the aircraft is on the glidepath, the needle is horizontal,
overlying the reference dots. Since the glidepath is much
narrower than the localizer course (approximately 1.4° from
full up to full down deflection), the needle is very sensitive
to displacement of the aircraft from on-path alignment. With
the proper rate of descent established upon GS interception,
very small corrections keep the aircraft aligned.
The localizer and GS warning flags disappear from view on
the indicator when sufficient voltage is received to actuate the
needles. The flags show when an unstable signal or receiver
malfunction occurs.
The OM is identified by a low-pitched tone, continuous dashes
at the rate of two per second, and a purple/blue marker beacon
light. The MM is identified by an intermediate tone, alternate
dots and dashes at the rate of 95 dot/dash combinations per
minute, and an amber marker beacon light. The IM, where
installed, is identified by a high-pitched tone, continuous dots
at the rate of six per second, and a white marker beacon light.
The back-course marker (BCM), where installed, is identified
by a high-pitched tone with two dots at a rate of 72 to 75 two-
dot combinations per minute and a white marker beacon light.
Marker beacon receiver sensitivity is selectable as high or low
on many units. The low-sensitivity position gives the sharpest
indication of position and should be used during an approach.
The high-sensitivity position provides an earlier warning that
the aircraft is approaching the marker beacon site.
ILS Function
The localizer needle indicates, by deflection, whether the
aircraft is right or left of the localizer centerline, regardless of
the position or heading of the aircraft. Rotating the OBS has
no effect on the operation of the localizer needle, although
it is useful to rotate the OBS to put the LOC inbound course
under the course index. When inbound on the front course, or
outbound on the back course, the course indication remains
directional. (See Figure 9-38, aircraft C, D, and E.)
Unless the aircraft has reverse sensing capability and it is in
use, when flying inbound on the back course or outbound on
the front course, heading corrections to on-course are made
opposite the needle deflection. This is commonly described
as “flying away from the needle.” (See Figure 9-38, aircraft A
and B.) Back course signals should not be used for an approach
unless a back course approach procedure is published for that
particular runway and the approach is authorized by ATC.
Once you have reached the localizer centerline, maintain
the inbound heading until the CDI moves off center. Drift
9-40
corrections should be small and reduced proportionately as
the course narrows. By the time you reach the OM, your drift
correction should be established accurately enough on a well-
executed approach to permit completion of the approach,
with heading corrections no greater than 2°.
The heaviest demand on pilot technique occurs during
descent from the OM to the MM, when you maintain
the localizer course, adjust pitch attitude to maintain the
proper rate of descent, and adjust power to maintain proper
airspeed. Simultaneously, the altimeter must be checked
and preparation made for visual transition to land or for a
missed approach. You can appreciate the need for accurate
instrument interpretation and aircraft control within the ILS
as a whole, when you notice the relationship between CDI
and glidepath needle indications and aircraft displacement
from the localizer and glidepath centerlines.
Deflection of the GS needle indicates the position of the
aircraft with respect to the glidepath. When the aircraft is
above the glidepath, the needle is deflected downward. When
the aircraft is below the glidepath, the needle is deflected
upward. [Figure 9-39]
ILS Errors
The ILS and its components are subject to certain errors,
which are listed below. Localizer and GS signals are subject to
the same type of bounce from hard objects as space waves.
1.
Reflection. Surface vehicles and even other aircraft
flying below 5,000 feet above ground level (AGL)
may disturb the signal for aircraft on the approach.
2.
False courses. In addition to the desired course, GS
facilities inherently produce additional courses at
higher vertical angles. The angle of the lowest of
these false courses occurs at approximately 9°– 12°.
An aircraft flying the LOC/GS course at a constant
altitude would observe gyrations of both the GS needle
and GS warning flag as the aircraft passed through the
various false courses. Getting established on one of
these false courses results in either confusion (reversed
GS needle indications) or in the need for a very high
descent rate. However, if the approach is conducted
at the altitudes specified on the appropriate approach
chart, these false courses are not encountered.
Marker Beacons
The very low power and directional antenna of the marker
beacon transmitter ensures that the signal is not received
any distance from the transmitter site. Problems with signal
reception are usually caused by the airborne receiver not
being turned on or by incorrect receiver sensitivity.

B
Localizer inbound
course is 180°
As you begin procedure turn,
course needle shows
divergence from course
C
centerline increasing.
While on the procedure turn
C
a
330°
inbound the course needle
y
\
HDG 330°
CRS 180°
df
becomes directional. Start
the turn to final approach
course when the needle
comes alive (needle moves
LOC1
_
y
away from side) and is
moving toward center.
\
.
*
C
135°
HDG 135°
CRS 180°
S
LOC1
*|
y
A
y |
i
E
W
*
2I
\
I2
I5
y |
B
N
OBS
A
-
a
~ |
~ |
S
I2
I5
A
>
2I
E
W
As you fly northbound of the
a
instrument runway (in this case
N
Localizer 18), with the radio
OBS
tuned to the Localizer
f
frequency (and identified), the
course needle is not directional.
D
D
180°
Correct left to center the course
HDG 180°
CRS 180°
needle.
Maintain course with the
—
—
needle centered.
350°
HDG 350°
CRS 180°
|
LOC1
~ |
~ |
S
2I
I5
*7
I2
W
A
E
LOC1
-|
\
ad
N
OBS
_——
—
ss
\
E
,
«4
As you fly a missed approach
—
—
S
along the back course, the
*
.
_
needle, indicating “fly left” is
FAF
180°
E
W
directional.
HDG 180°
CRS 180°
I2
In this case fly left to get on
2I
I5
course.
N
OBS
-
ss
LOC1
S
2I
I5
fs
dj
I2
*
W
E
N
OBS
f
-
-
-
=~
J
N
P~
GS
W
E
NAV
S
OBS
Es
es
a
—
ss
Instrument view is from
E
,
«
the pilot’s perspective,
and the movable card is
reset after each turn
Figure 9-38. Localizer course indications. To follow indications displayed in the aircraft, start from A and proceed through E.
9-41

Le
al
=
E
Outer Marker Beacons
*
S
TO
FR
N
NAV 1
W
OBS
Middle Marker Beacons
q
auf
te
a

a
E
*
S
TO
FR
N
NAV 1
W
OBS
Figure 9-39. A GS receiver indication and aircraft displacement. An analog system is on the left and the same indication on the Garmin
Figure 7-35. Glide-slope receiver indications and aircraft displacement.
PFD on the right.
Some marker beacon receivers, to decrease weight and cost,
2.
Disorientation during transition to the ILS due to poor
are designed without their own power supply. These units
planning and reliance on one receiver instead of on all
utilize a power source from another radio in the avionics
available airborne equipment. Use all the assistance
stack, often the ADF. In some aircraft, this requires the ADF
available; a single receiver may fail.
to be turned on in order for the marker beacon receiver to
3.
Disorientation on the localizer course, due to the first
function, yet no warning placard is required. Another source
error noted above.
of trouble may be the “HIGH/LOW/OFF” three-position
4.
Incorrect localizer interception angles. A large
switch, which both activates the receiver and selects receiver
interception angle usually results in overshooting
sensitivity. Usually, the “test” feature only tests to see if
and possible disorientation. When intercepting,
the light bulbs in the marker beacon lights are working.
if possible, turn to the localizer course heading
Therefore, in some installations, there is no functional way
immediately upon the first indication of needle
for the pilot to ascertain the marker beacon receiver is actually
movement. An ADF receiver is an excellent aid to
on except to fly over a marker beacon transmitter and see if
orient you during an ILS approach if there is a locator
a signal is received and indicated (e.g., audibly, and visually
or NDB on the inbound course.
via marker beacon lights).
5.
Chasing the CDI and glidepath needles, especially
Operational Errors
when you have not sufficiently studied the approach
before the flight.
1.
Failure to understand the fundamentals of ILS ground
equipment, particularly the differences in course
Simplified Directional Facility (SDF)
dimensions. Since the VOR receiver is used on the
The simplified directional facility (SDF) provides a final
localizer course, the assumption is sometimes made
approach course similar to the ILS localizer. The SDF course
that interception and tracking techniques are identical
may or may not be aligned with the runway and the course
when tracking localizer courses and VOR radials.
may be wider than a standard ILS localizer, resulting in less
Remember that the CDI sensing is sharper and faster
on the localizer course.
9-42


precision. Usable off-course indications are limited to 35°
either side of the course centerline. Instrument indications
in the area between 35° and 90° from the course centerline
are not controlled and should be disregarded.
The SDF must provide signals sufficient to allow satisfactory
operation of a typical aircraft installation within a sector
which extends from the center of the SDF antenna system
to distances of 18 NM covering a sector 10° either side of
centerline up to an angle 7° above the horizontal. The angle
of convergence of the final approach course and the extended
runway centerline must not exceed 30°. Pilots should note
this angle since the approach course originates at the antenna
site, and an approach continued beyond the runway threshold
would lead the aircraft to the SDF offset position rather than
along the runway centerline.
The course width of the SDF signal emitted from the
transmitter is fixed at either 6° or 12°, as necessary, to provide
maximum flyability and optimum approach course quality.
A three-letter identifier is transmitted in code on the SDF
frequency; there is no letter “I” (two dots) transmitted before
the station identifier, as there is with the LOC. For example,
the identifier for Lebanon, Missouri, SDF is LBO.
Localizer Type Directional Aid (LDA)
The localizer type directional aid (LDA) is of comparable
utility and accuracy to a localizer but is not part of a
complete ILS. The LDA course width is between 3° and 6°
and thus provides a more precise approach course than an
SDF installation. Some LDAs are equipped with a GS. The
LDA course is not aligned with the runway, but straight-in
minimums may be published where the angle between the
runway centerline and the LDA course does not exceed 30°. If
this angle exceeds 30°, only circling minimums are published.
The identifier is three letters preceded by “I” transmitted in
code on the LDA frequency. For example, the identifier for
Van Nuys, California, LDA is I-BUR.
Microwave Landing System (MLS)
The microwave landing system (MLS) provides precision
navigation guidance for exact alignment and descent of aircraft
on approach to a runway. It provides azimuth, elevation, and
distance. Both lateral and vertical guidance may be displayed
on conventional course deviation indicators or incorporated
into multipurpose flight deck displays. Range information
can be displayed by conventional DME indicators and also
incorporated into multipurpose displays. [Figure 9-40]
The system may be divided into five functions, which are
approach azimuth, back azimuth, approach elevation, range;
and data communications. The standard configuration of
MLS ground equipment includes an azimuth station to
-
|
-
|
20,000’
.
40°R
\
40 °L
—
Figure 7-36. MLS coverage volumes, 3-D representation
Figure 9-40. MLS coverage volumes, 3-D representation.
perform functions as indicated above. In addition to providing
azimuth navigation guidance, the station transmits basic data,
which consists of information associated directly with the
operation of the landing system, as well as advisory data on
the performance of the ground equipment.
Approach Azimuth Guidance
The azimuth station transmits MLS angle and data on one
of 200 channels within the frequency range of 5031 to 5091
MHz. The equipment is normally located about 1,000 feet
beyond the stop end of the runway, but there is considerable
flexibility in selecting sites. For example, for heliport
operations the azimuth transmitter can be collocated with
the elevation transmitter. The azimuth coverage extends
laterally at least 40° on either side of the runway centerline
in a standard configuration, in elevation up to an angle of 15°
and to at least 20,000 feet, and in range to at least 20 NM.
MLS requires separate airborne equipment to receive and
process the signals from what is normally installed in general
aviation aircraft today. It has data communications capability,
and can provide audible information about the condition
of the transmitting system and other pertinent data such as
weather, runway status, etc. The MLS transmits an audible
identifier consisting of four letters beginning with the letter
M, in Morse code at a rate of at least six per minute. The
MLS system monitors itself and transmits ground-to-air data
messages about the system’s operational condition. During
periods of routine or emergency maintenance, the coded
identification is missing from the transmissions. At this time
there are only a few systems installed.
9-43

Required Navigation Performance
RNP is a navigation system that provides a specified level
of accuracy defined by a lateral area of confined airspace in
which an RNP-certified aircraft operates. The continuing
growth of aviation places increasing demands on airspace
capacity and emphasizes the need for the best use of the
available airspace. These factors, along with the accuracy of
modern aviation navigation systems and the requirement for
increased operational efficiency in terms of direct routings
and track-keeping accuracy, have resulted in the concept
of required navigation performance—a statement of the
navigation performance accuracy necessary for operation
within a defined airspace. RNP can include both performance
and functional requirements and is indicated by the RNP type.
These standards are intended for designers, manufacturers,
and installers of avionics equipment, as well as service
providers and users of these systems for global operations.
The minimum aviation system performance specification
(MASPS) provides guidance for the development of airspace
and operational procedures needed to obtain the benefits of
improved navigation capability. [Figure 9-41]
The RNP type defines the total system error (TSE) that
is allowed in lateral and longitudinal dimensions within
a particular airspace. The TSE, which takes account of
navigation system errors (NSE), computation errors, display
errors and flight technical errors (FTE), must not exceed the
specified RNP value for 95 percent of the flight time on any
part of any single flight. RNP combines the accuracy standards
laid out in the ICAO Manual (Doc 9613) with specific accuracy
requirements, as well as functional and performance standards,
for the RNAV system to realize a system that can meet future
air traffic management requirements. The functional criteria
for RNP address the need for the flightpaths of participating
aircraft to be both predictable and repeatable to the declared
levels of accuracy. More information on RNP is contained in
subsequent chapters.
The term RNP is also applied as a descriptor for airspace,
routes, and procedures (including departures, arrivals,
and IAPs). The descriptor can apply to a unique approach
procedure or to a large region of airspace. RNP applies to
navigation performance within a designated airspace and
includes the capability of both the available infrastructure
(navigation aids) and the aircraft.
RNP type is used to specify navigation requirements for the
airspace. The following are ICAO RNP Types: RNP-1.0,
RNP-4.0, RNP-5.0, and RNP-10.0. The required performance
is obtained through a combination of aircraft capability and
the level of service provided by the corresponding navigation
infrastructure. From a broad perspective:
9-44
Aircraft Capability + Level of Service = Access
In this context, aircraft capability refers to the airworthiness
certification and operational approval elements (including
avionics, maintenance, database, human factors, pilot
procedures, training, and other issues). The level of service
element refers to the NAS infrastructure, including published
routes, signal-in-space performance and availability, and air
traffic management. When considered collectively, these
elements result in providing access. Access provides the
desired benefit (airspace, procedures, routes of flight, etc.).
RNP levels are actual distances from the centerline of the
flightpath, which must be maintained for aircraft and obstacle
separation. Although additional FAA-recognized RNP
levels may be used for specific operations, the United States
currently supports three standard RNP levels:
•
RNP 0.3 – Approach
•
RNP 1.0 – Departure, Terminal
•
RNP 2.0 – En route
RNP 0.3 represents a distance of 0.3 NM either side of a
specified flightpath centerline. The specific performance that
is required on the final approach segment of an instrument
approach is an example of this RNP level. At the present
time, a 0.3 RNP level is the lowest level used in normal
RNAV operations. Specific airlines, using special procedures,
are approved to use RNP levels lower than RNP 0.3, but
those levels are used only in accordance with their approved
operations specifications (OpsSpecs). For aircraft equipment to
qualify for a specific RNP type, it must maintain navigational
accuracy at least 95 percent of the total flight time.
Flight Management Systems (FMS)
A flight management system (FMS) is not a navigation
system in itself. Rather, it is a system that automates the
tasks of managing the onboard navigation systems. FMS may
perform other onboard management tasks, but this discussion
is limited to its navigation function.
FMS is an interface between flight crews and flightdeck
systems. FMS can be thought of as a computer with a large
database of airport and NAVAID locations and associated
data, aircraft performance data, airways, intersections,
DPs, and STARs. FMS also has the ability to accept and
store numerous user-defined WPs, flight routes consisting
of departures, WPs, arrivals, approaches, alternates, etc.
FMS can quickly define a desired route from the aircraft’s
current position to any point in the world, perform flight
plan computations, and display the total picture of the flight
route to the crew.

~\
"J
FINAL APPROACH
@
0.3 NM
e@
0.3 NM
TERMINAL
@
1.0 NM
-
EN ROUTE
@
y
a
1.0 NM
/
2.0 NM
~\
_
y
XQ
,
’ 4
2.0 NM
RNP 0.3
RNP 1.0
RNP 2.0
RNP 1.0
y.6O
y.6O
>wa
:
APPROACH
TERMINAL
ENROUTE
DEPARTURE
Figure 9-41. Required navigation performance.
FMS also has the capability of controlling (selecting) VOR,
act as the input/output device for the onboard navigation
DME, and LOC NAVAIDs, and then receiving navigational
systems, so that it becomes the “go-between” for the crew
data from them. INS, LORAN, and GPS navigational data
and the navigation systems.
may also be accepted by the FMS computer. The FMS may
9-45

Function of FMS
At startup, the crew programs the aircraft location, departure
runway, DP (if applicable), WPs defining the route, approach
procedure, approach to be used, and routing to alternate. This
may be entered manually, be in the form of a stored flight
plan, or be a flight plan developed in another computer and
transferred by disk or electronically to the FMS computer.
The crew enters this basic information in the control/display
unit (CDU). [Figure 9-42]
Once airborne, the FMS computer channels the appropriate
NAVAIDs and takes radial/distance information or
channels two NAVAIDs, taking the more accurate distance
information. FMS then indicates position, track, desired
heading, groundspeed, and position relative to desired track.
Position information from the FMS updates the INS. In more
sophisticated aircraft, the FMS provides inputs to the HSI,
RMI, glass flight deck navigation displays, head-up display
(HUD), autopilot, and autothrottle systems.
Head-Up Display (HUD)
The HUD is a display system that provides a projection of
navigation and air data (airspeed in relation to approach
reference speed, altitude, left/right and up/down GS) on a
transparent screen between the pilot and the windshield.
Other information may be displayed, including a runway
target in relation to the nose of the aircraft. This allows the
pilot to see the information necessary to make the approach
while also being able to see out the windshield, which
diminishes the need to shift between looking at the panel to
looking outside. Virtually any information desired can be
displayed on the HUD if it is available in the aircraft’s flight
computer and if the display is user definable. [Figure 9-43]
Radar Navigation (Ground-Based)
Radar works by transmitting a pulse of RF energy in a specific
direction. The return of the echo or bounce of that pulse from
The Universal UNS-1
Figure 9-42. Typical display and control unit(s) in general aviation. The Universal UNS-1 (left) controls and integrates all other systems. The
Avidyne (center) and Garmin systems (right) illustrate and are typical of completely integrated systems. Although the Universal CDU is not
typically found on smaller general aviation aircraft, the difference in capabilities of the CDUs and stand-alone sytems is diminishing each year.
9-46
a target is precisely timed. From this, the distance traveled
by the pulse and its echo is determined and displayed on a
radar screen in such a manner that the distance and bearing to
this target can be instantly determined. The radar transmitter
must be capable of delivering extremely high power levels
toward the airspace under surveillance, and the associated
radar receiver must be able to detect extremely small signal
levels of the returning echoes.
The radar display system provides the controller with a map-
like presentation upon which appear all the radar echoes
of aircraft within detection range of the radar facility. By
means of electronically-generated range marks and azimuth-
indicating devices, the controller can locate each radar target
with respect to the radar facility, or can locate one radar target
with respect to another.
Another device, a video-mapping unit, generates an actual
airway or airport map and presents it on the radar display
equipment. Using the video-mapping feature, the air traffic
controller not only can view the aircraft targets, but can see
these targets in relation to runways, navigation aids, and
hazardous ground obstructions in the area. Therefore, radar
becomes a NAVAID, as well as the most significant means
of traffic separation.
In a display presenting perhaps a dozen or more targets,
a primary surveillance radar system cannot identify one
specific radar target, and it may have difficulty “seeing” a
small target at considerable distance—especially if there is
a rain shower or thunderstorm between the radar site and
the aircraft. This problem is solved with the Air Traffic
Control Radar Beacon System (ATCRBS), sometimes
called secondary surveillance radar (SSR), which utilizes
a transponder in the aircraft. The ground equipment is an
interrogating unit, in which the beacon antenna is mounted
so it rotates with the surveillance antenna. The interrogating
The Avidyne
The Garmin system

of azimuth and present target information on a radar display
located in a tower or center. This information is used
independently or in conjunction with other navigational aids
in the control of air traffic.
ARSR is a long-range radar system designed primarily to
cover large areas and provide a display of aircraft while en
route between terminal areas. The ARSR enables air route
traffic control center (ARTCC) controllers to provide radar
service when the aircraft are within the ARSR coverage.
In some instances, ARSR may enable ARTCC to provide
terminal radar services similar to but usually more limited
than those provided by a radar approach control.
ASR is designed to provide relatively short-range coverage
in the general vicinity of an airport and to serve as an
[=]
gS
expeditious means of handling terminal area traffic through
observation of precise aircraft locations on a radarscope.
Nonprecision instrument approaches are available at airports
(aa)
that have an approved surveillance radar approach procedure.
ASR provides radar vectors to the final approach course and
then azimuth information to the pilot during the approach.
In addition to range (distance) from the runway, the pilot
is advised of MDA, when to begin descent, and when the
aircraft is at the MDA. If requested, recommended altitudes
are furnished each mile while on final.
~
eels,
PAR is designed to be used as a landing aid displaying range,
azimuth, and elevation information rather than as an aid for
a5,
sequencing and spacing aircraft. PAR equipment may be
used as a primary landing aid, or it may be used to monitor
other types of approaches. Two antennas are used in the PAR
array: one scanning a vertical plane and the other scanning
horizontally. Since the range is limited to 10 miles, azimuth
a
=
)
[-
to 20°, and elevation to 7°, only the final approach area is
covered. The controller’s scope is divided into two parts. The
Figure 9-43. Example of a head-up display (top) and a head-down
upper half presents altitude and distance information, and the
lower half presents azimuth and distance.
display (bottom). The head-up display presents information in front of
the pilot along his/her normal field of view while a head-down display
PAR is a system in which a controller provides highly
may present information beyond the normal head-up field of view.
accurate navigational guidance in azimuth and elevation
unit transmits a coded pulse sequence that actuates the aircraft
to a pilot. Pilots are given headings to fly to direct them to
transponder. The transponder answers the coded sequence
and keep their aircraft aligned with the extended centerline
by transmitting a preselected coded sequence back to the
of the landing runway. They are told to anticipate glidepath
ground equipment, providing a strong return signal and
interception approximately 10–30 seconds before it occurs
positive aircraft identification, as well as other special data
and when to start descent. The published decision height (DH)
such as aircraft altitude.
is given only if the pilot requests it. If the aircraft is observed
to deviate above or below the glidepath, the pilot is given
Functions of Radar Navigation
the relative amount of deviation by use of terms “slightly” or
The radar systems used by ATC are air route surveillance
“well” and is expected to adjust the aircraft’s rate of descent/
radar (ARSR), airport surveillance radar (ASR), and
ascent to return to the glidepath. Trend information is also
precision approach radar (PAR) and airport surface detection
issued with respect to the elevation of the aircraft and may
equipment (ASDE). Surveillance radars scan through 360°
9-47

be modified by the terms “rapidly” and “slowly” (e.g., “well
above glidepath, coming down rapidly”).
Range from touchdown is given at least once each mile. If
an aircraft is observed by the controller to proceed outside
of specified safety zone limits in azimuth and/or elevation
and continue to operate outside these prescribed limits, the
pilot will be directed to execute a missed approach or to fly a
specified course unless the pilot has the runway environment
(runway, approach lights, etc.) in sight. Navigational
guidance in azimuth and elevation is provided to the pilot
until the aircraft reaches the published decision altitude (DA)/
DH. Advisory course and glidepath information is furnished
by the controller until the aircraft passes over the landing
threshold, at which point the pilot is advised of any deviation
from the runway centerline. Radar service is automatically
terminated upon completion of the approach.
Airport Surface Detection Equipment
Radar equipment is specifically designed to detect all
principal features on the surface of an airport, including
aircraft and vehicular traffic, and to present the entire image
on a radar indicator console in the control tower. It is used
to augment visual observation by tower personnel of aircraft
and/or vehicular movements on runways and taxiways.
Radar Limitations
1.
It is very important for the aviation community to
recognize the fact that there are limitations to radar
service and that ATC may not always be able to issue
traffic advisories concerning aircraft which are not
under ATC control and cannot be seen on radar.
2.
The characteristics of radio waves are such that they
normally travel in a continuous straight line unless
they are “bent” by abnormal atmospheric phenomena
such as temperature inversions; reflected or attenuated
by dense objects such as heavy clouds, precipitation,
ground obstacles, mountains, etc.; or screened by high
terrain features.
3.
Primary radar energy that strikes dense objects is
reflected and displayed on the operator’s scope,
thereby blocking out aircraft at the same range and
greatly weakening or completely eliminating the
display of targets at a greater range.
9-48
4.
Relatively low altitude aircraft are not seen if they are
screened by mountains or are below the radar beam
due to curvature of the Earth.
5.
The amount of reflective surface of an aircraft
determines the size of the radar return. Therefore,
a small light airplane or a sleek jet fighter is more
difficult to see on primary radar than a large
commercial jet or military bomber.
6.
All ARTCC radar in the conterminous United States
and many ASR have the capability to interrogate Mode
C and display altitude information to the controller
from appropriately-equipped aircraft. However,
a number of ASR do not have Mode C display
capability; therefore, altitude information must be
obtained from the pilot.