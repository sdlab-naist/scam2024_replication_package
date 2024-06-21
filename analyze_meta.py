from git import *
import datetime 
import time
import shutil
import os
import csv
import violin_plot as vp

def make_date_list():
    date_list = []
    with open('commit_date.csv','r') as dpplist:
        csv_reader = csv.reader(dpplist)
        for line in csv_reader:
            dpp = []
            dpp.append(line[0])
            dpp.append(line[1])
            date_list.append(dpp)
    return date_list

def get_commit(project,b_date,a_date):
    dir_path = 'dpp-data/official-images'
    repo = Repo(dir_path) 
    log = repo.git.log('-p','--after=' + b_date.strftime("%Y/%m/%d %H:%M:%S"),'--before='+a_date.strftime("%Y/%m/%d %H:%M:%S"),'--date=format-local:%Y/%m/%d %H:%M:%S',"library/"+project)
    #print(log)
    logs = log.split('\n')
    print('{0} ~ {1}'.format(b_date,a_date))
    return logs

def analyze_line(line,key):#[Tag, Release, Arch]
    
    return (line.find(key) >= 0)


def analyze_logs(logs):#[release_in,release_de]
    delete = 0
    insert = 0
    in_hash = ''
    de_hash = ''
    for log in logs:
        if log.find('-') == 0 and log.find("---") < 0:
            if analyze_line(log,"Tags:"): delete += 1
            else:
                splited_log = log.split('@')
                hash = splited_log[-1].split(' ')
                if analyze_line(log,"git:") and hash[0] != de_hash:
                    delete += 1
                    de_hash = hash[0]
        if log.find('+') == 0 and log.find("+++") < 0:
            if analyze_line(log,"Tags:"): insert += 1
            else:
                splited_log = log.split('@')
                hash = splited_log[-1].split(' ')
                if analyze_line(log,"git:") and hash[0] != in_hash:
                    insert += 1
                    in_hash = hash[0]
                    print(in_hash)
    return [insert,delete]

def search_date(project,list):
    for i in range(len(list)):
        if list[i][0] == project:
            return datetime.datetime.strptime(list[i][1], "%Y/%m/%d %H:%M:%S")

def research_beforeafter_dpp():
    date_list = make_date_list()
    with open('result/meta_line_change.csv', 'w') as savefile:

        with open('result/RQ3-dpp-timing-met-re.csv','r') as dpplist:
            csv_reader = csv.reader(dpplist)
            for list in csv_reader:
                project = list.pop(0)
                date = search_date(project,date_list)
                before_date = date - datetime.timedelta(days=365)
                after_date = date + datetime.timedelta(days=365)

                logs = get_commit(project,before_date,date)
                result_b = analyze_logs(logs)

                logs = get_commit(project,date,after_date)
                result_a = analyze_logs(logs)
                print("{0},{1},{2}".format(project,result_b,result_a))
                #before[in,de], after[in,de]
                savefile.write("{0},{1},{2},{3},{4}\n".format(project,result_b[0],result_b[1],result_a[0],result_a[1]))

def research_dpp_vs_nondpp():
    date_list = make_date_list()
    with open('result/meta_line_change_nondpp.csv', 'w') as savefile:

        with open('RQ1-all-dpp-metrics.csv','r') as dpplist:
            csv_reader = csv.reader(dpplist)
            data_insert_nondpp = []
            data_delete_nondpp = []
            data_insert_dpp = []
            data_delete_dpp = []
            for list in csv_reader:
                project = list.pop(0)
                after_date = dt_now = datetime.datetime.now()
                before_date = after_date - datetime.timedelta(days=365)

                if list[0] == 'no':
                    logs = get_commit(project,before_date,after_date)
                    result_nondpp = analyze_logs(logs)
                    data_insert_nondpp.append(result_nondpp[0])
                    data_delete_nondpp.append(result_nondpp[1])
                    print("{0},{1}".format(project,result_nondpp))
                    savefile.write("{0},{1},{2}\n".format(project,result_nondpp[0],result_nondpp[1]))
                else:
                    logs = get_commit(project,before_date,after_date)
                    result_dpp = analyze_logs(logs)
                    data_insert_dpp.append(result_dpp[0])
                    data_delete_dpp.append(result_dpp[1])
                    print("{0},{1}".format(project,result_dpp))
                    savefile.write("{0},{1},{2}\n".format(project,result_dpp[0],result_dpp[1]))
                    #before[in,de], after[in,de]
            vp.make_seaborn_violin_graph([data_insert_nondpp,data_delete_nondpp], [data_insert_dpp,data_delete_dpp], ['Release','End_of_support'], 'rq1_meta_change.pdf', ['non-DPP', 'DPP'], True)
                


def main():
    research_beforeafter_dpp()
    #research_dpp_vs_nondpp()
    

if __name__ == '__main__':
    main()