import os



def count_oldversion_release(file_list):
    count = 0
    flag = True
    for line in file_list:
        print(line)
        if line.find("github.com") >= 0 and flag:
            flag = False            
        if line == '\n' and (not flag):
            count += 1
            flag = True
    if not flag: count += 1
    return count


def collect_metrics(dir_path,save_file):
    dpp_list = open(save_file, 'w')#dpp-prj-character.csv
    tag_list = []
    ver_list = []
    arch_list = []
    for f in os.listdir(dir_path):
        tag_count = 0
        ver_count = 0
        arch_count = 0
        arch_line_count = 0
        tag = []
        arch = []
        metafile_list = []

        file_path = os.path.join(dir_path, f)
        in_file = open(file_path, 'r')
        for line in in_file:
            metafile_list.append(line)
            if line.find("Tags:") == 0:
                print(line)
                ver_count += 1
                splited_line = line.split(",")
                tag_count = len(splited_line)
                tag.append(tag_count)
            if line.find("Architectures:") >= 0:
                arch_line_count += 1
                splited_line = line.split(",")
                arch_count = len(splited_line)
                arch.append(arch_count)
        
        
        if len(tag) > 0:
            tag.sort()
        else:
            tag.append(1)
            ver_count = count_oldversion_release(metafile_list)
        if len(arch) > 0:
            arch.sort()
        else:
            arch.append(1)
        
        print(str(tag[-1])+ " " + str(ver_count))
        dpp_list.write("{0},{1},{2},{3}".format(f,tag[-1],ver_count,arch[-1]))
        
        dpp_list.write("\n")
        tag_list.append(tag[-1])
        ver_list.append(ver_count)
        arch_list.append(arch[-1])
        in_file.close()

    dpp_list.close()
    return tag_list, ver_list, arch_list

def main():

    dpp_data_path = './dpp-data/official-images/library'
    dpp_past_path = 'dpp-metadata-past'
    dpp_dir_path = "dpp-metadata-past-remake"
    before_dir_path = "dpp-metadata-before-remake"
    after_dir_path = "dpp-metadata-after-remake"

    #collect_metrics(dpp_data_path,'result/all-dpp-metrics.csv')
    #collect_metrics(dpp_past_path,'result/rq1_dpp_timing_met.csv')

    #DPP timing
    dpp_tag, dpp_ver, dpp_arch = collect_metrics(dpp_dir_path,'./result/RQ3-dpp-timing-met-re.csv')

    #before DPP
    before_tag, before_ver, before_arch = collect_metrics(before_dir_path,'./result/RQ3-dpp-before-met-re.csv')

    #after DPP
    after_tag, after_ver, after_arch = collect_metrics(after_dir_path,'./result/RQ3-dpp-after-met-re.csv')

    with open('result/met_evolution.csv','w') as savefile:
        
        for i in range(len(dpp_tag)):
            before_tag_evo = dpp_tag[i] - before_tag[i]
            after_tag_evo = after_tag[i] - dpp_tag[i]
            before_ver_evo = dpp_ver[i] - before_ver[i]
            after_ver_evo = after_ver[i] - dpp_ver[i]
            before_arch_evo = dpp_arch[i] - before_arch[i]
            after_arch_evo = after_arch[i] - dpp_arch[i]
            print(("%d,%d,%d,%d,%d,%d\n"%(before_tag_evo,after_tag_evo,before_ver_evo,after_ver_evo,before_arch_evo,after_arch_evo)))
            savefile.write("%d,%d,%d,%d,%d,%d\n"%(before_tag_evo,after_tag_evo,before_ver_evo,after_ver_evo,before_arch_evo,after_arch_evo))


if __name__ == '__main__':
    main()