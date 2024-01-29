#!/usr/bin/python

from distutils.archive_util import make_archive
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os
import sys
import argparse
import seaborn as sns
from matplotlib.cm import Dark2
from matplotlib.lines import Line2D


def load_data(file):
    # Importing the dataset
    dataset = pd.read_csv(file, sep="\t")
    return dataset

def make_lists_for_contours():
    prec=range(0,100,1)
    #prec=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    #f=[70,75,80,85,90,95]
    f=[40,50,60,70,80,90]
    #rec_prec={j:[[i,(j*i)/((2*i)-j)] for i in prec if ((2*i)!=j)] for j in f }
    x=[i for i in prec for j in f if ((2*i)!=j)]
    y=[(j*i)/((2*i)-j) for i in prec for j in f if ((2*i)!=j)]
    #print(rec_prec)
    return x,y

def plot_data(options):
    num_categories = 9
    #c = [Dark2(float(i)/num_categories) for i in range(num_categories)]
    c = sns.color_palette(n_colors=9)

    #make font size larger
    sns.set(font_scale=1.8)
    sns.set_style("whitegrid")
    sns.color_palette(c, num_categories)
    df = load_data(options.input_file)
    g = sns.relplot(
        data=df,
        x="Precision", y="Recall", 
        # hue="Step", 
        # palette=c, 
        linewidth=2,
        color="black",
        s=300,
        markers=True,
        dashes=False,
        #sort=False, 
        #kind="line"
        kind="scatter"
        
    ).set(title=options.task)
    
    g.figure.set_size_inches(14,12)
    g.ax.margins(.15)
    g.ax.xaxis.grid(True, "major", linewidth=.25)
    # g.ax.xaxis.grid(True, "minor", linewidth=.05)
    g.ax.yaxis.grid(True, "major", linewidth=.25)
    
#     plt.yticks([65,70,75,80,85,90,95,100],[65,70,75,80,85,90,95,100])
#     plt.xticks([65,70,75,80,85,90,95,100],[65,70,75,80,85,90,95,100])
    plt.yticks([10,20,30,40,50,60,70,80,90,100],[10,20,30,40,50,60,70,80,90,100])
    plt.xticks([10,20,30,40,50,60,70,80,90,100],[10,20,30,40,50,60,70,80,90,100])

    g.ax.set_ylim([0, 102])
    g.ax.set_xlim([0, 102])


    g.ax.set(xlabel='Precision (%)', ylabel='Recall (%)')

    # #plot points from file to see what has been checked.
    
    sns.scatterplot(data=df,x='Precision',y='Recall',palette=c,hue="Lifestyle-factor branch",s=100)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    font_size=15
    plt.text(x=df.Precision[0]-25.0,y=df.Recall[0]-5.0,s=str(df['Lifestyle-factor_branch'][0])+" ("+str(df.F[0])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[0],alpha=0.5))
    plt.text(x=df.Precision[1]-13.0,y=df.Recall[1]-4.0,s=str(df['Lifestyle-factor_branch'][1])+" ("+str(df.F[1])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[1],alpha=0.5))
    plt.text(x=df.Precision[2]-23.0,y=df.Recall[2]-4.0,s=str(df['Lifestyle-factor_branch'][2])+" ("+str(df.F[2])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[2],alpha=0.5))
    plt.text(x=df.Precision[3]-33.0,y=df.Recall[3]-1.7,s=str(df['Lifestyle-factor_branch'][3])+" ("+str(df.F[3])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[3],alpha=0.5))
    plt.text(x=df.Precision[4]-10.0,y=df.Recall[4]+3.0,s=str(df['Lifestyle-factor_branch'][4])+" ("+str(df.F[4])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[4],alpha=0.5))
    plt.text(x=df.Precision[5]-28,y=df.Recall[5]+3.0,s=str(df['Lifestyle-factor_branch'][5])+" ("+str(df.F[5])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[5],alpha=0.5))

    plt.text(x=df.Precision[6]-5.0,y=df.Recall[6]+3.0,s=str(df['Lifestyle-factor_branch'][6])+" ("+str(df.F[6])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[6],alpha=0.5))
    plt.text(x=df.Precision[7]-35.0,y=df.Recall[7]-4.0,s=str(df['Lifestyle-factor_branch'][7])+" ("+str(df.F[7])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[7],alpha=0.5))
    plt.text(x=df.Precision[8]-1,y=df.Recall[8]+3.0,s=str(df['Lifestyle-factor_branch'][8])+" ("+str(df.F[8])+"%)", 
            fontdict=dict(color='black',size=font_size),
            bbox=dict(facecolor=c[8],alpha=0.5))
    
    # Create legend elements
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=label, 
                              markerfacecolor=color, markersize=10) for label, color in zip(df['Lifestyle-factor_branch'].unique(), c)]

    # Add the legend to the plot
    plt.legend(handles=legend_elements, loc='lower left', frameon=False)


    #plot the contours
    x_c,y_c=make_lists_for_contours()
    plt.scatter(x_c, y_c, s=1,  marker='o', c='grey')
    
    plt.savefig(options.output_file) 
    plt.show()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h','--help', action="help", help='Example call: python3 plot_prec_rec_progression.py --input_file=progression_precision_recall.tsv --task="Precision-Recall Plot for Progression" --output_file=progression_plot.pdf')
    parser.add_argument("--input_file", required=True, type=str)
    parser.add_argument("--task", required=True, type=str)
    parser.add_argument("--output_file", required=True, type=str)
    args = parser.parse_args()
    current_file_path = dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append("/".join(current_file_path.split("/")[:-1]))
    sys.path.append("/".join(current_file_path.split("/")[:-2]))
    plot_data(args)
