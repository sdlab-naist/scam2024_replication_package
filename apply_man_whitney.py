import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def manWhitney(dpp, nondpp):
    A = np.array(dpp)
    B = np.array(nondpp)
    result=stats.mannwhitneyu(A, B, alternative='two-sided')
    print('p-value:',result)
    return


class MakeData:
    dpp = []
    nondpp = []
    index = 0
    def __init__(self, dpp_list):
        dpp_list = dpp_list
    
    def makeData(self,mode,dpptype,index,dpp_list):
        
        for line in dpp_list:
            project = line.split(",")
            if mode == 0:
                if project[1].find("no") >= 0:
                    self.nondpp.append(float(project[index]))#ver:5,tag:6,arch:7
                else:
                    self.dpp.append(float(project[index]))
            else :
                self.nondpp.append(float(project[dpptype]))
                self.dpp.append(float(project[dpptype + 1]))

     
    def getDppData(self):
        return self.dpp
    def getNondppData(self):
        return self.nondpp

def make_plot(input_file):
    dpp_list = open(input_file, 'r')
    verdata = MakeData(dpp_list)

    verdata.makeData(1,1,3,dpp_list)
    nondppver = verdata.getNondppData()
    dppver = verdata.getDppData()
    print(dppver)
    print(nondppver)
    manWhitney(dppver,nondppver)

    points = [dppver, nondppver]
    fig, ax = plt.subplots()
    bp = ax.boxplot(points)

    #ax.set_xticklabels(['DPP', 'nonDPP'])
    ax.set_xticklabels(['DPP', 'nonDPP'])

    plt.ylabel('Number of commits')
    plt.grid()
    plt.savefig('esem-figure/rq1-commits-metrics.pdf')
    plt.show()


def main():
    make_plot('RQ1-all-dpp-metrics.csv',)
    #rq1:RQ1-all-dpp-metrics.csv   
    #rq3:RQ3-before-after-commit-incDfile.csv
    #RQ4-limited-project.csv


if __name__ == "__main__":
    main()