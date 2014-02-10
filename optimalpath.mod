param numberOfNodes, integer, > 0;
param numberOfEdges, integer, > 0; 

param edgeTime{i in 1..numberOfEdges}, >= 0; 

param edgeCost{i in 1..numberOfEdges}, >= 0; 

param chargingSpeed{i in 1..numberOfNodes}, > 0; 

param batteryCap, integer, > 0; 


var x{i in 1..numberOfNodes}, >= 0.9, <= 1.1; 
var x1{i in 1..numberOfNodes} >= 0.9, <= 1.1;

var y{i in 1..numberOfEdges}, >= 0; 

minimize obj: sum{i in 1..numberOfNodes} edgeTime[i]*x1[i] + sum{j in 1..numberOfEdges} chargingSpeed[j]*y[j]; 

s.t. energy{i in 1..numberOfNodes}:sum{k in 1..i} edgeCost[k]*(x[k]) <= sum{z in 1..i} chargingSpeed[z]*y[z]; 

s.t. battery{j in 1..numberOfEdges}: sum{k in 1..j} chargingSpeed[k]*y[k] - sum{z in 1..j} edgeCost[z]*y[z] <= batteryCap; 

s.t. equal{i in 1..numberOfNodes}: x[i]+x1[i] == 2; 

solve; 

display x;
display y;
display{k in 1..numberOfNodes} edgeCost[k] ,(x[k]);

#Start of data here. 
data; 

param batteryCap := 5;

param numberOfNodes := 4;

param numberOfEdges := 4; 

param edgeTime := 1 0, 2 4, 3 4, 4 2;

param edgeCost := 1 0, 2 5, 3 3, 4 2;

param chargingSpeed := 1 3, 2 4, 3 3, 4 4; 

  




