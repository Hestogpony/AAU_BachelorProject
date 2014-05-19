param n, integer, > 0; #Number of nodes/edges in the path being tested, a path will always have the same amound of nodes and edges. 

param m, integer, > 0; #Number of linear lines used to model function f(x). 

param edgeDist{i in 1..n}, >= 0; #The length of each edge. edgeDist[1] is the length from s to e1 and edgeDist[n] from en-1 to t.

param chargeConstants{i in 1..n},  >= 0; #In this example we asume that charging speed is constant. 

param batCap, > 0, integer; #The max amount of energy the battery can hold. 

param initialBat; #The initial battery of the EV when a path is being solved

param points{i in 1..n, j in 1..m}; #List of all 1st coordinats.

param points2{i in 1..n, j in 1..m}; #List of all 2ed coordinats. 

param linesA{i in 1..n, j in 1..m}; #List of slopes.

param linesB{i in 1..n, j in 1..m}; #List of konstants, a function i is defined by lineA[i]*x[i]+lineB[i]. 

param speedDistanceRelation{i in 1..n,j in 1..2};

var x{i in 1..n, j in 1..m}; #The optimal speed for each road segment.

var z{i in 1..n, j in 1..m}, integer; #Used to ensure only one line segment is choosen. 

var y{i in 1..n}, >= 0; #The optimal charging time at each charging station.


s.t. OnlyOneLineSeg{i in 1..n}: sum{j in 1..m}(z[i,j]) == 1; 
s.t. ZmustBeBinary{i in 1..n, j in 1..m}: 0 <= z[i,j] <= 1;
s.t. XmustBeOnTheLine{i in 1..n, j in 1..m}: x[i,j] <= z[i,j]*points2[i,j];
s.t. XmustBeBetween{i in 1..n, j in 1..m}: x[i,j] >= z[i,j]*points[i,j];

s.t. NoOverCharge{k in 1..n-1}: 0 <= initialBat+(sum{i in 1..k+1}(chargeConstants[i]*y[i])) - (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j]))  <= batCap;

#Todo fik all units to ensure that all mesures of energy have the exact same units and can be comparied. 
s.t. battery{k in 1..n}: 0 <= (sum{i in 1..k}(chargeConstants[i]*y[i])+initialBat) - (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])) <= batCap;

minimize time: sum{i in 1..n} ((speedDistanceRelation[i,1]*(sum{j in 1..m} x[i,j])+speedDistanceRelation[i,2]) + (y[i]));
solve;

#display (sum{i in 1..n}(chargeConstants[i]*y[i]) - (sum{i in 1..n} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])))
#display y;
#display{i in 1..n} chargeConstants[i]*y[i];
#display time;
#display x;

#display sum{i in 1..n} (y[i]+speedDistanceRelation[i,1]*(sum{j in 1..m} x[i,j])+speedDistanceRelation[i,2]);
#display{i in 1..n} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j]);
#display{i in 1..n} edgeDist[i]/sum{j in 1..m} x[i,j];
#display sum{i in 1..n} ((edgeDist[i]/sum{j in 1..m} x[i,j]) + (edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])/chargeConstants[i]));
display sum{i in 1..n} ((edgeDist[i]/sum{j in 1..m} x[i,j]) + (y[i]));
display sum{i in 1..n} chargeConstants[i]*y[i] - sum{i in 1..n} (edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])) + initialBat;
#display sum{i in 1..n} (edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j]));
#display sum{i in 1..n} ((speedDistanceRelation[i,1]*(sum{j in 1..m} x[i,j])+speedDistanceRelation[i,2]) + (y[i]));

