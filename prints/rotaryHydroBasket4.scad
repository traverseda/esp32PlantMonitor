m=1000;

module pie_slice(r=3.0,a=30) {
  intersection() {
    translate([0,-r/2])square(r);
    rotate(-a/2)square([r*2,r]);
    rotate(a/2-90)square([r,r*2]);
  }
}

outRad=0.41*m;
sideWall=0.4*4;
sharedWall=0.45*4;
floorWall=0.3*4;
height=70;
width=70;

segments=30;

drainageCutSize=5;
drainageCutHeight=4;

//For turning sharedWall into an arc-length measurement.
circumference=2*PI*outRad;
segmentArcLength=circumference/segments;
innerCut = 360/(circumference/(segmentArcLength-sharedWall*2));

module rail_segment(){
    intersection(){
        linear_extrude(height=20,center=true)pie_slice(r=0.4*m,a=12,$fn=100);
        rotate_extrude(angle = 360, convexity = 2,$fn=240) {
            translate([outRad-15,0,0]){
                difference(){
                    circle(d=8,$fn=6);
                    rotate([0,0,30])translate([-4,-5])square([4,10]);//Rail cutout
                }
            }
        }
    }
}

module slat(h=10,w=2){ //A slot that keeps modules aligned
    linear_extrude(height=w,center=true)hull(){
        circle($fn=6,r=sharedWall+1);
        translate([h,0])circle($fn=6,r=sharedWall+1);
    }
}

difference(){
    union(){ //body
        linear_extrude(height=width,center=true)pie_slice(r=outRad,a=360/segments,$fn=100);
        translate([0,0,width/2])rail_segment();
        mirror([0,0,1])translate([0,0,width/2])rail_segment();
        translate([0,0,width/2-20])rotate([0,0,360/segments/2])translate([outRad-height+15,0,0])slat();
        translate([0,0,-width/2+20])rotate([0,0,360/segments/2])translate([outRad-height+15,0,0])slat();


    }
    translate([0,0,width/2-20])rotate([0,0,-360/segments/2])translate([outRad-height+15,0,0])slat(w=2.2);
    translate([0,0,-width/2+20])rotate([0,0,-360/segments/2])translate([outRad-height+15,0,0])slat(w=2.2);
    
    //Determines height of pot
    linear_extrude(height=width+2,center=true)pie_slice(r=outRad-height,a=370/segments,$fn=100);
    //Cuts out inner hole
    linear_extrude(height=width-sideWall*2,center=true)pie_slice(r=outRad-floorWall,a=innerCut,$fn=100);
    difference(){
        for(i = [-2,-1,1,2]){//Bottom drainage holes
            translate([outRad,0,(height-sideWall*2-drainageCutSize)/4*i]){
                hull(){
                    rotate([90,0,0])cylinder(d=drainageCutSize,h=segmentArcLength+40,$fn=6, center=true);
                    translate([-drainageCutHeight,0,0])rotate([90,0,0])cylinder(d=drainageCutSize,h=segmentArcLength+40,$fn=6, center=true);
                }
        
            }
        }
        translate([outRad,0,0])cube([100,10,width+2],center=true);
    }
    //hex grid for side drainage
    rotate_extrude(angle = 360, convexity = 4,$fn=segments*2) {
        offs = (width-sideWall-8-2)/2;
        for(x = [-offs : offs/3 : offs]){
            translate([outRad-drainageCutHeight*3-2,x])circle(d=8,$fn=6);
        }
        for(x = [-offs+5 : offs/3 : offs]){
            translate([outRad-drainageCutHeight*3-8-1,x])circle(d=8,$fn=6);
        }
        for(x = [-offs : offs/3 : offs]){
            translate([outRad-drainageCutHeight*3-16-1,x])circle(d=8,$fn=6);
        }
        for(x = [-offs+5 : offs/3 : offs]){
            translate([outRad-drainageCutHeight*3-8*3-1,x])circle(d=8,$fn=6);
        }
    }
    difference(){//Card slot
        linear_extrude(height=width+2,center=true)pie_slice(r=outRad-height+5,a=innerCut,$fn=100);
        linear_extrude(height=width+4,center=true)pie_slice(r=outRad-height+3,a=innerCut+2,$fn=100);
    }
    translate([outRad-height+9,0,0])cube([2,segmentArcLength,20],center=true);//binder clip hole top
    translate([outRad-9,0,0])cube([2,segmentArcLength,20],center=true);//binder clip hole bottom
    rotate([0,0,(innerCut-innerCut/12)/2])linear_extrude(height=20,center=true)pie_slice(r=outRad+20,a=innerCut/12,$fn=100);
    rotate([0,0,-(innerCut-innerCut/12)/2])linear_extrude(height=20,center=true)pie_slice(r=outRad+20,a=innerCut/12,$fn=100);
}

module customSupport(){
    for(i = [-3 : 3]){
        translate([0,9*i,0])
        rotate([0,-90,0])rotate([0,0,45]){
            cylinder(d1=1.9,d2=0,h=1.4,$fn=4,center=true);
            cylinder(d1=0,d2=1.9,h=1.4,$fn=4,center=true);
        }
    }
    
}
translate([outRad-height+4,0,width/2-1])customSupport();
translate([outRad-height+4,0,-width/2+1])customSupport();


