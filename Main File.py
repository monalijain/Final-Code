__author__ = 'MJ'

#This is the main file: Set num in range(n-1,n) for Walkforward n:

from WFList import CreateWFList
from NonSortedGANewVersion import *

[TBeginList,TendList,RBeginList,REndList]=CreateWFList("PriceSeries", 20, 10) #Creates Walkforward List

import csv
c=csv.writer(open("MYFILE.csv","wb"))
PLRatio=csv.writer(open("NetPLRatio.csv","wb"))

#WalkForward 3
#Set num in range(n-1,n) for WalkForward n
for num in range(2,3):
    c.writerow(["Walkforward",num+1,TBeginList[num],TendList[num],RBeginList[num],REndList[num]])
    print "Walkforward ",num+1
	
#5000: Number of Individuals in Each Generation
#MaxGen=Maximum Generations Possible
#MaxIndividuals= Maximum Number of Individuals Present in the tradesheet
	
    [A,C,D]=NonSortedGA("Tradesheets","PriceSeries",5000,TBeginList[num],TendList[num],RBeginList[num],REndList[num],CostOfTrading=0.0,MaxGen=6,MaxIndividuals=30000)
#A stores the performance measures of the final evolved individuals
#C stores the NetPL/Total Trades, and Total Trades of the Pareto Optimal Front Individuals of Each Generation
#D stores the NetPL/Total Trades and Total Trades of the entire generation
	
    c.writerow(["IndividualID","TrainingPeriod"])
    c.writerow(["","NetPL/Trades ratio","NetPL/Drawdown ratio","total_Gain", "total_DD", "NetPL", "TotalTrades", "ProfitMakingEpochs",""])
    PLRatio.writerow(["Walkforward",num+1,TBeginList[num],TendList[num],RBeginList[num],REndList[num]])

    for key in A.keys():
        c.writerow([key,A[key][0],A[key][1],A[key][2],A[key][3],A[key][4],A[key][5],A[key][6]])

    c.writerow([])

    for key in C.keys():
        PLRatio.writerow([key,C[key][0],C[key][1]])

    PLRatio.writerow([])

    for key in D.keys():
        PLRatio.writerow([key,D[key][0],D[key][1]])

    PLRatio.writerow([])




#print "Evolved individuals",A
#NonSortedGA(Tradesheets,PriceSeries,MaxIndividualsInGen,TrainingBegin,TrainingEnd,ReportingBegin, ReportingEnd, CostOfTrading,MaxGen,MaxIndividuals)
#print "total_Gain,total_DD,total_Profit_Long,total_Loss_Long,total_Win_Long_Trades,total_Loss_Long_Trades,total_Profit_Short,total_Loss_Short,total_Win_Short_Trades,total_Loss_Short_Trades"



