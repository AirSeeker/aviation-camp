Chapter 6
Airborne Navigation Databases
| |
Introduction
Area Navigation (RNAV) systems, aeronautical applications,
and functions that depend on databases are widespread.
[Figure 6-1] Since the 1970s, installed flight systems
have relied on airborne navigation databases to support
their intended functions, such as navigation data used
to facilitate the presentation of flight information to the
flight crew and understanding and better visualization
of the governing aeronautical flight charts. With the
overwhelming upgrades to navigation systems and fully
integrated flight management systems (FMS) that are now
installed in almost all corporate and commercial aircraft,
the need for reliable and consistent airborne navigation
databases is more important than ever.
6-1

fe
os
a
_
ab A
Bee
=
-—
.
S
Ls
BO
@ir re,
alo Bol
=i
BE
=
So
my
mE
ene
a
= ook ma
—__ i
=
9 ===
an
|
a
Figure 6-1. Area navigation (RNAV) receivers.
The capabilities of airborne navigation databases depend
processed by the avionics manufacturer. Vital to this
largely on the way they are implemented by the avionics
discussion is understanding of the regulations guiding
manufacturers. They can provide data about a large
database maintenance and use.
variety of locations, routes, and airspace segments for use
by many different types of RNAV equipment. Databases
There are many different types of RNAV systems certified
can provide pilots with information regarding airports,
for instrument flight rules (IFR) use in the National Airspace
air traffic control (ATC) frequencies, runways, and special
System (NAS). The two most prevalent types are GPS and
use airspace. Without airborne navigation databases,
the multisensory FMS. [Figure 6-2] A modern GPS unit
RNAV would be extremely limited. In order to understand
accurately provides the pilot with the aircraft’s present
the capabilities and limitations of airborne navigation
position; however, it must use an airborne navigation
databases, pilots must understand the way databases
database to determine its direction or distance from
are compiled and revised by the database provider and
another location. The database provides the GPS with
6-2

position information for navigation fixes so it may perform
the required geodetic calculations to determine the
The display allows you to view information stored in the FMS.
6-3 |
appropriate tracks, headings, and distances to be flown.
[Figure 6-3]
. nm
RNG
PROC
CRSR
DTK
Modern FMS are capable of a large number of functions
-
,
TK
MENU
PUSH ON
LEG
BRT
including basic en route navigation, complex departure
APT 1
VOR NDB INT USR ACT NAV FPL SET AUX
and arrival navigation, fuel planning, and precise vertical
D
MSG
OBS
ALT
NRST
CLR
ENT
PULL SCAN
|
navigation. Unlike stand-alone navigation systems, most
FMS/
FMS use several navigation inputs. Typically, they formulate
RANGE
NAV-COM
&
Oo
*
PFD
MENU
−
+
the aircraft’s current position using a combination of
J
iF
FPL
PROC
Controls such as
PUSH CRSR/PUSH 1-2
PUSH
PAN
conventional distance measuring equipment (DME) signals,
buttons and knobs
—
—
PFD
MFD
A
B
C
D
inertial navigation systems (INS), GPS receivers, or other
allow you to make
&
&
E
F
G
H
entries into the FMS.
EMERG
RNAV devices. Like stand-alone navigation avionics, they
&§
&§
NAV
COM
I
J
K
L
rely heavily on airborne navigation databases to provide
=
=
M
N
O
P
—
—
the information needed to perform their numerous
Q
R
S
T
&
&
U
V
W
X
functions.
=
=
Y
Z
SPC
BKSP
−
+
DFLT MAP
SOFTKEY SELECT
Airborne Navigation Database Standardization
—
—
SEL
CLR
ENT
Beginning in the 1970s, the requirement for airborne
navigation databases became more critical. In 1973,
Figure 6-2. GPS with a flight route on display.
GARMIN
ae
VOL
ag
Modified
:
_——{Modify|—
===
(MAB
Pwr”
com
721.600 KSQL > 027
—
KSQL
==)
Be
BRG 060°
ie
SUNOL
21.74 [> Wet
|
:
XPDR
ane16.00"
discontinuity
Seesnracty
eS
[=Arwy]
This FMS allows you to insert
—
21.72 LE ArWwy'|
an entire airway into your route.
cpt
|
No Active Leg
FPL
INFO
w
‘Toaral
Fj
| BACK]| EXEC ||XPND.
ENTER
\ &
susP @
FN
a
a
az
a
CRSR
po cum] V195 + ECA
Viosle
The navigation database looks up
ee
all of the airways that connect to
sm [va07]
-
the previous waypoint in the route.
I
"
fs
N
[334
;
Modified
a
io
i ae
SUNOL
21.7%
|
* ECA:
The software performs a
V195
BACK]
FPL Um TRACY
40.08,
database search for all of the
-
'BRG 060°
airways, causing all waypoints
SHARR.
#9Gi
along the airway to be inserted
ECA,
55.0m
into the route.
|
No Active Leg
FPL
BACK] EXEC | XPND
Figure 6-3. FMS display.

