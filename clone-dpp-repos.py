import git
import datetime, time
import shutil
import csv
import os

def main():
  in_file = open('dpp-data/dpp-official-images.csv', 'r')

  files = os.listdir("dpp-data/dpp-repos")
  files_dir = [fi for fi in files if os.path.isdir(os.path.join("dpp-data/dpp-repos", fi))]

  #for dir in files_dir:
  #  repopath = "dpp-data/dpp-repos/" + dir
  #  shutil.rmtree(repopath)
    
  #i = 1
  #1行とってセル毎にリスト
  csv_reader = csv.reader(in_file)
  for dppdata in csv_reader:
    
    repopath = "dpp-data/dpp-repos/" + dppdata[0]#str(i)
    if os.path.exists(repopath):
      shutil.rmtree(repopath)
    if len(dppdata) > 0 and dppdata[1] != "":
      url = dppdata[1]
      
      if dppdata[0] != "ubuntu":
        print(url + " is cloned...")
        git.Repo.clone_from(url, repopath)
      #i += 1
    

  in_file.close()

if __name__ == '__main__':
    main()