param n, integer, > 0; #length of the path

param edgeDistance{i in 1..n}, > 0; #the length of each road segment

param speedLimits{i in 1..n}, > 0; #the speed limits of each road segment 

param chargingFunctions{i in 1..n, j in 1..2}; #the function for each charging station

param batCap, > 0; #The maximum amount of kWh the battery can hold

var x{i in 1..n}; #The optimal speed for each road segment

var y{i in 1..n}, >= 0; #The optimal charging time for each charging station

var t{i in 1..n};

minimize obj: sum{i in 1..n} (t[i] + y[i]); 

s.t. time{i in 1..n}: t[i] = edgeDistance[i]/x[i]; 

s.t. speed{i in 1..n}: speedLimits[i]*0.7 <= x[i] <= speedLimits[i];

s.t. battery{j in 1..n}: 0 <= sum{i in 1..j}((chargingFunctions[i, 1]*y[i]+chargingFunctions[i, 2]) -  (edgeDistance[i]*(3*x[i])/1000)) <= batCap;

solve; 

display x;
display y; 

data; 

param n := 8; 

param batCap := 40; 

param edgeDistance := 1 20, 2 22, 3 10, 4 8, 5 12, 6 25, 7 9, 8 15; 

param speedLimits := 1 50, 2 40, 3 70, 4 30, 5 90, 6 50, 7 55, 8 12; 

param chargingFunctions : 
  1   2 := 
1 10 0
2 12 0 
3 15 0 
4 16 0 
5 0 0 
6 10 0 
7 8 0 
8 7 0
;




