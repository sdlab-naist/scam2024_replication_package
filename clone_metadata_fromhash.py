from git import *
import shutil
import os

def clone_meta_file(repo,index,path,elements):
    filename = "library/" + elements[0]
    repo.git.checkout(elements[index],"--",filename)
    shutil.copy(filename,path)
    repo.git.checkout("master", "--", filename)



def init(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)

def main():

    dir_path = "./dpp-data/official-images"
    dpp_timing_path = "./dpp-metadata-past"
    past_path = "../../dpp-metadata-past-remake"
    before_path = "../../dpp-metadata-before-remake"
    after_path = "../../dpp-metadata-after-remake"

    init("./dpp-metadata-past-remake")
    init("./dpp-metadata-before-remake")
    init("./dpp-metadata-after-remake")
    repo = Repo(dir_path)

    infile = open("./dpp_rq2_threehex.csv",'r')

    os.chdir("dpp-data/official-images")

    for line in infile:
        elements = line.split(",")
        elements[-1] = elements[-1].rstrip('\r\n')
        print(elements)
        if elements[1] != elements[2] and elements[2] != elements[3] and elements[3] != elements[0]:
            clone_meta_file(repo,1,past_path,elements)
            clone_meta_file(repo,2,before_path,elements)
            clone_meta_file(repo,3,after_path,elements)
        
        #clone_meta_file(1,dpp_timing_path,elements)

    infile.close()
    os.chdir("..")
    os.chdir("..")

if __name__ == '__main__':
    main()