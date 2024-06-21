from git import *
import datetime 
import time
import shutil
import os

def search_in_repo(project,date,repo):
    flag = False
    dpp_datelist = []
    hash_list = []

    #print(project)
    blame = repo.git.blame('--date=format-local:@@%Y/%m/%d %H:%M:%S@@',"library/"+project)
    #print(blame)
    blame_list = blame.split('\n')
    

    for commit_item in blame_list:
        commit_list = commit_item.split('@@')
        #print(filename + "\n" + commit_list[1])
        hash_author = commit_list[0].split(' ')
        hash_list.append(hash_author[0])
        dpp_datelist.append(commit_list[1])
        dpp_datelist.sort()
    

    for i in range(len(dpp_datelist)):
        dt_tmp = datetime.datetime.strptime(dpp_datelist[i], "%Y/%m/%d %H:%M:%S")
        if (not flag):
            lag = date - dt_tmp 
            flag = True
            commit_index = i
        else:
            tmplag = date - dt_tmp
            if (tmplag > datetime.timedelta(days=0,hours=0,weeks=0,minutes=0) and abs(lag) > abs(tmplag)):
                lag = tmplag
                commit_index = i
    print(project +','+ dpp_datelist[commit_index] +','+str(lag))
    return hash_list[commit_index]


def search_nearest_commit(project,date,dir_path,output):
    repo = Repo(dir_path)
    print('{0}: {1}'.format(project,date))
    hash = search_in_repo(project,date,repo)

    #beforeDPP
    beforedate = date - datetime.timedelta(days=365)
    before_hash = search_in_repo(project,beforedate,repo)

    #afterDPP
    afterdate = date + datetime.timedelta(days=365)
    after_hash = search_in_repo(project,afterdate,repo)
   
    output.write('{0},{1},{2},{3}\n'.format(project,hash,before_hash,after_hash))

    #if (hash != after_hash) and (hash != before_hash) and (before_hash != after_hash):

def main():       
    dir_path = "./dpp-data/official-images"
    output = open('./dpp_rq2_threehex.csv','w')

    with open("commit_date.csv", 'r', newline='', encoding='utf-8') as date_list:
        for line in date_list:
            splited_line = line.split(",")
            date_string = splited_line[1]
            date = datetime.datetime.strptime(date_string, "%Y/%m/%d %H:%M:%S")
            #print(str(date))
            search_nearest_commit(splited_line[0],date,dir_path,output)

    output.close()

if __name__ == '__main__':
    main()



