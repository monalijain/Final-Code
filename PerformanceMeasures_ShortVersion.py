__author__ = 'MJ'

import csv
def CalculatePerformanceMeasures(PriceSeries,Tradesheets,cost_of_trading,IndividualID,Begin,End):
    iFile=open("PerformanceMeasures.csv",'rb')
    rq=csv.reader(iFile)
    Performance_Measures=[]
    for row in rq:
        if(int(row[0])==IndividualID):
            Performance_Measures.append((float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7])))
            return Performance_Measures

        else:
            continue

    Performance_Measures.append((-50000,-50000, 0, -50000, -50000, 0, 0.0))
    return Performance_Measures