National Airlines installed the Collins ANS-70 and AINS­
70 RNAV systems in their DC-10 fleet, which marked the
first commercial use of avionics that required navigation
databases. A short time later, Delta Air Lines implemented
the use of an ARMA Corporation RNAV system that also
used a navigation database. Although the type of data
stored in the two systems was basically identical, the
designers created the databases to solve the individual
problems of each system, which meant that they were not
interchangeable. As the implementation of RNAV systems
expanded, a world standard for airborne navigation
databases was needed.
In 1973, Aeronautical Radio, Inc. (ARINC) sponsored the
formation of a committee to standardize aeronautical
databases. In 1975, the committee published the first
standard, ARINC Specification 424, which has remained the
worldwide accepted format for transmission of navigation
databases.
ARINC 424
ARINC 424 is the air transport industry’s recommended
standard for the preparation and transmission of data for
the assembly of airborne system navigation databases. The
data is intended for merging with the aircraft navigation
system software to provide a source of navigation
reference. Each subsequent version of ARINC 424
Specification provides additional capability for navigation
systems to utilize. Merging of ARINC 424 data with each
manufacturer’s system software is unique and ARINC 424
leg types provide vertical guidance and ground track for
a specific flight procedure. These leg types must provide
repeatable flight tracks for the procedure design. The
navigation database leg type is the path and terminator
concept.
ARINC 424 Specification describes 23 leg types by their path
and terminator. The path describes how the aircraft gets to
the terminator by flying direct (a heading, a track, a course,
etc.). The terminator is the event or condition that causes
the navigation computer system to switch to the next leg (a
fix, an altitude, an intercept, etc.). When a flight procedure
instructs the pilot to fly runway heading to 2000 feet then
direct to a fix, this is the path and terminator concept. The
path is the heading and the terminator is 2000 feet. The
next leg is then automatically sequenced. A series of leg
types are coded into a navigation database to make a flight
procedure. The navigation database allows an FMS or GPS
navigator to create a continuous display of navigational
data, thus enabling an aircraft to be flown along a specific
route. Vertical navigation can also be coded.
6-4
The data included in an airborne navigation database is
organized into ARINC 424 records. These records are strings
of characters that make up complex descriptions of each
navigation entity. ARINC records can be sorted into four
general groups: fix records, simple route records, complex
route records, and miscellaneous records. Although it is not
important for pilots to have in-depth knowledge of all the
fields contained in the ARINC 424 records, pilots should be
aware of the types of records contained in the navigation
database and their general content.
Fix Records
Database records that describe specific locations on the
face of the earth can be considered fix records. Navigational
aids (NAVAIDs), waypoints, intersections, and airports are
all examples of this type of record. These records can be
used directly by avionics systems and can be included as
parts of more complex records like airways or approaches.
Another concept pilots should understand relates to how
aircraft make turns over navigation fixes. Fixes can be
designated as fly-over or fly-by, depending on how they
are used in a specific route. [Figure 6-4] Under certain
circumstances, a navigation fix is designated as fly-over.
This simply means that the aircraft must actually pass
directly over the fix before initiating a turn to a new course.
Conversely, a fix may be designated fly-by, allowing an
aircraft’s navigation system to use its turn anticipation
feature, which ensures that the proper radius of turn is
commanded to avoid overshooting the new course. Some
RNAV systems are not programmed to fully use this feature.
It is important to remember a fix can be coded as fly-over
and fly-by in the same procedure, depending on how the
fix is used (i.e., holding at an initial approach fix). RNAV or
GPS stand-alone IAPs are flown using data pertaining to
the particular IAP obtained from an onboard database
to include the sequence of all waypoints used for the
approach and missed approach, except that step down
waypoints may not be included in some TSO-C129 receiver
databases. Included in the database, in most receivers, is
coding that informs the navigation system of which WPs
are fly-over or fly-by. The navigation system may provide
guidance appropriately to include leading the turn prior
to a fly-by waypoint; or causing over flight of a fly-over
waypoint. Where the navigation system does not provide
such guidance, the pilot must accomplish the turn lead or
waypoint over flight manually. Chart symbology for the fly­
by waypoint provides pilot awareness of expected actions.
Simple Route Records
Route records are those that describe a flightpath
instead of a fixed position. Simple route records contain

6-5 =
'
a
@&
7a
Fly-over
"|
a
_
a
a
.
_
()
f
~~
~~
Fly-by
~~
~~
Waypoint
Waypoint
Flight plan path
Aircraft track
Figure 6-4. Fly-by-waypoints and fly-over-waypoints.
strings of fix records and information pertaining to how
coding of terminal area procedures, SIDs, STARs, and
the fixes should be used by the navigation avionics.
approach procedures. Simply put, a textual description of
a route or a terminal procedure is translated into a format
that is useable in RNAV systems. One of the most important
A Victor Airway, for example, is described in the database by
concepts for pilots to learn regarding the limitations of
a series of en route airway records that contain the names
RNAV equipment has to do with the way these systems
of fixes in the airway and information about how those
deal with the path and terminator field included in complex
fixes make up the airway.
route records.
Complex Route Records
The first RNAV systems were capable of only one type of
Complex route records include those strings of fixes that
navigation; they could fly directly to a fix. This was not a
describe complex flightpaths like standard instrument
problem when operating in the en route environment
departures (SIDs), standard terminal arrival routes (STARs),
in which airways are mostly made up of direct routes
and instrument approach procedures (IAPs). Like simple
between fixes. The early approaches for RNAV did not
routes, these records contain the names of fixes to be
present problems for these systems and the databases
used in the route, as well as instructions on how the route
they used because they consisted mainly of DME/DME
is flown.
overlay approaches flown only direct point-to-point
navigation. The desire for RNAV equipment to have the
Miscellaneous Records
ability to follow more complicated flightpaths necessitated
There are several other types of information that is coded
the development of the path and terminator field that is
into airborne navigation databases, most of which deal
included in complex route records.
with airspace or communications. The receiver may contain
Path and Terminator Legs
additional information, such as restricted airspace, airport
minimum safe altitudes, and grid minimum off route
There are currently 23 different leg types, or path and
altitudes (MORAs).
terminators that have been created in the ARINC 424
standard that enable RNAV systems to follow the complex
Path and Terminator Concept
paths that make up instrument departures, arrivals, and
The path and terminator concept is a means to permit
approaches. They describe to navigation avionics a path

