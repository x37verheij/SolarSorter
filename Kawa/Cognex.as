.PROGRAM solarSorter() ; Project bij GTM | Q1 '20'21 | Sorteren van zonnecellen
  ; *******************************************************************
  ;
  ; Program:      solarSorter
  ; Comment:      Voor het eerste bedrijfsproject in de minor heeft GTM gevraagd of wij een systeem kunnen bouwen die trays met zonnecellen en een excelsheet accepteert en dat omzet naar gesorteerde trays met ieder een bepaalde klasse cellen.
  ;     De robot zal initieel verbinding maken met de TCP server van de python pc en reageren op elk bericht dat de pc stuurt.
  ;     Gedurende het programma zal de robot vanuit de rustpositie wachten tot de pc uit de invoercamera beeld heeft ontvangen en de robot vertelt waar de ongesorteerde cellen liggen. De robot pakt dan een voor een elke ongesorteerde cel op en verplaatst deze boven de qrcamera. De robot zal de pc een bericht sturen dat deze op locatie is.
  ;     De pc zal het serienummer laten scannen door de qrcamera en koppelen aan deze cel in de eerste foto. Vervolgens wordt de klasse opgezocht in de excelsheet en stuurt de pc de klasse naar de robot. De robot verplaatst de cel dan naar de uitvoertray met cellen van die klasse. De robot verplaatst zich dan weer naar de rustpositie.
  ;     Mocht een uitvoertray vol zitten, laat de robot dit via de pc weten en stopt met verdergaan totdat hij expliciet te horen krijgt dat de uitvoertray is verwijderd. Dit gaat via de hmi. Vervolgens plaatst de robot een lege tray op de geleegde plek en vervolgt hij zijn programma.
  ;     Mocht de invoertray leeg zijn, dan vertelt de pc niet welke cel de robot moet pakken, maar dat de tray leeg is en vervangen moet worden. De robot verplaatst dan de lege tray en gaat terug naar de rustpositie. De robot laat vervolgens de pc vertellen waar de volgende cellen liggen en gaat deze een na een af.
  ; Author:       User
  ;
  ; Date:         october 12th, 2020
  ;
  ; *******************************************************************
  ;
  ; AS Programming Language: variables
  ; var1      : Global variables are saved in memory and can be used in any program
  ; .var2     : Local variables are not saved
  ; $var3     : String variable
  ; var4[5]   : Element located directly to the right of var4[4], index must be in [0-9999]
  ; var5[1,2] : Element in 2D array var5
  ; pose1     : Transformation pose (consists of the values x, y, z, rx, ry, rz)
  ; #pose2    : Joint pose (consists of the values JT1, JT2, JT3, JT4, JT5, JT6)
  ;
  ; Variable name can only consist of: [0-9a-zA-Z._] and are case insensitive
  ; Variable names start with [a-zA-Z] and have a length of max 15 characters
  ;
  ; *Invalid* variable names: (See AS programming reference page 41 or 3-12)
  ; 3p        : Does not start with [a-zA-Z]
  ; part#2    : # prefix is reserved for joint poses and cannot be used in variable names
  ; random    : Keyword
  ; TCP_SEND  : Keyword
  ; .arr[1]   : Arrays can't be defined local variables. 
  ;
  ; For defining/accessing arrays:
  ; arr[1] = 6    ; Cannot assign multiple variables on the same line
  ; arr[3] = 7    ;   e.g. var1 = 6, var2 = 7 is a syntax error
  ; PRINT arr[2]  ; Gives runtime error E0102: Variable is not defined.
  ;
  ; For operators: many are valid, see AS programming reference page 50 or 3-21
  ;
  ; For comparing strings: (See AS programming reference page 53 or 3-24)
  ; "AAA"  < "AAB"
  ; "ABC" == "ABC"
  ; "DEF." > "DEF"
  ; "xyz"  > "XYZ"
  ;
  ; Loops / other structure instructions:
  ; IF expr THEN ... [ELSE ...] END     ; ELSEIF does not exist in the AS programming reference and appears to be an invalid statement
  ; WHILE expr DO ... END
  ; DO ... UNTIL expr
  ; FOR var = x TO y [STEP z] ... END
  ; CASE var OF VALUE x,y,z: ... [VALUE n: ...]+ [ANY ...] END
  ; SCASE $var OF SVALUE $x+"y": ... [SVALUE $x+"z": ... ]+ [ANY ...] END
  ;
  ;
  ; AS Programming Language: poses
  ; HERE #pose1         : Define a joint pose variable using the current pose of the robot
  ; HERE pose2          : Define a transformation pose variable using the current pose of the robot
  ; POINT #pose3        : Type in the joint values or copy them using 'POINT pose3 = pose1'
  ; POINT pose4         : Type in the transformation values or copy them using 'POINT pose4 = pose2'
  ; HERE pose4 + pose5  : Pose5 relative to pose4, since we defined pose4 earlier
  ;
  ;
  ; AS Programming Language: moves
  ; JMOVE pose1         : Joint move: during the move, every joint moves at linear speed
  ; LMOVE pose1         : Linear move: during the move, the tool moves at linear speed
  ; JAPPRO pose1, 100   : Joint move: approach 100 mm above the target pose
  ;
  ; *******************************************************************
  
  ; Variables
  .err = -1             ; Error variable
  .port = 10000         ; Outgoing port
  sock_id1 = -1         ; Positive socket id if connected with pc 
  .timeout = 60         ; Timeout in seconds to wait for a connection
  ip[0] = 0             ; The ip of the connecting pc (ip[1-4])
  $data[0] = ""         ; "Character string variable array"
  MAX_TCP_LENGTH = 255  ; Maximum length of data received/sent
  
  ; Listen for devices that would like to connect
  TCP_LISTEN .err, .port
  IF .err < 0 THEN
    PRINT "ERR IN TCP_LISTEN: ", .err
    GOTO exit
  END
  
  ; Accept connection from the pc. Note that the sock_id param is also the err param
  TCP_ACCEPT sock_id1, .port, .timeout, ip[0]
  IF sock_id1 < 0 THEN
    PRINT "ERR IN TCP_ACCEPT: ", sock_id1
    GOTO exit
  END
  
  ; Stop listening for more devices
  TCP_END_LISTEN .err, .port
  .timeout = 1
  
  ; Loop 2 times and echo messages
  FOR i = 0 TO 1    ; In AS Language 'TO' means: To and including
    
    ; Receive a message
    TCP_RECV .err, sock_id1, $data[0], .length, .timeout, MAX_TCP_LENGTH
    IF .err < 0 THEN
      PRINT "ERR IN TCP_RECV: ", .err
      GOTO exit
    ELSE
      IF .length < 1 THEN
        PRINT "EMPTY MESSAGE IN TCP_RECV"
        GOTO exit
      END
    END
    
    ; Send/echo the message
    TCP_SEND .err, sock_id1, $data[0], .length, .timeout
    IF .err < 0 THEN
      PRINT "ERR IN TCP_SEND: ", .err
      GOTO exit
    END
  END
  
  ; Close connection
  TCP_CLOSE .err, sock_id1
  PRINT "Succesfully disconnected socket ", sock_id1
  sock_id1 = -1
    
  ; Bedenk of je de TCP parallel wil laten lopen op de achtergrond
  ; Uitzoeken. Heet dit subroutine?
  
  exit:
