import os
import sys
import csv
import pickle
from datetime import date, datetime

def get_git_root(path=os.getcwd()):
    
    '''
    Get Git Root Directory(starts at calling script). Only recursively goes up 10 directories.
    RETURNS: None or absolute path to git root directory
    '''
    count = 0
    prefix = ""
    while count < 10:
        if os.path.exists(prefix+'.git'):
            return os.path.abspath(prefix)
        else:
            prefix +="../"
            count+=1
    print("No git top level directory")
    return None

def get_env_vars():
    env_file = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),get_git_root()+"/.env"))
    if os.path.exists(env_file):
        if os.stat(env_file).st_size > 12: # there is 12 characters in there by default.
            print(".env exists with value filled in- API keys")
            try:
                file = open(env_file)
                for line in file:
                    var = line.strip().split('=')[0]
                    value = line.strip().split('=')[1].strip("\"")
                    os.environ[var] = value
            except Exception as e:
                print(e)
                exit()
        # otherwise get it from an environment variable
        else:
            print(".env is empty")
            sys.exit()
    else:
        print(".env doesn't exist")
        sys.exit()


def listOfDictsToCSV(list, path):

    '''
    Takes in a list of dictionaries and outputs it to a CSV file
    '''
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(list[0].keys())
        for check in list:
            writer.writerow(check.values())

def CSVToListOfDicts(path):
    '''
    Takes in a CSV and turns it into a list of dictionaries. Assumes formatted correctly.
    '''
    with open(path, 'r') as f:
        listOfDicts = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return listOfDicts

def dataPath(filename=None):
    '''
    filename = (optional) the filename of the file you want to access
    RETURNS: absolute path of your file in the data folder
    '''
    root = get_git_root()
    path = os.path.abspath(root+"/data/")
    # Must ensure path to that file exists
    if not os.path.exists(path):
        os.makedirs(path)

    if filename is not None:
        return os.path.abspath(path+"/"+filename)
    else:
        return path

def resultsPath(filename=None):
    '''
    filename = (optional) the filename of the file you want to access
    RETURNS: absolute path of your file in the data folder
    '''
    root = get_git_root()
    path = os.path.abspath(root+"/results/")
    # Must ensure path to that file exists
    if not os.path.exists(path):
        os.makedirs(path)

    if filename is not None:
        return os.path.abspath(path+"/"+filename)
    else:
        return path

def fileSaveCache(filepath, data, datestamp=True):
    if os.path.exists(filepath):
        print("already cached... overwriting it")
    if datestamp:
        filepath = os.path.splitext(filepath)[0]+str(date.today())+os.path.splitext(filepath)[1]
    with open(filepath, 'wb') as outp:
        pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)

def fileLoadCache(filepath,datestamp=True):
    if datestamp:
        filepath = os.path.splitext(filepath)[0]+str(date.today())+os.path.splitext(filepath)[1]
    if os.path.exists(filepath):
        with open(filepath, 'rb') as inp:
            print("Loading "+str(filepath)+" as cache")
            return pickle.load(inp)
    else:
        print(str(filepath)+" does not exist")
        return None


def clean_list_of_dicts(list_of_dicts):
    # get rid of unwanted columns
    cleaned_stocks_to_buy = []
    for dict in list_of_dicts:
        new_dict = {}
        new_dict['Symbol'] = dict['Symbol']
        new_dict['Price'] = dict['Price']
        new_dict['Signal'] = dict['Based on Indicators']
        cleaned_stocks_to_buy.append(new_dict)

    return (cleaned_stocks_to_buy)
