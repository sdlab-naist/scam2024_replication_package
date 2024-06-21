from git import *
import datetime, time
import csv
import os
import re
import matplotlib.pyplot as plt

def make_graph(list):
   bp = plt.boxplot(list)
   plt.grid()
   plt.ylabel('Days',fontsize=16)
   plt.xticks([])
   plt.tick_params(labelsize=16)
   plt.tight_layout()
   plt.savefig('esem-figure/RQ1-dpp-timing.pdf')
   os.system('pdfcrop esem-figure/RQ1-dpp-timing.pdf')
   plt.show()

def check_oldest(repo):
   date_list = []
   for item in repo.iter_commits("HEAD"):
      date_list.append(datetime.datetime.fromtimestamp(item.committed_date))
   date_list.sort()
   return date_list[0]

def check_dpp_timing():
   outfile = open('commit_date.csv', 'w')
   oneyear_file = open('result/commit_date_more1year.csv', 'w')

   lag_list = []
   commit_count_list = []

   with open("dpp-filelist.csv", 'r', newline='', encoding='utf-8') as dpp_list:
       csv_reader = csv.reader(dpp_list)

       for row in csv_reader:
         project = row.pop(0)
         git_path = "./dpp-data/dpp-repos/" + project
         print(git_path)
         if os.path.isdir(git_path):
            repo = Repo(git_path)
            dpp_datelist = []
            for filename in row:      
               blame = repo.git.blame('--date=format-local:@@%Y/%m/%d %H:%M:%S@@',filename)
               blame_list = blame.split('\n')

               for commit_info in blame_list:
                  commit_list = commit_info.split('@@')

                  dpp_datelist.append(commit_list[1])
            dpp_datelist.sort()
            #print("{0}:{1}".format(project,dpp_datelist))
            if dpp_datelist != []:
               oldest = check_oldest(repo)
               dppoldest = datetime.datetime.strptime(dpp_datelist[0], "%Y/%m/%d %H:%M:%S")

               lag = dppoldest - oldest
               lag_list.append(float(lag.days))
               print("{0},{1},{2}\n".format(project,dpp_datelist[0],lag))           
               outfile.write("{0},{1},{2}\n".format(project,dpp_datelist[0],lag))
               if lag >= datetime.timedelta(days=365):
                  hash_list = commit_list[0].split(" ")
                  oneyear_file.write("{0},{1},{2}\n".format(project,dpp_datelist[0],lag))
   return lag_list




#plt.hist(lag_list,bins=20) 
#plt.show()
#plt.savefig("figure/dpp-date.png")
def main():
   lag_list = check_dpp_timing()
   #make_graph(lag_list)

if __name__ == '__main__':
    main() 
