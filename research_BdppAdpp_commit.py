from git import *
import os
import datetime
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

def split_line(line):
    elements = line.split(",")
    elements[len(elements)-1] = elements[len(elements)-1].rstrip('\r\n')
    return elements

class Commit_checker:
    dfile = 0
    dpp = 0
    dpp_in_ten_dfile = []

    def __init__(self) -> None:
        pass
    def check_commit(self,item,project,dpp_data):
        file_commited = item.stats.files
        flag_dfile = False
        flag_dpp = False
        for file_name in file_commited :
            if is_dpp(project, file_name,dpp_data):
                self.dpp += 1
                if not flag_dpp: 
                    flag_dpp = not flag_dpp
            if is_dfile(file_name): 
                self.dfile += 1
                if not flag_dfile:
                    flag_dfile = not flag_dfile
                if self.dfile >= 10:
                    self.dpp_in_ten_dfile.append(self.dpp)
                    self.dpp = 0
                    self.dfile -= 10
        return [flag_dfile,flag_dpp]

def is_dfile(file_name):
    file_splited = file_name.split("/")
    if file_splited[len(file_splited) - 1] == "Dockerfile":
        return True
    else: 
        return False

def is_dpp(project, file_name,dpp_data):
    project_dpp = dpp_data[project]
    for dpp_name in project_dpp:
        if file_name.find(dpp_name) >= 0:
            return True
        else: 
            return False
    
def analyze_lines(item):
    file_list = item.stats.files
    insertion_list = []
    deletion_list = []
    for file_name in file_list:
        if is_dfile(file_name):
            insertion = file_list.get(file_name).get('insertions')
            deletion = file_list.get(file_name).get('deletions')
            lines = file_list.get(file_name).get('lines')
            insertion_list.append(insertion)
            deletion_list.append(deletion)
            print('inserted:%d deleted:%d changed:%d'%(insertion, deletion, lines))
    return insertion_list,deletion_list


def get_target_commit(repo,elements,dpp_data):
    count = [0,0]
    dfile_count = [0,0]
    dpp_count = [0,0]
    dpp_tmp = 0
    dfile_tmp = 0
    dpp_in_ten_dfile = []
    insertions_list = []
    deletions_list = []
    cc = Commit_checker()
    for item in repo.iter_commits("HEAD") :
        dt_tmp = datetime.datetime.fromtimestamp(item.committed_date)
        dt_dpp = datetime.datetime.strptime(elements[1], "%Y/%m/%d %H:%M:%S")        
        #before DPP
        if ((dt_dpp - datetime.timedelta(days=365)) < dt_tmp) and (dt_tmp < dt_dpp):
            count[0] += 1
            result = cc.check_commit(item,elements[0],dpp_data)
            if result[0] : dfile_count[0] += 1
            if result[1] : dpp_count[0] += 1
        #after DPP
        if (dt_dpp < dt_tmp) and (dt_tmp < (dt_dpp + datetime.timedelta(days=365))):
            count[1] += 1
            result = cc.check_commit(item,elements[0],dpp_data)
            if result[0]: 
                dfile_count[1] += 1
            if result[1]: 
                dpp_tmp += 1
                dpp_count[1] += 1
    
    return count,dfile_count,dpp_count,cc.dpp_in_ten_dfile  
        
def output_result(elements,count,outfile,dfile_count,dpp_count):
    outfile.write(elements[0]+','+str(count[0])+','+str(count[1])+','+str(dfile_count[0])+
                  ','+str(dfile_count[1])+','+str(dpp_count[0])+','+str(dpp_count[1])+'\n')
    

def search_commit(elements,outfile,dpp_data):
    if len(elements) > 2:    
        print("open " + "dpp-data/dpp-repos/" + elements[0])
        repo = Repo("dpp-data/dpp-repos/" + elements[0])
        count,dfile_count,dpp_count,dpp_in_ten_dfile = get_target_commit(repo,elements,dpp_data)

        print("Before dpp:" + str(count[0]))
        print("Before dpp dfile:" + str(dfile_count[0]))
        print("Before dpp dpp:" + str(dpp_count[0]))
        print("After dpp:" + str(count[1]))
        print("After dpp dfile:" + str(dfile_count[1]))
        print("After dpp dpp:" + str(dpp_count[1]))
        output_result(elements,count,outfile,dfile_count,dpp_count)
    return 

def search_after_before_DPP(line,outfile,dpp_data):
    elements = split_line(line)
    result = search_commit(elements,outfile,dpp_data)
    return result
    

def research(infile_name,outfile_name):
    dpp_data = {}
    #dpp_count = []  
    with open('dpp-filelist.csv','r') as dpp_list:
        csv_reader = csv.reader(dpp_list)
        for row in csv_reader:
            dppfiles = []
            project = row.pop(0)
            dpp_data[project] = []
            for filename in row:
                dpp_data[project].append(filename)
        
    #print(dpp_data)
    #result/commit_date_more1year.csv
    f = open(infile_name, 'r')
    outfile = open(outfile_name,'w')
    for line in f:
        #test+=1##
        #if test == 10 :break##
        search_after_before_DPP(line,outfile,dpp_data) 

    f.close()
    outfile.close()


if __name__ == "__main__":
    #research('commit_date.csv','result/RQ3.csv')
    research('result/commit_date_more1year.csv','result/RQ3_commit_only1year.csv')