to be followed and the criteria that must be met before
the path concludes and the next path begins. Although
there are 23 leg types available, none of the manufactured
database equipment is capable of using all of the leg types.
Pilots must continue to monitor procedures for accuracy
and not rely solely on the information that the database
is showing. If the RNAV system does not have the leg type
Figure 6-5. Initial fix.
demanded by procedures, data packers have to select one
or a combination of available lleg types to give the best
approximation, which can result in an incorrect execution
of the procedure. Below is a list of the 23 leg types and
their uses that may or may not be used by all databases.
TF LEG
Figure 6-6. Track to a fix leg type.
•
Initial fix or IF leg—defines a database fix as a point
in space and is only required to define the beginning
of a route or procedure. [Figure 6-5]
•
Track to a fix or TF leg—defines a great circle track
over the ground between two known database
fixes and the preferred method for specification of
straight legs (course or heading can be mentioned
on charts but designer should ensure TF leg is used
for coding). [Figure 6-6]
•
Constant radius arc or RF leg—defines a constant
radius turn between two databases fixes, lines
tangent to the arc, and a center fix. [Figure 6-7]
•
Course to a fix or CF leg—defines a specified course
to a specific database fix. Whenever possible, TF legs
6-6
G
Next
LE
segment
F
R
ARC
CENTER
FIX
segment
Previous
Figure 6-7. Constant radius arc or RF leg.
CF LEG
080°
Course is flown making adjustment for wind
Figure 6-8. Course to a fix or CF leg.
Unspecified position
DF LEG
Figure 6-9. Direct to a fix or DF leg.
Unspecified position
FA LEG
080°
8,000'
FA leg is flown making adjustment for wind
Figure 6-10. Fix to an altitude or FA leg.

should be used instead of CF legs to avoid magnetic
database fix until manual termination of the leg.
variation issues. [Figure 6-8]
[Figure 6-13]
•
Direct to a fix or DF leg—defines an unspecified track
•
Course to an altitude or CA leg—defines a specified
starting from an undefined position to a specified
course to a specific altitude at an unspecified
fix. [Figure 6-9]
position. [Figure 6-14]
•
Fix to an altitude or FA leg—defines a specified track
•
Course to a DME distance or CD leg—defines a
Unspecified position
090°
FC LEG
CA LEG
080°
9 NM
9,000'
Course is flown making adjustment for wind
Figure 6-11. Track from a fix from a distance or FC leg.
Figure 6-14. Course to an altitude or CA leg.
080°
D 10
FD LEG
D 10
090°
CD LEG
Figure 6-12. Track from a fix to a DME distance or FD leg.
Figure 6-15. Course to a DME distance of CD leg.
Manual
termination
080°
FM LEG
Next leg
070°
090°
FM leg is flown making adjustment for wind
CI LEG
Figure 6-13. From a fix to a manual termination or FM leg.
Figure 6-16. Course to an intercept or CI leg.
over the ground from a database fix to a specified
altitude at an unspecified position. [Figure 6-10]
•
Track from a fix from a distance or FC leg—defines
a specified track over the ground from a database
120°
CR LEG
fix for a specific distance. [Figure 6-11]
170°
•
Track from a fix to a distance measuring equipment
(DME) distance or FD leg—defines a specified track
over the ground from a database fix to a specific
DME distance that is from a specific database DME
NAVAID. [Figure 6-12]
•
From a fix to a manual termination or FM leg—
Figure 6-17. Course to a radial termination or CR leg.
defines a specified track over the ground from a
6-7

specified course to a specific DME distance that is
defines a specified heading to a specific altitude
from a specific database DME NAVAID. [Figure 6-15]
termination at an unspecified position. [Figure 6-19]
•
Course to an intercept or CI leg—defines a specified
•
Heading to a DME distance termination or VD
course to intercept a subsequent leg. [Figure 6-16]
leg—defines a specified heading terminating at a
specified DME distance from a specific database
•
Course to a radial termination or CR leg—defines a
DME NAVAID. [Figure 6-20]
course to a specified radial from a specific database
VOR NAVAID. [Figure 6-17]
•
Heading to an intercept or VI leg—defines a
specified heading to intercept the subsequent leg
at an unspecified position. [Figure 6-21]
Next leg
070°
G
LE
090°
D10
F
A
VI LEG
Figure 6-21. Heading to an intercept or VI leg.
Boundary radial
245°
070°
Manual termination
VM LEG
Figure 6-18. Arc to a fix or AF leg.
No correction made for wind
Unspecified position
Figure 6-22. Heading to a manual termination or VM leg.
090°
•
Heading to a manual termination or VM leg—
VA LEG
defines a specified heading until a manual
termination. [Figure 6-22]
8,000'
•
Heading to a radial termination or VR leg—defines a
No correction made for wind
specified heading to a specified radial from a specific
Figure 6-19. Heading to an altitude termination or VA leg.
•
Arc to a fix or AF leg—defines a track over the ground
120°
at a specified constant distance from a database
VR LEG
DME NAVAID. [Figure 6-18]
170°
•
Heading to an altitude termination or VA leg—
D 10
Figure 6-23. Heading to a radial termination or VR leg.
090°
VD LEG
Figure 6-20. Heading to a DME distance termination or VD leg.
6-8

