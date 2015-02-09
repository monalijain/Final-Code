from WFList import CreateWFList
import datetime
import csv

#This file calculates and stores Performance Measures of Individuals for a certain Walkforward (set num=n-1, where n is the walkfoward)

cost_of_trading=0.0
num=1 # For Third Walkforward
NumberOfIndividuals=30000 #Stores the Number of Individuals in Tradesheet File
NumberOfRows=89596579 #Stores the number of Rows in Tradesheet File

writePerf=csv.writer(open("PerformanceMeasures.csv","wb"))

[TBeginList,TendList,RBeginList,REndList]=CreateWFList("PriceSeries", 20, 10) #Creates Walkforward List
Begin=TBeginList[num]
End=TendList[num]


BeginDate=datetime.datetime.strptime(Begin,"%Y%m%d")
EndDate=datetime.datetime.strptime(End,"%Y%m%d")
iFile=open("PriceSeries.csv",'rb')
rq=csv.reader(iFile)
c=0
DictOfDates={}
date_count_range=1
for row in rq:
    CurrentDate=datetime.datetime.strptime(row[0],"%Y%m%d")
    if(c==0):
        DictOfDates[CurrentDate.date()]=date_count_range-1
    else:
        if(row1[0]!=row[0] and CurrentDate.date()>=BeginDate.date() and CurrentDate.date()<=EndDate.date()):
            date_count_range=date_count_range+1
            DictOfDates[CurrentDate.date()]=date_count_range-1
    row1=row
    c=c+1

#Calculation of Performance Measures
TFile=open("Tradesheets.csv",'rb')
rT=csv.reader(TFile)

trade=next(rT)
count=1
for IndividualID in range(0,NumberOfIndividuals):
    print( IndividualID )
    Performance_Measures=[]                    #List of Tuples to store the Performance_Measures the calculation_type
    #Lists to store the variables for daily calculations
    tmp_daily_running_pl=[]

    #Variables for the total period of between begin date and end date
    total_Win_Long_Trades=0
    total_Win_Short_Trades=0
    total_Loss_Long_Trades=0
    total_Loss_Short_Trades=0
    total_Profit_Long=0
    total_Profit_Short=0
    total_Loss_Long=0
    total_Loss_Short=0

    #Creating a list which stores daily PL values
    for filler_date_count in range(date_count_range):
        tmp_daily_running_pl.append(0)

    date_count=0
    diff=0
    DD_History = []          #List to store the DD values.
    Gain_History = []        #List to store the MaxGain values
    IndividualIDExist=0      #Variable to see whether the individual has not been traded at all

    while(int(trade[1])==IndividualID):
        CurrentDate=datetime.datetime.strptime(trade[3],"%Y-%m-%d")
        dateinrange=CurrentDate.date()<=EndDate.date() and CurrentDate.date()>=BeginDate.date()
        if(dateinrange):
            if(diff==0):
                if(DictOfDates.has_key(CurrentDate.date())):
                        date_count= DictOfDates[CurrentDate.date()]
            else:
                if(trade1[3]!=trade[3]):
                    if(DictOfDates.has_key(CurrentDate.date())):
                        date_count= DictOfDates[CurrentDate.date()]


            if (int(trade[1]) == IndividualID):
                IndividualIDExist=IndividualIDExist+1
                trade_entry_price = int(float(trade[5]))
                trade_qty = int(float(trade[6]))
                trade_type = int(float(trade[2]))
                trade_exit_price = int(float(trade[9]))

                #Trade type 0=FALSE is short and 1=TRUE is long
                if(trade_type==1):
                    trade_pl = ((trade_exit_price - trade_entry_price)-(trade_exit_price+trade_entry_price)*cost_of_trading)*trade_qty
                    if(trade_pl>0):
                        total_Win_Long_Trades+=1
                        total_Profit_Long+=trade_pl
                    else:
                        total_Loss_Long_Trades+=1
                        total_Loss_Long+=trade_pl
                else:
                    trade_pl = ((trade_entry_price - trade_exit_price)-(trade_exit_price+trade_entry_price)*cost_of_trading)*trade_qty
                    if(trade_pl>0):
                        total_Win_Short_Trades+=1
                        total_Profit_Short+=trade_pl
                    else:
                        total_Loss_Short_Trades+=1
                        total_Loss_Short+=trade_pl

                tmp_daily_running_pl[date_count] = tmp_daily_running_pl[date_count]+trade_pl

        diff=1
        trade1=trade
        if(count<NumberOfRows):
            trade=next(rT)
            count=count+1
        else:
           break

    #if the individual has not been traded at all, then make all the performance measures 0 or negative, and return from this function
    if(IndividualIDExist==0):
        Performance_Measures.append((-50000,-50000, 0, -50000, -50000, 0, 0.0))

    else:
        #calculation of DD:
        if(tmp_daily_running_pl[0] < 0):
            DD_History.append(tmp_daily_running_pl[0])
        else:
            DD_History.append(0)

        DD_date_count = 1
        while(DD_date_count < date_count_range):
            if(tmp_daily_running_pl[DD_date_count]<0):
                DD_History.append(DD_History[DD_date_count-1]+tmp_daily_running_pl[DD_date_count])
            else:
                DD_History.append(0)
            DD_date_count = DD_date_count +1

        total_DD=0
        for DD_Daily_Value in DD_History:
            if(DD_Daily_Value<total_DD):
                total_DD=DD_Daily_Value

        #if the individual (trade) is not feasible  i.e. Total Trades or the drawdown is 0 , that means its not feasible
        TotalTrades= total_Win_Short_Trades+total_Loss_Short_Trades+total_Win_Long_Trades+total_Loss_Long_Trades

        if(TotalTrades==0 or total_DD==0):
            Performance_Measures.append((-50000,-50000, 0, -50000, -50000, 0, 0.0))
        else:
        #calculation of MaxGain (Similar to DD Calculation):
            if(tmp_daily_running_pl[0]>0):
                Gain_History.append(tmp_daily_running_pl[0])
            else:
                Gain_History.append(0)

            Gain_date_count=1
            while(Gain_date_count <date_count_range):
                if(tmp_daily_running_pl[Gain_date_count]>0):
                    Gain_History.append(Gain_History[Gain_date_count-1]+tmp_daily_running_pl[Gain_date_count])
                else:
                    Gain_History.append(0)
                Gain_date_count+=1

            total_Gain=0.0
            for Gain_Daily_Value in Gain_History:
                if(Gain_Daily_Value>total_Gain):
                    total_Gain=Gain_Daily_Value

            NetPL=total_Profit_Long+total_Loss_Long+total_Profit_Short+total_Loss_Short
            ProfitMakingEpochs=1.0*(total_Win_Long_Trades+total_Win_Short_Trades)/(1.0*(TotalTrades))
            Performance_Measures.append((NetPL/(TotalTrades), NetPL/(-total_DD), total_Gain, total_DD, NetPL, TotalTrades, ProfitMakingEpochs))

    writePerf.writerow([IndividualID,Performance_Measures[0][0],Performance_Measures[0][1],Performance_Measures[0][2],Performance_Measures[0][3],Performance_Measures[0][4],Performance_Measures[0][5],Performance_Measures[0][6]])
