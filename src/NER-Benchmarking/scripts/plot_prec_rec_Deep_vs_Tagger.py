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
    font_size=15
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
        # linewidth=2,
        # color="black",
        # s=300,
        # markers=True,
        # dashes=False,
        #sort=False, 
        #kind="line"
        kind="scatter"
        
    ).set(title=options.task)
    
    g.figure.set_size_inches(12,12)
    g.ax.margins(.15)
    g.ax.xaxis.grid(True, "major", linewidth=.25)
    # g.ax.xaxis.grid(True, "minor", linewidth=.05)
    g.ax.yaxis.grid(True, "major", linewidth=.25)
    
    plt.yticks([10,20,30,40,50,60,70,80,90,100],[10,20,30,40,50,60,70,80,90,100])
    plt.xticks([10,20,30,40,50,60,70,80,90,100],[10,20,30,40,50,60,70,80,90,100])

#    g.ax.set_ylim([15, 102])
#    g.ax.set_xlim([15, 102])
    g.ax.set_ylim([0, 102])
    g.ax.set_xlim([0, 102])


    g.ax.set(xlabel='Precision (%)', ylabel='Recall (%)')

#     # #plot points from file to see what has been checked.
    
#     sns.scatterplot(data=df,x='Precision',y='Recall',palette=c,hue="Lifestyle-factor branch",s=100)

#     sns.scatterplot(data=df, x='Precision_ooc', y='Recall_ooc', marker='x', color='red', s=100)


        # Define a color palette based on "Lifestyle-factor branch"
    palette = sns.color_palette("Set1", n_colors=len(df["Lifestyle-factor branch"].unique()))

        # Create a dictionary to map each unique value in "Lifestyle-factor branch" to a color
    color_mapping = dict(zip(df["Lifestyle-factor branch"].unique(), palette))

        # Initialize lists to store colors for each data point
    colors_prec_recall = []
    colors_prec_ooc_recall_ooc = []

        # Iterate over rows in the DataFrame
    for index, row in df.iterrows():
        # Extract "Lifestyle-factor branch" value
        lifestyle_branch = row['Lifestyle-factor branch']
                
        # Get the color based on "Lifestyle-factor branch"
        color = color_mapping.get(lifestyle_branch)
        
        # Append colors to the respective lists
        colors_prec_recall.append(color)
        colors_prec_ooc_recall_ooc.append(color)

        
        # Create scatter points for the two sets with different markers and colors
    plt.scatter(df['Precision'], df['Recall'], c=c, marker='o', s=300,label='Dictionary-NER')
    
    scatter=plt.scatter(df['Precision_transformer'], df['Recall_transformer'], c=c, marker='^', s=300,label='Transformer-NER')

    plt.legend(loc='lower left',fontsize=font_size)  # Change the legend position to lower right
    #plt.legend(loc='upper left', fontsize=font_size, bbox_to_anchor=(1.05, 1))

  

    # Get unique labels from the "Lifestyle-factor branch" column
    unique_labels = df['Lifestyle-factor branch'].unique()

    df.columns = [c.replace(' ', '_') for c in df.columns]

  # Create custom legend handles and labels for "Without OOC"
    legend_handles_ooc = [plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=15, label=label)
                        for color, label in zip(c, unique_labels)]

    # Get the existing handles and labels
    handles, labels = plt.gca().get_legend().legendHandles, ["Dictionary-based NER" , "Transformer-based NER"]

  
    # Add an empty legend entry as a separator
    empty_legend = plt.Line2D([], [], color='none', markerfacecolor='none', markersize=0, label='Separator')

    # Add the custom legend for "Without OOC" using the handles and labels
    #plt.legend(handles=handles + [empty_legend] + legend_handles_ooc, labels=labels + ['Lifestyle-factor branch'] + [f"{label}" for label in unique_labels], loc='upper left', fontsize=font_size)
    plt.legend(handles=handles + [empty_legend] + legend_handles_ooc, labels=labels + [''] + [f"{label}" for label in unique_labels], loc='lower left', fontsize=font_size)

   
    # Add a title to the second legend (for "Without OOC")
    plt.gca().get_legend().get_title().set_text('Lifestyle-factor branch')

    #plot the contours
    x_c,y_c=make_lists_for_contours()
    plt.scatter(x_c, y_c, s=1,  marker='o', c='grey')
    # Create the figure
    # plt.legend(handles=legend_elements, loc='center', bbox_to_anchor=(1.1, 0.2), frameon=False)
    # Add the line for setting the aspect ratio
    plt.gca().set_aspect('equal', adjustable='box')

    plt.savefig(options.output_file, dpi=300,bbox_inches='tight')
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