field for the first leg of the departure route. This path and
terminator tells the avionics to provide course guidance
based on heading, until the aircraft reaches 6,000 feet,
018°
and then the system begins providing course guidance
for the next leg. After reaching 6,000 feet, the procedure
PI
calls for a right turn direct to the Grand Junction (JNC)
VORTAC. This leg is coded into the database using the path
063°
and terminator direct to a fix (DF) value, which defines an
unspecified track starting from an undefined position to a
specific database fix.
Another commonly used path and terminator value is
Figure 6-24. Procedure turn or PI leg.
heading to a radial (VR) which is shown in Figure 6-27
database VOR NAVAID. [Figure 6-23]
using the CHANNEL ONE DEPARTURE procedure for Santa
•
Procedure turn or PI leg—defines a course reversal
Ana, California. The first leg of the runway 19L/R procedure
starting at a specific database fix and includes
requires a climb on runway heading until crossing the I-SNA
outbound leg followed by a left or right turn and
1 DME fix or the SLI R-118, this leg must be coded into the
180° course reversal to intercept the next leg. [Figure
database using the VR value in the Path and Terminator
6-24]
field. After crossing the I-SNA 1 DME fix or the SLI R-118, the
avionics should cycle to the next leg of the procedure that
•
Racetrack course reversal or altitude termination
in this case, is a climb on a heading of 175° until crossing SLI
(HA), single circuit terminating at the fix (base turn)
R-132. This leg is also coded with a VR Path and Terminator.
(HF), or manual termination (HM) leg types—define
The next leg of the procedure consists of a heading of 200°
racetrack pattern or course reversals at a specified
until intercepting the SXC R-084. In order for the avionics to
database fix. [Figure 6-25]
correctly process this leg, the database record must include
the heading to an intercept (VI) value in the Path and
Terminator field. This value directs the avionics to follow
HA, HF, HM
a specified heading to intercept the subsequent leg at an
076°
unspecified position.
The path and terminator concept is a very important part
of airborne navigation database coding. In general, it is not
Previous leg
necessary for pilots to have an in-depth knowledge of the
HA - Terminates at an altitude
ARINC coding standards; however, pilots should be familiar
HF - Terminates at the fix after one orbit
with the concepts related to coding in order to understand
HM - Manually terminated
the limitations of specific RNAV systems that use databases.
Figure 6-25. Racetrack course reversal or HA, HF, and HM leg.
Path and Terminator Limitations
How a specific RNAV system deals with Path and
The GRAND JUNCTION FIVE DEPARTURE for Grand Junction
Terminators is of great importance to pilots operating
Regional in Grand Junction, Colorado, provides a good
with airborne navigation databases. Some early RNAV
example of different types of path and terminator legs
systems may ignore this field completely. The ILS or LOC/
used. [Figure 6-26] When this procedure is coded into the
DME RWY 3 approach at Durango, Colorado, provides an
navigation database, the person entering the data into the
example of problems that may arise from the lack of path
records must identify the individual legs of the flightpath
and terminator capability in RNAV systems. Although
and then determine which type of terminator should be
approaches of this type are authorized only for sufficiently
used.
equipped RNAV systems, it is possible that a pilot may elect
to fly the approach with conventional navigation, and then
The first leg of the departure for Runway 11 is a climb
re-engage RNAV during a missed approach. If this missed
via runway heading to 6,000 feet mean sea level (MSL)
approach is flown using an RNAV system that does not use
and then a climbing right turn direct to a fix. When this is
Path and terminator values or the wrong leg types, then
entered into the database, a heading to an altitude (VA)
the system will most likely ignore the first two legs of the
value must be entered into the record’s path and terminator
procedure. This will cause the RNAV equipment to direct
6-9

