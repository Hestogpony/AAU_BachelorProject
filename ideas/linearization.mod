param n, > 0; #n is the number of edges
param m, > 0; #m is the degree of details

param points{k in 1..n, i in 1..m};
param points2{k in 1..n, i in 1..m};
param linesA{k in 1..n, i in 1..m};
param linesB{k in 1..n, i in 1..m};
var x{k in 1..n, i in 1..m}, integer;
var z{k in 1..n, i in 1..m}, integer;

s.t. OnlyOneLineSeg{k in 1..n}: 0 <= sum{i in 1..m}(z[k,i]) <= 1;
s.t. ZmustBeBinary{k in 1..n, i in 1..m}: 0 <= z[k,i] <= 1;  
s.t. XmustBeOnTheLine{k in 1..n, i in 1..m}: x[k,i] <= z[k,i]*points2[k,i]; 
s.t. XmustBeBetween{k in 1..n, i in 1..m}: x[k,i] >= z[k,i]*points[k,i]; 

maximize obj: sum{k in 1..n} (sum{i in 1..m}(linesA[k,i]*x[k,i])+ sum{i in 1..m} linesB[k,i]*z[k,i]);

solve;
display obj;
display x;
display z;
/* the objective is to use as much energy as possible without importing
           energy exports is left out of this equation and calculated as the schedule is read back */

data;

param m := 5;

param n := 2; 

param points:
   1 2 3 4 5 :=
1  4 5 6 8 9 
2  3 6 8 9 10; 

param points2:
   1 2 3 4 5 :=
1  5 6 7 9 10
2  8 7 10 11 12;

param linesA:
   1 2 3 4 5 :=
1  1 4 1 2 3
2  4 5 2 4 2; 

param linesB:
   1 2 3 4 5 :=
1  3 2 4 5 12
2  4 3 1 3 2; 




