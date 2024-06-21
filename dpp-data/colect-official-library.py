import git
import datetime, time
import shutil
import os


dir_path = "dpp-data/official-images/library"
dpp_list = open("dpp-data/dpp-official-images.csv", 'w')

for f in os.listdir(dir_path):
    file_path = os.path.join(dir_path, f)  #ファイル名取得
    dpp_list.write(f + ',')
    in_file = open(file_path, 'r')
    for line in in_file:
        if line.find("GitRepo:") >= 0: #GitHubURL情報の発見
            splited_line = line.split(" ")
            print(splited_line[1])
            dpp_list.write(splited_line[1].rstrip('\r\n') + ',')
    dpp_list.write("\n")
    in_file.close()
dpp_list.close()