(UNC5.JNC) 10322
GRAND JUNCTION RGNL (GJT)
GRAND JUNCTION FIVE DEPARTURE
_s.e34 (Fas)
GRAND JUNCTION, COLORADO
ATIS
118.55
CLNC DEL
§,
1217 2878
y s
By oae ON wee
rasiS
GND
yy
7RAND JU
ER
N97 317.4
DEP CON *
feria
DENVER
& 7 wi08er3.33"
UNICOM 122.95
ny
Ss
ow
pe
act
=
o
/
RED TABLE
fi
113.0 DBL S43;
3) OT 25)
y000, SPACES |Chon 77
—960
3909.95),
aap)
ee
$000")
ye
082"
a
GRAND JUNCTION
i aeB0
-
ENS,
(43)
g
1i24INC Epa>
Vy
Pins, ‘te
DIRDY
o
me
‘chon 71
m0
Nae"5s80 |
e
0g,
wio730.91" | &
Ly
+
&
@
g
|
TAKE-OFF OBSTACLE NOTE
Y
3 | Rwy 11: Tree 192’ from DER, 438" left of centerline,
100’ AGL/4949 MSL.
=
& | TAKE-OFF MINIMUMS
Nissi
g
3 | Rwy 4: NA- Obstacles.
wi08"17.36"
B
| Rwy 22: NA- Obstacles, facility receplion (INC VOR/DME).
SAL
3 | Rwy 11: Standard with o minimdng climb of 300’ per NM to 9300.
AS,
=
& | Rwy 29: Standard with a’minimum climb of 300’ per NM to 8300.
Rs,
=
NOTE: Rwy 11, cross DER at orabove 35” AGL/4893 MSL.
i fe
NOTE: Rwy 29, cross DER ator above 35’ AGL/4855’ MSL.
OX S ty
NOTE: BRICK ond DIRDY TRANSITIONS: DME required.
NOTE: Chart notte seal.
BS
™
DEPARTURE ROUTE DESCRIPTION
peciemmovar
via transition/route.
-
ar
(AY 11: Climb runway heading to 6000, then climbing right turn
TAKE-OFF RUNWAY 29: Climb runway heading to 6000, then climbing left turn
‘direct JNC VOR/DME; then via transition/route.
BRICK TRANSITION (JNC5.BRICK): From over JNC VOR/DME via JNC R-113 to
BRICK/JNC 30 DME.
DIRDY TRANSITION (JNC5.DIRDY): From over JNC VOR/DME via JNC R-082 to
HONKR/JNC 17 DME then via JNC R-082 to DIRDY INT/JNC 60 DME.
PACES TRANSITION (JNC5.PACES): From over JNC VOR/DME via JNC R-060 to
PACES INT/JNC 25 DME.
SQUAT TRANSITION (JNC5.SQUAT): From over JNC VOR/DME via JNC R-045 to
SQUAT INT/JNC 31 DME.
GRAND JUNCTION FIVE DEPARTURE
GRAN INGTON, COBRA
(INC5.JNC) 10322
GRAND JUNCTION RGNL (GJT)
Figure 6-26. Grand Junction Five Departure.
6-10

a
(CHANL1.SXC)
SANTA ANA/JOHN WAYNE AIRPORT-ORANGE COUNTY (SNA)
CHANNEL ONE DEPARTURE _ sv277 Faw)
SANTA ANA, CALIFORNIA
ATIS 126.0
‘SHAFTER:
NOT FOR NAVIGATION
118.0
‘Chon 101
‘GND CON
Q
(EAST) 120.8
LOT, HA
(WEST) 132.25
2 oo
ina
Bes
NOTE: RADAR required.
25%
NOTE: Some aircraft may be radar vectored
GORMAN
Noo,
to assigned route.
N35°00.75"
NOTE: Approximate distance from Rwy 19R/L
wiie?36.98"
take-off area to SXC VORTAC is 40 NM.
Chan 108
.
”
a
NOTE: This departure requires a minimum climb
°
rate of 240’ per NM to 2400" MSL.
.
NARGIS
%
Bes
NOTE: This departure is restricted to turbojet and
P\
Sst
turboprop aircraft only. SHAFTER transition
149 Rs Ee
|g)
e
and GORMAN transition restricted to turbojet
Chan 96"
2.
\B)
aircraf.
‘333\e
L347, Hea
BD
TOS ANGELES,
o ON 1s,
ca
TOCALZER 111.75
z
25gto
tna HE
ay NG
Chan54 (Y)
Q
yp
s
>
z
R, °. oa)
8z
S
SEAL BEACH
a
z
VENTURA,
157 SU iE
°
z
108.2 VU =
Chan 104
rR
SOE
WHIPOIT|
Ve
=
Zao
Bes
/
£
Vv
es 2642_/ NOTE: Chart not to scale
‘SANTA CATALINA.
DEPARTURE ROUTE DESCRIPTION
TAKE-OFF RUNWAY 191/R: Maintain runway heading or ISNA localizer south course
to KSNA 1 DME fix or SLI R-118, turn left heading 175°, cross SLI R-132 then turn right
heading 200°, intercept and proceed via SXC R-084 to SXC VORTAC, thence via (transition)
or (assigned route). Expect filed altitude ten minutes after departure.
GORMAN TRANSITION (CHANLI.GMN): From over SXC VORTAC via SXC R-344 and
LAX R-164 to LAX VORTAC, then via LAX R-323 and GMN R-142 to GMN VORTAC.
SAN MARCUS TRANSITION (CHANLI.RZS):
From over SXC VORTAC via SXC R-310 and
VTU R-129 to VTU VOR/DME, then via VTU R-289 and RZS R-109 to RZS VORTAC.
SHAFTER TRANSITION (CHANLI.EHF):
From over SXC VORTAC via SXC R-344 and LAX
R-164 to LAX VORTAC, then via LAX R-337 to LANDO INT and EHF R-126 to EHF VORTAC.
CHANNEL ONE DEPARTURE
seen
(CHANLI.SXC) 07208
SANTA ANA/JOHN WAYNE AIRPORT-ORANGE COUNTY (SNA)
Figure 6-27. Channel One Departure.
6-11

