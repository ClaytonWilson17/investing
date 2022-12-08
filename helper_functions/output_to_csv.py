# Outputs a list of dictionaries to a csv file

import itertools
from openpyxl import Workbook
import csv
import pandas as pd

def print_to_csv(data, filename):
    '''
    Input:
    
    data - list of dictionaries

    filename - name you want the file to have

    
    '''

    print("Creating reports...\n")
    keys = data[0].keys()

    save_path = './results/' + filename + '.csv'

    with open(save_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


    print ("Results saved to the results directory.\n")

    return (save_path)