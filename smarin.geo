Mesh.MshFileVersion = 2.2;
DefineConstant[
  Rext1 = {1, Min 0.5, Max 10, Step 0.1, Name "R1"},
  Rext2 = {1/2, Min 0.5, Max 10, Step 0.1, Name "R2"}
  h = {1/15, Min 0.01, Max 10, Step 0.01, Name "h"}
  Rint={1/4,Min 0.5,Max 2, Step 0.1,Name "Rint" }
];

L=Rint*4;

//arriere
Rarr=Rint/3;
xarr=L/2-Rarr;
yarr=0;
Point(22)={xarr,yarr,0,h};

Point(15)={xarr,yarr-Rarr,0,h};
Point(16)={xarr+Rarr,yarr, 0, h};
Point(1)={xarr,yarr+Rarr, 0, h};

//Aile haut
//Point 1
Point(2) ={xarr+Rarr/2,3*Rint/4, 0, h};
Point(3) ={xarr-Rarr/2,3*Rint/4, 0, h};
Point(4) ={xarr-Rarr,Rint/2, 0, h};

//aile bas
Point(12) = {xarr-Rarr,-Rint/2, 0, h};
Point(13) ={xarr-Rarr/2,-3*Rint/4, 0, h};
Point(14) ={xarr+Rarr/2,-3*Rint/4, 0, h};
//Point(15)

//haut sousmarin
Point(5)={L/10,Rint/2, 0, h};
Point(6)={0.5*L/10,Rint, 0, h};
Point(7)={-0.5*L/10,Rint, 0, h};
Point(8)={-L/10,Rint/2, 0, h};

//tete
rtete=Rint/2;
xtete=-L/2 + rtete;
ytete=0;

Point(910)={xtete,ytete, 0, h};
Point(9)={xtete,ytete+rtete, 0, h};
Point(10)={xtete-rtete,ytete,0, h};
Point(11)={xtete,ytete-rtete, 0, h};



//ellipse
Point(17)={0,0,0,h}; //centre
Point(18)={Rext2,0,0,h};

Point(19) = {0,-Rext2,0,h};
Point(20) = {-Rext2*2,0,0,h};
Point(21) = {0,Rext2,0,h};
Point(23) = {Rext2*2,0,0,h};

Ellipse(91) = {19,17,18,20};
Ellipse(92) = {20,17,18,21};
Ellipse(93) = {21,17,18,23};
Ellipse(94) = {23,17,18,19};

Line(12)={1,2};
Line(23)={2,3};
Line(34)={3,4};
Line(45)={4,5};

Line(56)={5,6};
Line(67)={6,7};
Line(78)={7,8};
Line(89)={8,9};

Circle(1)={9,910,10};
Circle(11)={10,910,11};

Line(1112)={11,12};
Line(1213)={12,13};
Line(1314)={13,14};
Line(1415)={14,15};

Circle(2)={15,22,16};
Circle(22)={16,22,1};

Line Loop(1) ={91,92,93,94};
Line Loop(2) = {12,23,34,45,56,67,78,89,1,11,1112,1213,1314,1415,2,22};

Plane Surface(1)={1,-2};
Physical Line(1)={91,92,93,94};
Physical Line(2)={12,23,34,45,56,67,78,89,1,11,1112,1213,1314,1415,2,22};
//Physical Surface(3) = {1};
