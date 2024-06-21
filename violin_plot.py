import plotly.graph_objects as go
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import apply_man_whitney as mw
import os

def make_data(file):
    tag_list = []
    release_list = []
    arch_list = []
    csv_reader = csv.reader(file)

    for line in csv_reader:
       tag_list.append(int(line[1]))
       release_list.append(int(line[2]))
       arch_list.append(int(line[3]))

    return [tag_list,release_list,arch_list]

def make_evo_data(file):
    before_tag = []
    before_release = []
    before_arch = []
    after_tag = []
    after_arch = []
    after_release = []
    csv_reader = csv.reader(file)
    for line in csv_reader:
        before_tag.append(int(line[0]))
        before_release.append(int(line[2]))
        before_arch.append(int(line[4]))
        after_tag.append(int(line[1]))
        after_release.append(int(line[3]))
        after_arch.append(int(line[5]))
    return [before_tag,before_release,before_arch],[after_tag,after_release,after_arch]

def make_metachange_data(file):
    insert_b = []
    delete_b = []
    insert_a = []
    delete_a = []
    csv_reader = csv.reader(file)
    for line in csv_reader:
        insert_b.append(int(line[1]))
        insert_a.append(int(line[3]))
        delete_b.append(int(line[2]))
        delete_a.append(int(line[4]))
    return [insert_b,delete_b],[insert_a,delete_a]


def make_commit_data(file):
    allcommit_before = []
    allcommit_after = []
    dfilecommit_before = []
    dfilecommit_after = []
    csv_reader = csv.reader(file)
    for line in csv_reader:
        allcommit_before.append(int(line[1]))
        allcommit_after.append(int(line[2]))
        dfilecommit_before.append(int(line[3]))
        dfilecommit_after.append(int(line[4]))
    return [allcommit_before,dfilecommit_before],[allcommit_after,dfilecommit_after]

def classify_data(file):
    nonDPP_tag = []
    nonDPP_release = []
    nonDPP_arch = []
    DPP_tag = []
    DPP_arch = []
    DPP_release = []
    csv_reader = csv.reader(file)

    for line in csv_reader:
        if line[1] == "no":
            nonDPP_tag.append(int(line[2]))
            nonDPP_release.append(int(line[3]))
            nonDPP_arch.append(int(line[4]))
        else:
            DPP_tag.append(int(line[2]))
            DPP_release.append(int(line[3]))
            DPP_arch.append(int(line[4]))

    return [nonDPP_tag,nonDPP_release,nonDPP_arch],[DPP_tag,DPP_release,DPP_arch]

def classify_type(file):
    template_tag = []
    template_release = []
    template_arch = []
    find_tag = []
    find_arch = []
    find_release = []
    csv_reader = csv.reader(file)

    for line in csv_reader:
        if line[1] == "template":
            template_tag.append(int(line[2]))
            template_release.append(int(line[3]))
            template_arch.append(int(line[4]))
        elif line[1] == "find":
            find_tag.append(int(line[2]))
            find_release.append(int(line[3]))
            find_arch.append(int(line[4]))

    return [template_tag,template_release,template_arch],[find_tag,find_release,find_arch]


def make_violin_graph(list1, list2, namelist, filename):    
    fig = go.Figure()
    for i in range(len(list1)):
        fig.add_trace(go.Violin(y=list1[i],
                                #x=i,
                            name=namelist[i],
                            side='negative',
                            line_color='blue', fillcolor='lightblue', opacity=0.6
                              ))
        fig.add_trace(go.Violin(y=list2[i],
                                #x=i+1,
                            name=namelist[i],
                            side='positive',
                            line_color='red', fillcolor='lightcoral', opacity=0.6
                              ))
        mw.manWhitney(list1[i],list2[i])
    fig.update_traces(box_visible=True,
                        meanline_visible=True
                        ) 
    fig.update_layout(plot_bgcolor="white", showlegend = False)
    fig.update_yaxes(gridcolor='lightgrey', gridwidth=1, griddash='dot')#range=[0, None],
    fig.show()
    fig.write_image(filename)
    print('save %s'%(filename))



