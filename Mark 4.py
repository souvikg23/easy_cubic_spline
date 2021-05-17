# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 21:43:29 2021

@author: SOUVIK
"""
#Any X,Y input 
import matplotlib.pyplot as plt

import numpy as np
from numpy import zeros
#Taking Input as a set of 2 numbers (t,x)


n= int(input("enter no of data points :"))
ele =zeros([n-2,n-2])


#This is for manual input
'''data=[]
print("please input the data as indepenent var. [SPACE] dependent var.")
for i in range (0,n):
    dot = [float(x) for x in input("enter t x:").split()]
    data.append(dot)
print()
print    ("entered data is", (data))'''

#This is for taking inputs from Excel files

import xlrd
import openpyxl
import xlsxwriter
import xlwt
location = "E:\\to sir\\Sacroiliac Joint Arthralgia Group Hip Angles after treatment.xlsx"
wb = xlrd.open_workbook(location)
sheet = wb.sheet_by_index(0)
for j in range (2,17):
    data=[]
    for i in range (1,n+1):
        dot=[float(sheet.cell_value(17, i)), float(sheet.cell_value(j, i))]
        data.append(dot)
    #print    ("entered data is", (data))

    h=[]
    for i in range (1,n,1):
        L=(data[i][0]-data[i-1][0])
        L=float(L)
        h.append(L)


#print("list of differences",h)




    for i in range (1,n-2):
    
    
    
        ele[i][i-1]= h[i]
        kk=h[i-1]+h[i]
        ele[i-1][i-1]=2*kk
        ele[i-1][i]=h[i]
  

    ele[n-3][n-3]=2*((h[n-3])+(h[n-2]))
    print()
    #print("co-efficient matrix is",(ele))
    R=zeros([n-2,1])

#print ("value of rhs matrix before assigning the cell values",(R))

    for i in range (1,n-1,1):
        R[i-1][0]=6*((data[i+1][1]-data[i][1])/h[1]-(data[i][1]-data[i-1][1])/h[0])




#print ("final R =",(R))

    inv_ele = np.linalg.inv(ele)

#print()
#print ("inverse of co-eff matrix =", inv_ele)


    K=np.dot(inv_ele,R)

#print ("matrix of spline second dervatives without first and last ones=", K)

    M=zeros([n,1])
    for i in range(1,n-1):
        M[i][0]=K[i-1][0]
    print()
    #print ("matrix of spline ssds =", M)

#x=data[0][1]
    '''print ("so the spline functions are listed below : -")
    for i in range (1,n):
    
        print()
        print ("S",i,"=",1/h[i-1],"[","1/6","(",data[i][0],"- t)^3 * (",M[i-1][0],") +1/6 *(x-",data[i-1][0],")^3 * (",M[i][0],")")
                                                                                                                       
        print ("+(",(data[i-1][1]-(h[i-1]*h[i-1]*M[i-1][0]/6)),")*(",data[i][0],"- t)","+",(data[i][1]-(h[0]*h[0]*M[i][0]/6)),"*(t -",data[i-1][0],")]")
        print()
        print ("S",i,"is for:",data[i-1][0],"<","x","<",data[i][0])
        #empty prints are for proviing space between loop outputs of first 2 prints
        print()
        print()'''

    i=0
    t=data[i][0]
    for i in range (1,n)  : 
        plt.plot(data[i][0],data[i][1],marker=".",markersize=25,color='red')
        plt.plot(data[0][0],data[0][1],marker=".",markersize=25,color='red')
        while data[i][0]> t >= data[i-1][0] :
        
   
         
       
          
                sp1= 1/6*(data[i][0]- t)**3 * M[i-1][0]
                sp2= 1/6 *(t-data[i-1][0])**3 * M[i][0]
                sp31=data[i-1][1]- h[i-1]*h[i-1]*M[i-1][0]/6 
                sp32=data[i][0]- t
                sp41=data[i][1]-h[i-1]*h[i-1]*M[i][0]/6
                sp42=t -data[i-1][0]
                sp3=sp31*sp32
                sp4=sp41*sp42
                sp5=sp1+sp2+sp3+sp4
                sp=sp5 * 1/h[i-1]
                plt.title(j-1)
                plt.xlabel('% GAIT')
                plt.ylabel('Joint angle')
                plt.plot(t,sp,marker=".",markersize=5,color='blue')
               
            
            
            
                t=t+0.02
    plt.show()
        
# NOw to calculate derivatives at each point

    from sympy import Symbol, Derivative

    t = Symbol('t')
    AV =[]
    for i in range (1,n):

        sp11= 1/6*(data[i][0]- t)**3 * M[i-1][0]
        sp21= 1/6 *(t-data[i-1][0])**3 * M[i][0]
        sp31a=data[i-1][1]- h[i-1]*h[i-1]*M[i-1][0]/6 
        sp32a=data[i][0]- t
        sp41a=data[i][1]-h[i-1]*h[i-1]*M[i][0]/6
        sp42a=t -data[i-1][0]
        sp31=sp31a*sp32a
        sp41=sp41a*sp42a
        sp51=sp11+sp21+sp31+sp41
        sp01=sp51 * 1/h[i-1]


        deriv= Derivative(sp01, t)

    
    

  

        k= deriv.doit().subs({t:data[i-1][0]})
        AV.append(k)
        print (k)
    k1 = deriv.doit().subs({t:data[n-1][0]})
    AV.append(k1)
    print ( k1)
    print ("the anguler velocities of patient", j-1, "are above")