DURANGO, COLORADO.
AL-4B0 (FAA)
10 Hono ar cs]
9 20
ILS or LOC/DME RWY 3
109.1 | 027°
|TOZE | 6638
Apt Elev 6685
DURANGO-LA PLATA COUNTY (DRO)
VME from DROVOR/DME
MALSR | MISSEDAPPROACH:
Simultaneous reception of HDRO and DRO VOR/DME
Climb to 7500 then climbing rightim
-3- |e 10000 via heading140°
required,
ond DRO VOR/DME R-120 to.
© © |SovDE/14
DME ond hold. Continue
climb-infeld
jo 10000
ASOS.
DENVER CENTER
UNICOM,
120.625
118.575 348.7
won
Bas
DME REQUIRED
wp
ey,
7a00
vie
Procedure NA for arrivals of RSK VORTAG
IAF)
sirway radials 333 CW 072
wah
(070°—— [275°
DRO [14)
LOCAUZER
109.)
p
~R27
boro Hes
>
69032 “>
DURANGO.
a,
ee
108.2 DRO E2!_
=
a
=
68192f/~100000
COR
Chan 19
(AF)
TP
sos 5)
Bee
=
g
Yo hes
M
reel Pog (et 8
Ss
ae
Y
OS
(wh
Ks
& fe~)
OG
JURE
SS9
|e
a
N
%,
“Ye
| $
1b
OTE)
we
$5
Xt
ZS
a,
wan | S
3S
Xe
z
R
(;
Ny, SK sove | O
to,XN profi] &
A
°
ose hy ¥
=
OP
Ril
S
g
iF
orl
bi
tinoy
iDare | _fIEV 6685
10000 NoPt
to HINDY.
i ~ pro [14)
fg putt PRO
Mv
IAF
Z
018° (15.6) 9
RATTLESNAKE
8702. A
CO
J
115.3 Rsk STL
fe
Chan 100.
JUBEP
(J
_ Remain
pro[75) te
DRO | SOVDE
a
within 10 NM
——
hhdg | 8-120 [DRO
bm
S207"
|
140°
__oe 027°.
OC only
VBE
DRO.
a
a
ro[2:8)
a
GS 3,00°
|
Lo
ADEE.
G
eau
sia
6638 Offs
Ee
ee
f°
| sis3 |
FS
SS ST
eA
6838-V2 200 (200-15)
f ©
07776.
S-l0C 3
70B0-V2 442 (400-1)
ee
ena
fe Oe
7180-1
442(400-%4) | 442 (400-1)
ery |
7200-1
7220-12
7260-2
HIRLR rea ry
DURANGO, COLORADO
(500-1)_|_515(600-1)_|
535 (400-114) | _575 (600-2
y
Bee aR
DURANGO-LA PLATA COUNTY (DRO)
srorntorasw
ILS or LOC/DME RWY 3
Figure 6-28. ILS or LOC/DME RWY 3 in Durango, Colorado.
6-12

the pilot to make an immediate turn toward the Durango
21 days prior to the effective date of the revision.
VOR instead of flying the series of headings that terminate
at specific altitudes as dictated by the approach procedure.
The integrity of the data is ensured through a process called
[Figure 6-28] Pilots must be aware of their individual
cyclic redundancy check (CRC). A CRC is an error detection
systems Path and Terminator handling characteristics
algorithm capable of detecting small bit-level changes in
and always review the manufacturer’s documentation to
a block of data. The CRC algorithm treats a data block as
familiarize themselves with the capabilities of the RNAV
a single, large binary value. The data block is divided by a
equipment they are operating. Pilots should be aware that
fixed binary number called a generator polynomial whose
some RNAV equipment was designed without the fly-over
form and magnitude is determined based on the level of
capability which can cause problems for pilots attempting
integrity desired. The remainder of the division is the CRC
to use this equipment to fly complex flightpaths in the
value for the data block. This value is stored and transmitted
departure, arrival, or approach environments.
with the corresponding data block. The integrity of the
data is checked by reapplying the CRC algorithm prior to
Role of the Database Provider
distribution.
Compiling and maintaining a worldwide airborne
Role of the Avionics Manufacturer
navigation database is a large and complex job. Within the
United States, the FAA sources give the database providers
When avionics manufacturers develop a piece of
information, in many different formats, which must be
equipment that requires an airborne navigation database,
analyzed, edited, and processed before it can be coded
they typically form an agreement with a database provider
into the database. In some cases, data from outside the
to supply the database for that new avionics platform. It
United States must be translated into English so it may be
is up to the manufacturer to determine what information
analyzed and entered into the database. Once the data is
to include in the database for their system. In some cases,
coded, it must be continually updated and maintained.
the navigation data provider has to significantly reduce the
number of records in the database to accommodate the
Once the FAA notifies the database provider that a change
storage capacity of the manufacturer’s new product, which
is necessary, the update process begins. The change is
means that the database may not contain all procedures.
incorporated into a 28-day airborne database revision cycle
based on its assigned priority. If the information does not
Another important fact to remember is that although there
reach the coding phase prior to its cutoff date (the date that
are standard naming conventions included in the ARINC
new aeronautical information can no longer be included
424 specification, each manufacturer determines how
in the next update), it is held out of revision until the next
the names of fixes and procedures are displayed to the
cycle. The cutoff date for aeronautical databases is typically
pilot. This means that although the database may specify
|
| ewes
om
TK
322,
~eed
|
RK
322%
it) 19600) 1335 KE .
105: Fey
"apd
1280 |W
_
oT
Mi tosco |”
ye
be!
cg
(feoaier|
..
oY
~
|
oe
SIEM]
68. (eee)
=
PIEOFEPes
Pee
it
KEUG
APPROACH
§
x
: ‘=
<ivorone 34
GPsau> il =}
P|
mn
| <Koe
“ULE
‘S)) =)os) oe) ew
oe
EUGA <VOR 34
>APR
ew
IAF / TRAN: D130NIF
a)
—
ri)
|
APP TRANS
rRRvAL>
1h
Figure 6-29. Naming conventions of three different systems for the VOR 34 Approach.
6-13

