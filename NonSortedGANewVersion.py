from PerformanceMeasures_ShortVersion import CalculatePerformanceMeasures
from MakeNewPopulationVersion2 import MakeNewPopulation #Change this to MakeNewPopulationVersion3 (if you want to make population in a different manner, as explained in the readme)
import csv
from datetime import datetime
from FastNonDominatedSort import FastNonDominatedSort

ParetoFront=csv.writer(open("ParetoFront.csv","wb"))
ParetoFront.writerow(["IndividualID","TrainingPeriod"])
ParetoFront.writerow(["","NetPL/Trades ratio","NetPL/Drawdown ratio","total_Gain", "total_DD", "NetPL", "TotalTrades", "ProfitMakingEpochs"])

C={}
D={}

#For checking the convergence of the Pareto Optimal Front
ParetoOptimalFront={}
MinimumGen=2 #Minimum Generations for which the program should run, provided those many individuals exist
CheckGen=3 #Number of generations for which the convergence will be checked
ConvergenceValue=0.01 #Value of NetPL/Total Trades

def NonSortedGA(Tradesheets,PriceSeries,MaxIndividualsInGen,TrainingBegin,TrainingEnd,ReportingBegin,ReportingEnd,CostOfTrading,MaxGen,MaxIndividuals):
    Pt={}
    print str(datetime.now()),"Current Time"
    
#Storing the initial seed individuals
    for num in range(1,MaxIndividualsInGen+1):
        PerfM=CalculatePerformanceMeasures("PriceSeries","Tradesheets",CostOfTrading,num,TrainingBegin,TrainingEnd)
        Pt[num]=[PerfM[0][0],PerfM[0][1],PerfM[0][2],PerfM[0][3],PerfM[0][4],PerfM[0][5],PerfM[0][6]]
        
    print "Initial seed individuals",Pt
	
#For each generation, divide population in different fronts, and Make New Population
    for gen in range(1,min(MaxGen,MaxIndividuals/MaxIndividualsInGen)):
        print str(datetime.now()),"Current Time of Generation: ",gen
        F=FastNonDominatedSort(Pt) #Create Fronts From Population
        print "Pareto Optimal Front of generation",gen-1,"is: ",F[1] #Print the first front
		
        ParetoFront.writerow([gen-1]) #Write the first front in paretofront file
        for key in F[1].keys():
            ParetoFront.writerow([key,F[1][key][0],F[1][key][1],F[1][key][2],F[1][key][3],F[1][key][4],F[1][key][5],F[1][key][6]])

        ParetoFront.writerow([])
        
        i=max(F.keys())
        lengOfFront1=len(F[1])
        Q=MakeNewPopulation(F,Pt,i,gen,MaxIndividualsInGen,lengOfFront1) #Make New Population (returns the indices of the child individuals
        Qt={}
        counter=0
		
#Calculate and store the performance measures of the child population
        for num in Q:
            PerfM=CalculatePerformanceMeasures("PriceSeries","Tradesheets",CostOfTrading,num,TrainingBegin,TrainingEnd)
            Qt[num]=[PerfM[0][0],PerfM[0][1],PerfM[0][2],PerfM[0][3],PerfM[0][4],PerfM[0][5],PerfM[0][6]]
            counter=counter+1

        print counter,"Number of children"
        Pt1=dict((F[1]).items()+Qt.items()) #Store the new population as, first front + child population

        if(CheckConvergenceOfPopulation(F,gen)==0): #Check for convergence 
            print "Converged" #Right Now do nothing , if converged
        Pt=Pt1
	
#Calculating NetPL and Total Trades for the last generation's Pareto Optimal Front
	
    F=FastNonDominatedSort(Pt)
    NetPL_CurrentGen=0.0
    TotalTrades_CurrentGen=0

    for individual in F[1].keys():
        NetPL_CurrentGen=float(F[1][individual][4])+NetPL_CurrentGen
        TotalTrades_CurrentGen=float(F[1][individual][5])+TotalTrades_CurrentGen

    C[gen]=[NetPL_CurrentGen/(1.0*TotalTrades_CurrentGen),TotalTrades_CurrentGen]
    print "NetPL/TotalTrades[gen=",gen,"]:",C[gen]

#Calculating NetPl and total trades for the entire last generation
    NetPLTotal=0.0
    TotalTrades=0
    kl=max(F.keys())
    for number in range(1,kl+1):
        for individual in F[number].keys():
            NetPLTotal=F[number][individual][4]+NetPLTotal
            TotalTrades=F[number][individual][5]+TotalTrades

    D[gen]=[NetPLTotal/(1.0*TotalTrades),TotalTrades]

    print "Pareto Optimal Front of generation",gen,"is: ",F[1]
    ParetoFront.writerow([gen])
    for key in F[1].keys():
        ParetoFront.writerow([key,F[1][key][0],F[1][key][1],F[1][key][2],F[1][key][3],F[1][key][4],F[1][key][5],F[1][key][6]])

    print "Performance Measure of evolved individuals in Training Period",Pt

    return [Pt,C,D]

#function to check convergence of the population
def CheckConvergenceOfPopulation(F,gen):
    NetPL_CurrentGen=0.0
    TotalTrades_CurrentGen=0
	
#Calculating NetPL and Drawdown for each generation's first front
    for individual in F[1].keys():
        NetPL_CurrentGen=float(F[1][individual][4])+NetPL_CurrentGen
        TotalTrades_CurrentGen=float(F[1][individual][5])+TotalTrades_CurrentGen

    C[gen-1]=[NetPL_CurrentGen/(1.0*TotalTrades_CurrentGen),TotalTrades_CurrentGen]
    print "NetPL/TotalTrades[gen=",gen-1,"]:",C[gen-1]
	
#Calculating NetPL and Dradown for entire generation
    NetPLTotal=0.0
    TotalTrades=0
    kl=max(F.keys())
    for number in range(1,kl+1):
        for individual in F[number].keys():
            NetPLTotal=F[number][individual][4]+NetPLTotal
            TotalTrades=F[number][individual][5]+TotalTrades

    D[gen-1]=[NetPLTotal/(1.0*TotalTrades),TotalTrades]
	
#If the generation==1 or the convergence criteria is not satisfied, then return 1, else return 0
	
    if(gen==1):
        return 1
    else:
        ParetoOptimalFront[gen]=abs(C[gen-1][0]-C[gen-2][0])

#print "ParetoOptimalFront[",gen,"]:",ParetoOptimalFront
    if(gen<max(CheckGen,MinimumGen)):
        return 1
    done=0
    for i in range(gen-CheckGen+1,gen+1):
        if(ParetoOptimalFront.has_key(i)):
            if(ParetoOptimalFront[i]<=ConvergenceValue):
                done+=1
    if(done==CheckGen):
        print("Converged algorithm in generation",gen)
        return 0

    return 1



#A=list()
#A=NonSortedGA("Tradesheets","PriceSeries",6,'20120622','20121109','20121112','20130111',0.0,2,12)
#print "Evolved individuals",A
#NonSortedGA(Tradesheets,PriceSeries,MaxIndividualsInGen,TrainingBegin,TrainingEnd,ReportingBegin, ReportingEnd, CostOfTrading,MaxGen,MaxIndividuals)
#print "total_Gain,total_DD,total_Profit_Long,total_Loss_Long,total_Win_Long_Trades,total_Loss_Long_Trades,total_Profit_Short,total_Loss_Short,total_Win_Short_Trades,total_Loss_Short_Trades"
