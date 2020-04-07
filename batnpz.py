import csv
import numpy as np


train_durations = []
train_files = []
train_pos = []
train_class = []
test_durations = []
test_files = []
test_pos = []
test_class = []
flip = 0

species = {}
species['Barbar_G'] = 1
species['Barbar'] = 1

species['Envsp'] = 2
species['ENVsp'] = 2
species['Eptnil'] = 2
species['Eptser'] = 2
species['Vesmur'] = 2
species['Nyclas'] = 2
species['Nyclei'] = 2
species['Nycnoc'] = 2

species['Myosp'] = 3
species['Myoalc'] = 3
species['Myobec'] = 3
species['Myobra'] = 3
species['Myodas'] = 3
species['Myodau'] = 3
species['Myoema'] = 3
species['Myomyo'] = 3
species['Myomys'] = 3
species['Myonat'] = 3

species['Pip35'] = 4
species['Pipkuh'] = 4
species['Pipnat'] = 4

species['Pip50'] = 5
species['pippiT'] = 5
species['PippiT'] = 5
species['pippyg'] = 5

species['Plesp'] = 6
species['Pleaur'] = 6
species['Pleaus'] = 6

species['Rhisp'] = 7
species['Rhifer'] = 7
species['Rhihip'] = 7

def cleaning(group): 
    global train_durations, train_files, train_pos
    with open('meta' + group + '.csv') as cfile:
        creader = csv.DictReader(cfile, delimiter=',')
        for row in creader:
            if row['FOLDER'] == '':
                with open('group' + group + '/_' + row['IN FILE'].split('.wav')[0] + '-sceneRect.csv') as dfile:
                    dreader = csv.DictReader(dfile, delimiter=',')
                    calls = []
                    for call in dreader:
                        tmp = float(call['LabelStartTime_Seconds'])
                        if tmp > 9:
                            tmp/= 1000.0
                        calls.append(np.array([tmp]))
                    if len(calls) > 0:
                        with open('data' + group + '.csv') as tfile:
                            treader = csv.DictReader(tfile, delimiter=',')
                            for trow in treader:
                                if trow['File'] == row['IN FILE']:
                                    if trow['Id'] != 'ChiroSp':
                                        cond = float(len(train_durations) + len(test_durations))
                                        if cond != 0:
                                            cond = len(train_durations) / cond
                                        
                                        if cond < (5.0/6):
                                            train_files.append(row['IN FILE'])
                                            tmp = float(row['DURATION'])
                                            if tmp > 9:
                                                tmp /= 1000.0
                                            train_durations.append(tmp)
                                            train_pos.append(np.array(calls))
                                            train_class.append(species[trow['Id']])
                                        else:
                                            test_files.append(row['IN FILE'])
                                            tmp = float(row['DURATION'])
                                            if tmp > 9:
                                                tmp /= 1000.0
                                            test_durations.append(tmp)
                                            test_pos.append(np.array(calls))
                                            test_class.append(species[trow['Id']])
                                    break
                                    
                                                

cleaning('1')
cleaning('2')


train_durations = np.array(train_durations)
train_files = np.array(train_files)
train_pos = np.array(train_pos)
train_class = np.array(train_class)
test_durations = np.array(test_durations)
test_files = np.array(test_files)
test_pos = np.array(test_pos)
test_class = np.array(test_class)

np.savez("test.npz", train_durations=train_durations, train_files=train_files, train_pos=train_pos, train_class=train_class, test_durations=test_durations, test_files=test_files, test_pos=test_pos, test_class=test_class)