the approach identifier field for the VOR/DME Runway
34 approach at Eugene Mahlon Sweet Airport (KEUG) in
Eugene, Oregon, as “V34,” different avionics platforms
may display the identifier in any way the manufacturer
deems appropriate. For example, a GPS produced by one
manufacturer might display the approach as “VOR 34,”
whereas another might refer to the approach as “VOR/DME
34,” and an FMS produced by another manufacturer may
refer to it as “VOR34.” [Figure 6-29]
These differences can cause visual inconsistencies between
chart and GPS displays, as well as confusion with approach
clearances and other ATC instructions for pilots unfamiliar
with specific manufacturer’s naming conventions. The
manufacturer determines the capabilities and limitations
of an RNAV system based on the decisions that it makes
regarding that system’s processing of the airborne
navigation database.
Users Role
Like paper charts, airborne navigation databases are
subject to revision. According to 14 CFR Part 91, § 91.503,
the end user (operator) is ultimately responsible for
ensuring that data meets the quality requirements for its
intended application. Updating data in an aeronautical
database is considered to be maintenance and all Part 91
operators may update databases in accordance with 14
CFR Part 91, § 43.3(g). Parts 121, 125, and 135 operators
must update databases in accordance with their approved
maintenance program. For Part 135 helicopter operators,
this includes maintenance by the pilot in accordance with
* Collect the data
* Format per ARINC 424
* Revise and maintain database
Decide on:
* Information to be included
* How information will be processed
+ User interface
* Ensure currency
[Plots
* Execute updates
* Responsible for working knowledge of avionics using
database
Figure 6-30. Database rolls.
6-14
end users)
14 CFR Part 43, § 43.3(h).
Pilots using the databases are ultimately responsible for
ensuring that the database they are operating with is
current. This includes checking Notices to Airmen (NOTAM)­
type information concerning errors that may be supplied
by the avionics manufacturer or the database supplier. The
database user is responsible for learning how the specific
navigation equipment handles the navigation database.
The manufacturer’s documentation is the pilot’s best source
of information regarding the capabilities and limitations of
a specific database. [Figure 6-30]
Operational Limitations of Airborne Navigation
Databases
Understanding the capabilities and limitations of the
navigation systems installed in an aircraft is one of the
pilot’s biggest concerns for IFR flight. Considering the vast
number of RNAV systems and pilot interfaces available
today, it is critical that pilots and flight crews be familiar
with the manufacturer’s operating manual for each RNAV
system they operate and achieve and retain proficiency
operating those systems in the IFR environment.
Most professional and general aviation pilots are familiar
with the possible human factors issues related to flightdeck
automation. It is particularly important to consider those
issues when using airborne navigation databases. Although
modern avionics can provide precise guidance throughout
all phases of flight, including complex departures and
arrivals, not all systems have the same capabilities.
RNAV equipment installed in some aircraft is limited to
direct route point-to-point navigation. Therefore, it is
very important for pilots to familiarize themselves with
|
the capabilities of their systems through review of the
manufacturer documentation. Most modern RNAV systems
|
are contained within an integrated avionics system that
receives input from several different navigation and aircraft
system sensors. These integrated systems provide so much
information that pilots may sometimes fail to recognize
errors in navigation caused by database discrepancies or
misuse. Pilots must constantly ensure that the data they
|
enter into their avionics is accurate and current. Once
the transition to RNAV is made during a flight, pilots and
flight crews must always be capable and ready to revert to
conventional means of navigation if problems arise.
Closed Indefinitely Airports
Some U.S. airports have been closed for up to several years,
|
with little or no chance that they will ever reopen; yet their
“indefinite” closure status – as opposed to permanent or
UFN closure, or abandonment – causes them to continue

to appear on both VFR and IFR charts and in airborne
navigation databases; and their instrument approach
procedures, if any, continue to be included – and still
appear to be valid – in the paper and electronic versions
of the United States Terminal Procedures Publication (TPP)
charts. Airpark South, 2K2, at Ozark, Missouri, is a case in
point.
Even though this airport has been closed going on two
years and, due to industrial and residential development
surrounding it, likely will never be reopened, the airport
is nonetheless still charted in a way that could easily lead
a pilot to believe that it is still open and operating. Even
the current U.S. Low Altitude En route chart displays a
blue symbol for this airport, indicating that it still has
a Department of Defense (DOD) approved instrument
approach procedure available for use.
Aircrews need to use caution when selecting an airport
in a cautionary or emergency situation, especially if the
airport was not previously analyzed suitable for diversion
during preflight. Aircrews could assume, based on charts
and their FMS database, the airport is suitable and perhaps
the only available diversionary or emergency option. The
airport however, could be closed and hazardous even for
emergency use. In these situations, Air Traffic Control may
be queried for the airport’s status.
Storage Limitations
As the data in a worldwide database grows, the required
data storage space increases. Over the years that panel-
mounted GPS and FMSs have developed, the size of the
commercially available airborne navigation databases has
grown exponentially.
Some manufacturer’s systems have kept up with this
growth and some have not. Many of the limitations of
older RNAV systems are a direct result of limited data
storage capacity. For this reason, avionics manufacturers
must make decisions regarding which types of procedures
will be included with their system. For instance, older GPS
units rarely include all of the waypoints that are coded into
master databases. Even some modern FMS equipment,
which typically have much larger storage capacity, do not
include all of the data that is available from the database
producers. The manufacturers often choose not to include
certain types of data that they think is of low importance
to the usability of the unit. For example, manufacturers
of FMS used in large airplanes may elect not to include
airports where the longest runway is less than 3,000 feet
or to include all the procedures for an airport.
Manufacturers of RNAV equipment can reduce the size of
the data storage required in their avionics by limiting the
geographic area the database covers. Like paper charts, the
amount of data that needs to be carried with the aircraft is
directly related to the size of the coverage area. Depending
on the data storage that is available, this means that the
larger the required coverage area, the less detailed the
database can be.
Again, due to the wide range of possible storage capacities,
and the number of different manufacturers and product
lines, the manufacturer’s documentation is the pilot’s best
source of information regarding limitations caused by
storage capacity of RNAV avionics.
Charting/Database Inconsistencies
It is important for pilots to remember that many
inconsistencies may exist between aeronautical charts
and airborne navigation databases. Since there are so
many sources of information included in the production
of these materials, and the data is manipulated by several
different organizations before it is eventually displayed
on RNAV equipment, the possibility is high that there will
be noticeable differences between the charts and the
databases. Because of this, pilots must be familiar with the
capabilities of the database and have updated aeronautical
charts while flying to ensure the proper course is being
flown.
Naming Conventions
Obvious differences exist between the names of procedures
shown on charts and those that appear on the displays of
many RNAV systems. Most of these differences can be
accounted for simply by the way the avionics manufacturers
elect to display the information to the pilot. It is the avionics
manufacturer that creates the interface between the pilot
and the database. For example, the VOR 12R approach in
San Jose, California, might be displayed several different
ways depending on how the manufacturer designs the
pilot interface. Some systems display procedure names
exactly as they are charted, but many do not.
The naming of multiple approaches of the same type to the
same runway is also changing. Multiple approaches with
the same guidance will be annotated with an alphabetical
suffix beginning at the end of the alphabet and working
backwards for subsequent procedures (e.g., ILS Z RWY
28, ILS Y RWY 28, etc.). The existing annotations, such as
ILS 2 RWY 28 or Silver ILS RWY 28, will be phased out and
replaced with the new designation.
NAVAIDs are also subject to naming discrepancies as well.
This problem is complicated by the fact that multiple
NAVAIDs can be designated with the same identifier. VOR
6-15

