from git import *
import os
import datetime
import pandas as pd
import csv
import re
import research_BdppAdpp_commit as rq3
import violin_plot as vp
import apply_man_whitney as mw

def analyze_lines(item):
    file_list = item.stats.files
    insertion_list = []
    deletion_list = []
    isdpp = False
    for file_name in file_list:
        if rq3.is_dfile(file_name):
            isdpp = True
            insertion = file_list.get(file_name).get('insertions')
            deletion = file_list.get(file_name).get('deletions')
            lines = file_list.get(file_name).get('lines')
            insertion_list.append(insertion)
            deletion_list.append(deletion)
            print('inserted:%d deleted:%d changed:%d'%(insertion, deletion, lines))
    return insertion_list,deletion_list,isdpp

def make_graph(insert_be, insert_af, delete_be, delete_af, name_list, filename,label):
    input_list_before = [insert_be, delete_be]
    input_list_after = [insert_af, delete_af]
    #vp.make_violin_graph(input_list_before,input_list_after,name_list,'esem-figure/violin/'+filename)
    vp.make_seaborn_violin_graph(input_list_before,input_list_after,name_list,filename,label,False)   
    return

def contain_bugfix(item,isdpp):
    message = item.message
    message = message.lower()
    return (("bug" in message) or ("fix" in message) or ("defects" in message) or ("close" in message) or ("resolve" in message)) and isdpp

def research(infile, outfile_name):
    outfile = open(outfile_name, 'w')
    with open(infile, 'r') as dpplist:
        csv_reader = csv.reader(dpplist)
        insertions_list_before = []
        deletions_list_before = []
        insertions_list_after = []
        deletions_list_after = []
        
        bugfix_rate_before = []
        bugfix_rate_after = []
        bugfix_list_before = []
        bugfix_list_after = []
    #test+=1##
    #if test == 10 :break##
        for elements in csv_reader:
            allcommit_before = 0
            allcommit_after = 0
            bugfix_before = 0
            bugfix_after = 0
            print("open " + "dpp-data/dpp-repos/" + elements[0])
            repo = Repo("dpp-data/dpp-repos/" + elements[0])
            for item in repo.iter_commits("HEAD") :
                dt_tmp = datetime.datetime.fromtimestamp(item.committed_date)
                dt_dpp = datetime.datetime.strptime(elements[1], "%Y/%m/%d %H:%M:%S")#"%Y/%m/%d %H:%M:%S" "%Y-%m-%d %H:%M:%S"
                

                #beforeDPP
                if ((dt_dpp - datetime.timedelta(days=365)) < dt_tmp) and (dt_tmp < dt_dpp):
                    
                    item_insertion_list,item_deletion_list,isdpp = analyze_lines(item)
                    for insert in item_insertion_list:
                        insertions_list_before.append(insert)
                    for delete in item_deletion_list:
                        deletions_list_before.append(delete)
                    
                    if isdpp: allcommit_before += 1
                    if contain_bugfix(item,isdpp):
                        allcommit_before += 1
                        bugfix_before += 1

                #afterDPP
                if (dt_dpp < dt_tmp) and (dt_tmp < (dt_dpp + datetime.timedelta(days=365))):
                    item_insertion_list,item_deletion_list,isdpp = analyze_lines(item)
                    for insert in item_insertion_list:
                        insertions_list_after.append(insert)
                    for delete in item_deletion_list:
                        deletions_list_after.append(delete)
                    if isdpp: allcommit_after += 1
                    if contain_bugfix(item,isdpp):
                        bugfix_after += 1


            if len(insertions_list_before) != 0:
                before_insert_mean = sum(insertions_list_before) / len(insertions_list_before)
            else: before_insert_mean = 0
            if allcommit_before > 0:
                bugfix_rate_before.append(bugfix_before/allcommit_before)
            if allcommit_after > 0:
                bugfix_rate_after.append(bugfix_after/allcommit_after)
            bugfix_list_before.append(bugfix_before)
            bugfix_list_after.append(bugfix_after)
            print("{0}:{1}".format(elements[0],before_insert_mean))
            print("bugfix before DPP:{} / {}".format(bugfix_before,allcommit_before))
            print("bugfix after DPP:{} / {}".format(bugfix_after,allcommit_after))
            outfile.write("{0},{1}\n".format(elements[0],before_insert_mean))

    outfile.close()
    print(bugfix_list_before)
    #make_graph(insertions_list_before, insertions_list_after, deletions_list_before, deletions_list_after, ['insert', 'delete'],'dfile_line_change.pdf',['before the adoption\nof DPP','after the adoption\nof DPP'])
    make_graph(bugfix_list_before, bugfix_list_after, bugfix_rate_before, bugfix_rate_after,['bugfix_commit_counts', 'bugfix_commit_rate'],'bugfix.pdf',['before the adoption\nof DPP','after the adoption\nof DPP'])
        
        


if __name__ == "__main__":

    research('result/commit_date_more1year.csv','result/commited_line_analysis.csv')#commit_date.csv