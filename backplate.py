from data_ingress import LugConfig,LoadCase
import math as m
import numpy as np

class BackplatePins:
    #pos_holes - 2D array storing x and z positions of the holes (in that respective order)
    def __init__(self, n: int,pos_holes):
        self.n=n
        self.pos_holes=pos_holes

    
    def compute_cg(self,lugconfig: LugConfig):
    #this method computes the x and z location of the cg of the backplate pin holes
        x_cg=0
        z_cg=0
        hole_area=((lugconfig.bolt_diameter)**2)*(m.pi*0.25)
        for i in range(len(self.pos_holes)):
            x_cg+=self.pos_holes[i][0]*hole_area
            z_cg+=self.pos_holes[i][1]*hole_area
        x_cg=x_cg/(self.n*hole_area)
        z_cg=z_cg/(self.n*hole_area)
        cg=[x_cg,z_cg]
        return cg
        
        
    def compute_xz_hole_force(self,cg,lugconfig: LugConfig,loadcase: LoadCase):
        #D is the denominator of the experssion, which is the sum of Ai*ri^2 for all holes
        #the x_prime and y_prime are coordinates of a given hole in the coord. centered at C.G.
        m_y_cg=-loadcase.force_x*cg[1]+loadcase.force_z*cg[0]
        xz_forces=[]
        D=0
        hole_area=((lugconfig.bolt_diameter)**2)*(m.pi*0.25)
        for i in range(len(self.pos_holes)):
            x_prime=self.pos_holes[i][0]-cg[0]
            z_prime=self.pos_holes[i][1]-cg[1]
            D+=hole_area*((x_prime**2)+(z_prime**2))
        for i in range(len(self.pos_holes)):
            x_prime=self.pos_holes[i][0]-cg[0]
            z_prime=self.pos_holes[i][1]-cg[1]
            alpha=np.arctan2(z_prime,x_prime)
            fx=(loadcase.force_x/self.n)+((m_y_cg*hole_area*m.sqrt(x_prime**2+z_prime**2))/D)*np.cos(alpha-m.pi/2)
            fz=(loadcase.force_z/self.n)+((m_y_cg*hole_area*m.sqrt(x_prime**2+z_prime**2))/D)*np.sin(alpha-m.pi/2)
            xz_forces.append([fx,fz])
        return xz_forces
    

    def compute_y_hole_force(self,cg,lugconfig: LugConfig,loadcase: LoadCase):
        y_forces=[]
        D=0
        hole_area=((lugconfig.bolt_diameter)**2)*(m.pi*0.25)
        for i in range(len(self.pos_holes)):
            x_prime=self.pos_holes[i][0]-cg[0]
            z_prime=self.pos_holes[i][1]-cg[1]
            D+=hole_area*((x_prime**2)+(z_prime**2))
        for i in range(len(self.pos_holes)):
            x_prime=self.pos_holes[i][0]-cg[0]
            z_prime=self.pos_holes[i][1]-cg[1]
            fy=(loadcase.force_y/self.n)+((loadcase.moment_z*np.sign(x_prime)*hole_area*m.sqrt(x_prime**2+z_prime**2))/D)
            y_forces.append(fy)
        return y_forces
    

    def pull_out_check(self,y_forces,thickness,bolt_diam,tau_allowable):
        for i in range(len(self.pos_holes)):
            tau=(y_forces[i]/(m.pi*bolt_diam*thickness))
            print("The pullout stress at hole: " + str(i) + " is "+ str(tau)+" and Von Mises stress is: " + str(m.sqrt(3*(tau**2))))
            if m.sqrt(3*(tau**2))>=0.9*tau_allowable:
                print("Pullout stress exceeded at hole: "+ str(i))



    def bearing_check(self,xz_forces,lugconfig: LugConfig,thickness,sigma_allowable):
        for i in range(len(self.pos_holes)):
            p=m.sqrt(xz_forces[i][0]**2+xz_forces[i][1]**2)
            sigma=p/(lugconfig.bolt_diameter*thickness)
            print("The bearing stress at hole: " + str(i) + " is "+ str(sigma))
            if abs(sigma)>=0.9*sigma_allowable:
                print("Bearing stress exceeded at hole: "+ str(i))




            