def make_seaborn_violin_graph(list1, list2, namelist, filename, labels, log):
    for i in range(len(list1)):
        sns.set_context('talk')
        plt.rcParams['figure.subplot.bottom'] = 0.15
        plt.rcParams['figure.subplot.left'] = 0.18
        if log:
            data = [np.log10(list1[i]),np.log10(list2[i])]
        else: data = [list1[i],list2[i]]
        plt.xticks([0, 1], labels)
        #plt.title(namelist[i])
        ax = sns.violinplot(data,cut=0)
        if log: ax.set_yscale('log')
        mw.manWhitney(list1[i],list2[i])
        plt.savefig('figure/' +namelist[i]+'_'+filename)
        #os.system('pdfcrop ' + 'figure' + namelist[i]+'_'+filename)
        plt.show()
    
    
    print('save %s'%(filename))
    

def make_rq1_graph():
    with open('RQ1-all-dpp-metrics.csv','r') as input_file:
        list1,list2 = classify_data(input_file)
        #make_violin_graph(list1,list2,['Tag','Release','Arch'],'esem-figure/violin/extra-nonDPPvsDPP-met.pdf')
        make_seaborn_violin_graph(list1,list2,['Tag','Supported_image','Arch'],'extra-nonDPPvsDPP-met.pdf',['non-DPP','DPP'],False)

def make_rq2_graph():
    with open('result/RQ3-dpp-before-met-re.csv','r') as input_file:
        list1 = make_data(input_file)
    with open('result/RQ3-dpp-after-met-re.csv','r') as input_file:
        list2 = make_data(input_file)
    
    print(list1)
    print(list2)
    #make_violin_graph(list1,list2,['Tag','Release','Arch'],'esem-figure/violin/rq2-before-afterDPP-met.pdf')
    #make_seaborn_violin_graph(list1,list2,['Tag','Supported_image','Arch'],'rq2-met-evo.pdf',['before the adoption\nof DPP','after the adoption\nof DPP'],False)
    with open('result/met_evolution.csv','r') as input_file:
        list1,list2 = make_evo_data(input_file)
        make_seaborn_violin_graph(list1,list2,['Tag','Supported_image','Arch'],'before_after_dpp.pdf',['before the adoption\nof DPP','after the adoption\nof DPP'],False)
        

def make_extra_graph():
    with open('RQ1-all-dpp-metrics.csv','r') as input_file:
        list1,list2 = classify_type(input_file)
        #make_violin_graph(list1,list2,['Tag','Release','Arch'],'esem-figure/violin/extra-type-dpp-met.pdf')
        make_seaborn_violin_graph(list1,list2,['Tag','Supported_image','Arch'],'extra-type-dpp-met.pdf',['Template','Find and replace'],False)

def make_rq3_graph():
    with open('result/RQ3_commit_only1year.csv')as input_file:
        list1,list2 = make_commit_data(input_file)
        make_seaborn_violin_graph(list1,list2,['all_commit','Dockerfile_commit'],'before_after_dpp.pdf',['before the adoption\nof DPP', 'after the adoption\nof DPP'],True)

def make_meta_change_graph():
    with open('result/meta_line_change.csv')as input_file:
        list1,list2 = make_metachange_data(input_file)
        #make_violin_graph(list1,list2,['insert','delete'],'esem-figure/violin/meta_line_change.pdf')
        make_seaborn_violin_graph(list1,list2,['Release','End_of_support'],'before_after_dpp.pdf', ['before the adoption\nof DPP', 'after the adoption\nof DPP'],False)


def main():
    #make_rq1_graph()
    make_rq2_graph()
    make_rq3_graph()
    #make_extra_graph()
    make_meta_change_graph()

if __name__ == '__main__':
    main()