manufacturer’s naming conventions.
XYZ may occur several times in a provider’s database, so
the avionics manufacturer must design a way to identify
For detailed operational guidance, refer to Advisory Circular
these fixes by a more specific means than the three-letter
(AC) 90-100, U.S. Terminal and En Route Area Navigation
identifier. Selection of geographic region is used in most
(RNAV) Operations; AC 90-101, Approval Guidance for
instances to narrow the pilot’s selection of NAVAIDs with
Required Navigation Performance (RNP) Procedures with
like identifiers.
Authorization Required (AR); AC 90-105, Approval guidance
for RNP Operations and Barometic Vertical Navigation
Non-directional beacons (NDBs) and locator outer markers
in the U.S. National Airspace System and in Oceanic and
(LOMs) can be displayed differently than they are charted.
Remote Continental Airspace; and AC 90-107, Guidance
When the first airborne navigation databases were being
for Localizer Performance with Vertical Guidance and
implemented, NDBs were included in the database as
Localizer Performance without Vertical Guidance Approach
waypoints instead of NAVAIDs. This necessitated the use
Operations in the U.S. National Airspace System.
of five character identifiers for NDBs. Eventually, the NDBs
were coded into the database as NAVAIDs, but many of
Issues Related To Magnetic Variation
the RNAV systems in use today continue to use the five-
character identifier. These systems display the characters
Magnetic variations for locations coded into airborne
“NB” after the charted NDB identifier. Therefore, NDB ABC
navigation databases can be acquired in several ways. In
would be displayed as “ABCNB.”
many cases they are supplied by government agencies in
the epoch year variation format. Theoretically, this value
Other systems refer to NDB NAVAIDs using either the NDB’s
is determined by government sources and published for
charted name if it is five or fewer letters, or the one to three
public use every five years. Providers of airborne navigation
character identifier. PENDY NDB located in North Carolina,
databases do not use annual drift values; instead the
for instance, is displayed on some systems as“PENDY,”while
database uses the epoch year variation until it is updated by
other systems might only display the NDBs identifier “ACZ.”
the appropriate source provider. In the United States, this
[Figure 6-31]
is the National Oceanic and Atmospheric Administration
(NOAA). In some cases the variation for a given location is
Using the VOR/DME Runway 34 approach at Eugene
a value that has been calculated by the avionics system.
Mahlon Sweet Airport (KEUG) in Eugene, Oregon, as
These dynamic magnetic variation values can be different
another example, which is named V34, may be displayed
than those used for locations during aeronautical charting
differently by another avionics platform. For example, a
and must not be used for conventional NAVAIDs or airports.
GPS produced by one manufacturer might display the
approach as VOR 34, whereas another might refer to the
Discrepancies can occur for many reasons. Even when the
approach as VOR/DME 34, and an FMS produced by another
variation values from the database are used, the resulting
manufacturer may refer to it as VOR34. These differences
calculated course might be different from the course
can cause visual inconsistencies between chart and GPS
depicted on the charts. Using the magnetic variation for the
displays, as well as confusion with approach clearances
region instead of the actual station declination can result
and other ATC instructions for pilots unfamiliar with specific
in differences between charted and calculated courses and
Pa / few i +B
soe
fort)
-f
A]
i
ys
a
f
Y
r
WASHINGTON
Semper
x g
bo /|
wag
/
Le
J
Jf
|
(
|
rrcxsona
Re
Se, |
(a anf)
|
|
oan
P
.
-
A}
\
al\\
/
\
|
i
}
|
we \ JS
\/
fs
101 Nea ait
S
|
UB = f_ —$8.
\ |
anarerae
/
S
S
=
—_ 4 Bate
vauace
y
1 S203 EXCLUDES ABSPACE
<
Pn,
re
;
frome
Li
oe
:
ere
I\
Wing,
*
—
|
Ng, a
| cous
© Oe
%
"
ae
|
sé
TNA HEN
J \
s
Se
#008,
ay
Y
hy
=
y
Uy,
gv?
=,
x»
Figure 6-31. Manufacturer’s naming conventions.
6-16

incorrect ground track. Station declination is only updated
when a NAVAID is site checked by the governing authority
that controls it, so it is often different than the current
magnetic variation for that location. Using an onboard
means of determining variation usually entails coding
some sort of earth model into the avionics memory. Since
magnetic variation for a given location changes predictably
over time, this model may only be correct for one time in
the lifecycle of the avionics. This means that if the intended
lifecycle of a GPS unit were 20 years, the point at which the
variation model might be correct would be when the GPS
unit was 10 years old. The discrepancy would be greatest
when the unit was new, and again near the end of its life
span.
Another issue that can cause slight differences between
charted course values and those in the database
occurs when a terminal procedure is coded using
magnetic variation of record. When approaches or other
procedures are designed, the designers use specific rules
to apply variation to a given procedure. Some controlling
government agencies may elect to use the epoch year
variation of an airport to define entire procedures at that
airport. This may result in course discrepancies between
the charted value and the value calculated using the actual
variations from the database.
Issues Related To Revision Cycle
Pilots should be aware that the length of the airborne
navigation database revision cycle could cause
discrepancies between aeronautical charts and information
derived from the database. One important difference
between aeronautical charts and databases is the length
of cutoff time. Cutoff refers to the length of time between
the last day that changes can be made in the revision, and
the date the information becomes effective. Aeronautical
charts typically have a cutoff date of 10 days prior to the
effective date of the charts.
6-17

6-18