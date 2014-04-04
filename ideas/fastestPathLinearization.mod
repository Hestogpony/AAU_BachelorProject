param n, integer, > 0; #Number of nodes/edges in the path being tested, a path will always have the same amound of nodes and edges. 

param m, integer, > 0; #Number of linear lines used to model function f(x). 

param edgeDist{i in 1..n}, integer, > 0; #The length of each edge. edgeDist[1] is the length from s to e1 and edgeDist[n] from en-1 to t.

param chargeConstants{i in 1..n},  >= 0; #In this example we asume that charging speed is constant. 

param batCap, > 0, integer; #The max amount of energy the battery can hold. 

param points{i in 1..n, j in 1..m}; #List of all 1st coordinats.

param points2{i in 1..n, j in 1..m}; #List of all 2ed coordinats. 

param linesA{i in 1..n, j in 1..m}; #List of slopes.

param linesB{i in 1..n, j in 1..m}; #List of konstants, a function i is defined by lineA[i]*x[i]+lineB[i]. 


var x{i in 1..n, j in 1..m}, integer; #The optimal speed for each road segment.  

var z{i in 1..n, j in 1..m}, integer; #Used to ensure only one line segment is choosen. 

var y{i in 1..n}, integer, >= 0; #The optimal charging time at each charging station. 


minimize obj: sum{i in 1..n} y[i] + sum{i in 1..n, j in 1..m} -1*x[i,j]; #The objective function to be solved. 



s.t. OnlyOneLineSeg{i in 1..n}: sum{j in 1..m}(z[i,j]) == 1; 
s.t. ZmustBeBinary{i in 1..n, j in 1..m}: 0 <= z[i,j] <= 1;
s.t. XmustBeOnTheLine{i in 1..n, j in 1..m}: x[i,j] <= z[i,j]*points2[i,j];
s.t. XmustBeBetween{i in 1..n, j in 1..m}: x[i,j] >= z[i,j]*points[i,j];

s.t. battery{k in 1..n}: 0 <= sum{i in 1..k}(chargeConstants[i]*y[i]*0.1) - (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])/1000) <= batCap;

solve; 

display x;
display y;
display z; 

data;

param n := 8;
param m := 4;

param batCap := 40;

param edgeDist := 1 20, 2 22, 3 10, 4 8, 5 12, 6 25, 7 9, 8 15;

param chargeConstants := 1 0.6, 2 0.7, 3 0.4, 4 0.3, 5 0.8, 6 0.9,7 0.3,8 0.6; 

param points: 
	1	2	3	4  :=
1	40 	42	44	46
2	30	32	34	36
3	60	62	64	66
4	20	22	24	26
5	80	82	84	86
6	40	42	44	46
7	45	47	49	51
8	2	4	6	8;

param points2:
	1	2	3	4  :=
1	42	44	46	48
2	32	34	36	38
3	62	64	66	68
4	22	24	26	28
5	82	84	86	88
6	42	44	46	48
7	47	49	51	53
8	4	6	8	10; 

param linesA: 
   	1  	2  	3  	4  :=
1  	2.7548  2.8692  2.9836 	3.098
2 	2.1828 	2.2972 	2.4116 	2.526
3  	3.8988 	4.0132 	4.1276 	4.242
4  	1.6108 	1.7252 	1.8396 	1.954 
5  	5.0428 	5.1572 	5.2716 	5.386
6  	2.7548 	2.8692 	2.9836 	3.098
7  	3.0408 	3.1552 	3.2696 	3.384
8  	0.5812 	0.6956 	0.810 	0.9244; 

param linesB: 
	1  	2  	3  	4  :=
1	59.522 	54.7172	49.6836	44.4212
2	80.114 	76.4532 72.5636 68.4452
3	1.178 	-5.9148	-13.23	-20.7868
4	94.986 	92.4692	89.7236	86.7493
5	-80.046	-89.42	-99.03	-108.8748
6	59.522	54.7172	49.683	44.4212
7	47.081	41.7042	36.09	30.2642
8	107.34	106.88	106.19	105.282;