.END
.PROGRAM robotcalibrate () ; 
  ; *******************************************************************
  ;
  ; Program:      test8
  ; Comment:      
  ; Author:       User
  ;
  ; Date:         10/15/2020
  ;
  ; *******************************************************************
  ;
  POINT #neutral = #[0, 100, 100, 0, 0, 0]
  
  ;FOR i = 0 TO 2
  ;  print i
  ;END
    
  SPEED 10
  JMOVE #neutral
.END
.PROGRAM autostart.pc() ; Resets connection boolean with Cognex Camera
  ; *******************************************************************
  ;
  ; Program:      autostart.pc
  ; Comment:      The variable sock_id1 holds a positive value when the Cognex camera is connected. This autostart resets the boolean so that a new connection with the camera can be made.
  ; Author:       User
  ;
  ; Date:         9/30/2020
  ;
  ; *******************************************************************
  ;
  SIGNAL -2254,-2245
  sock_id1 = -2
.END
.PROGRAM Comment___ () ; Comments for IDE. Do not use.
	; @@@ PROJECT @@@
	; @@@ HISTORY @@@
	; 13.10.2020 09:16:15
	; 
	; 15.10.2020 10:53:57
	; 
	; 16.10.2020 11:57:33
	; 
	; 19.10.2020 11:03:33
	; 
	; @@@ INSPECTION @@@
	; @@@ CONNECTION @@@
	; Robot
	; 192.168.0.1
	; 23
	; @@@ PROGRAM @@@
	; 0:solarSorter
	; .err 
	; .port 
	; .timeout 
	; .length 
	; 0:robotcalibrate
	; 0:autostart.pc
	; @@@ TRANS @@@
	; @@@ JOINTS @@@
	; @@@ REALS @@@
	; @@@ STRINGS @@@
	; @@@ INTEGER @@@
	; @@@ SIGNALS @@@
	; @@@ TOOLS @@@
	; @@@ BASE @@@
	; @@@ FRAME @@@
	; @@@ BOOL @@@
.END
