param n, integer, > 0; #Number of nodes/edges in the path being tested, a path will always have the same amound of nodes and edges. 

param m, integer, > 0; #Number of linear lines used to model function f(x). 

param edgeDist{i in 1..n}, >= 0; #The length of each edge. edgeDist[1] is the length from s to e1 and edgeDist[n] from en-1 to t.

param chargeConstants{i in 1..n},  >= 0; #In this example we asume that charging speed is constant. 

param batCap, > 0, integer; #The max amount of energy the battery can hold. 

param points{i in 1..n, j in 1..m}; #List of all 1st coordinats.

param points2{i in 1..n, j in 1..m}; #List of all 2ed coordinats. 

param linesA{i in 1..n, j in 1..m}; #List of slopes.

param linesB{i in 1..n, j in 1..m}; #List of konstants, a function i is defined by lineA[i]*x[i]+lineB[i]. 

param speedDistanceRelation{i in 1..n,j in 1..2};

var x{i in 1..n, j in 1..m}; #The optimal speed for each road segment.  

var z{i in 1..n, j in 1..m}, integer; #Used to ensure only one line segment is choosen. 

var y{i in 1..n}, integer, >= 0; #The optimal charging time at each charging station. 


minimize obj: sum{i in 1..n} y[i] + (sum{i in 1..n} (speedDistanceRelation[i,1]*(sum{j in 1..m} x[i,j]) + speedDistanceRelation[i,2])); #The objective function to be solved. 



s.t. OnlyOneLineSeg{i in 1..n}: sum{j in 1..m}(z[i,j]) == 1; 
s.t. ZmustBeBinary{i in 1..n, j in 1..m}: 0 <= z[i,j] <= 1;
s.t. XmustBeOnTheLine{i in 1..n, j in 1..m}: x[i,j] <= z[i,j]*points2[i,j];
s.t. XmustBeBetween{i in 1..n, j in 1..m}: x[i,j] >= z[i,j]*points[i,j];

s.t. NoOverCharge{k in 1..n-1}: 0 <= sum{i in 1..k+1}(chargeConstants[i]*y[i]) - (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])*0.001) <= batCap;

#Todo fik all units to ensure that all mesures of energy have the exact same units and can be comparied. 
s.t. battery{k in 1..n}: 0 <= sum{i in 1..k}(chargeConstants[i]*y[i]) - (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])*0.001) <= batCap;
#s.t. roads{k in 1..n}: 0 <= (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])*0.001)-(sum{i in 1..k-1} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])*0.001) <= batCap;
solve; 


display y;
display z; 
display edgeDist;
display sum{i in 1..n} chargeConstants[i]*y[i];
display sum{i in 1..n} edgeDist[i];
display obj;
display x;

display{k in 1..n}: (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])*0.001)-(sum{i in 1..k-1} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])*0.001); 
display{k in 1..n}: k,  sum{i in 1..k}(chargeConstants[i]*y[i]) - (sum{i in 1..k} edgeDist[i]*(sum{j in 1..m}(linesA[i,j]*x[i,j]) + sum{j in 1..m} linesB[i,j]*z[i,j])*0.001);
data;

param n := 10;
param m := 14;

param batCap := 105;

param edgeDist := 1 50, 2 4, 3 41, 4 100, 5 5.2, 6 4, 7 209, 8 20, 9 30, 10 7;

param chargeConstants := 1 0.259989, 2 0, 3 0, 4 0, 5 2, 6 2, 7 0, 8 0, 9 0, 10 3.1; 

param speedDistanceRelation:
	1			2 :=
1 	-0.00728862973761 	0.204081632653
2 	-0.000583090379009 	0.0163265306122
3 	-0.00597667638484 	0.167346938776
4 	-0.0145772594752 	0.408163265306
5 	-0.000758017492711 	0.0212244897959
6 	-0.000583090379009 	0.0163265306122
7 	-0.0304664723032 	0.85306122449
8 	-0.00291545189504 	0.0816326530612
9 	-0.00437317784257 	0.122448979592
10 	-0.00102040816327 	0.0285714285714;

param points: 
	1	2	3	4	5	6	7	8	9	10	11	12	13	14  :=
1	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
2	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
3	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
4	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
5	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
6	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
7	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
8	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
9	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	
10	70.0	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0;	

param points2:
	1	2	3	4	5	6	7	8	9	10	11	12	13	14  :=
1	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
2	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
3	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
4	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
5	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
6	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
7	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
8	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
9	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0	
10	72.0	74.0	76.0	78.0	80.0	82.0	84.0	86.0	88.0	90.0	92.0	94.0	96.0	98.0;

param linesA: 
	1	2	3	4	5	6	7	8	9	10	11	12	13	14  :=
1	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
2	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
3	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
4	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
5	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
6	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
7	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
8	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
9	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96	
10	4.47	4.59	4.7	4.81	4.93	5.04	5.16	5.27	5.39	5.5	5.61	5.73	5.84	5.96;

param linesB: 
	1	2 	3 	4  	5	6	7	8	9	10	11	12	13	14  :=
1	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
2	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
3	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
4	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
5	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
6	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
7	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
8	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
9	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5	
10	-36.57	-44.81	-53.28	-61.97	-70.89	-80.05	-89.43	-99.04	-108.87	-118.94	-129.24	-139.76	-150.52	-161.5;