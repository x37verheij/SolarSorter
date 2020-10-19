.PROGRAM KAWABOT() ; test
  ; *******************************************************************
  ;
  ; Program:      KAWABOT
  ; Comment:      test
  ; Author:       User
  ;
  ; Date:         10/5/2020
  ;
  ; *******************************************************************
  ;
  ;z=-56,711
  ;y=-91,5
  
  POINT start = #[2.573, 124.960, 119.467, -156.385, -5.291, -21.385]
  POINT abovecamera = #[-31.245,   105.156,    92.962 ,    0.272,    14.572 ,  151.734]
  
  POINT ITC1H= #[-66.735,93.106,58.038,-179.007,-34.633,202.493]
  POINT ITC1L= #[-66.672,79.320,43.007,-179.035,-35.874,202.594]
  ;POINT KAAS= [-471.976,204.398,327.774,104.682,0.718,-14.636]
  
  ;POINT ITC2H= [-471.789,203.702,271.063,104.663,0.715,-14.620]
 
  ;POINT ITC2H= *(-471.789,   112.702,   271.063,   104.663,     0.715,   -14.620)
  ;POINT ITC2L= *(-471.789,   112.702,   327.774,   104.663,     0.715,  -14.620)
  
  
  FOR .i = 1 TO 3
  SPEED 20
  PRINT "Frits is een sletje"
  JMOVE start
  TWAIT 1
  JMOVE ITC1H
  TWAIT 1
  LMOVE ITC1L
  TWAIT 1
  LMOVE ITC1H
  TWAIT 1
  ;JMOVE ITC2H
  TWAIT 1
  ;JMOVE ITC2L
  TWAIT 1
  ;JMOVE ITC2H
  TWAIT 1
  
  END
.END
