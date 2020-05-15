# -*- coding: utf-8 -*-
import csv
import numpy as np
import os
import subprocess

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
species['Pippyg'] = 5

species['Plesp'] = 6
species['Pleaur'] = 6
species['Pleaus'] = 6

species['Rhisp'] = 7
species['Rhifer'] = 7
species['Rhihip'] = 7

countspecies={ 1 : [0,0], 2 : [0,0], 3 : [0,0], 4 : [0,0], 5 : [0,0], 6 : [0,0], 7 : [0,0]}

def cleaning(group): 
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
                        tmp *= 10
                        calls.append(np.array([tmp]))
                    if len(calls) > 0:
                        with open('data' + group + '.csv') as tfile:
                            treader = csv.DictReader(tfile, delimiter=',')
                            for trow in treader:
                                if trow['File'] == row['IN FILE']:
                                    if trow['Id'] not in ('ChiroSp', 'Pipsp', 'Nycsp') and countspecies[species[trow['Id']]][0] < 201:
                                        cond = float( sum( countspecies[species[trow['Id']]] ) )
                                        
                                        if cond != 0:
                                            cond = countspecies[species[trow['Id']]][0] / cond
                                        
                                        if cond < (9.0/10):
                                            countspecies[species[trow['Id']]][0] += 1
                                            train_files.append(row['IN FILE'].split('.')[0])
                                            tmp = float(row['DURATION'])
                                            if tmp > 9:
                                                tmp /= 1000.0
                                            tmp *= 10
                                            train_durations.append(tmp)
                                            train_pos.append(np.array(calls))
                                            train_class.append(species[trow['Id']])
                                        else:
                                            countspecies[species[trow['Id']]][1] += 1
                                            test_files.append(row['IN FILE'].split('.')[0])
                                            tmp = float(row['DURATION'])
                                            if tmp > 9:
                                                tmp /= 1000.0
                                            tmp *=10
                                            test_durations.append(tmp)
                                            test_pos.append(np.array(calls))
                                            test_class.append(species[trow['Id']])
                                    break
                                    
                                                
def directory(path, name="data.csv"):
    for x in os.listdir(path):
        if ".wav" in x:
            sub = subprocess.Popen("soxi " + path + x, shell=True, stdout=subprocess.PIPE)
            ret = sub.stdout.read()
            ret = ret.split("\n")
            
            duration = ret[5].split(' : ')[1].split("=")[0].split(':')
            duration = float(duration[0]) * 3600 + float(duration[1]) * 60 + float(duration[2])
            
            with open(path + 'individual_results/_' + x.split('.wav')[0] + '-sceneRect.csv') as dfile:
                dreader = csv.DictReader(dfile, delimiter=',')
                calls = []
                for call in dreader:
                    tmp = call['LabelStartTime_Seconds']
                    if not '.' in tmp:
                        tmp = float(tmp) / 1000.0
                    else:
                        tmp = float(tmp)
                    if tmp < (duration - 0.25):
                    	calls.append(np.array([tmp]))
                if len(calls) > 0:
                    with open(path + name) as tfile:
                        treader = csv.DictReader(tfile, delimiter=',')
                        for trow in treader:
                            nam = None
                            if "Fichier" in trow:
                                nam = trow['Fichier']
                            if nam == '' or nam is None:
                                nam = trow['File']
                            if nam == x:
                                if trow['Id'] not in ('ChiroSp', 'Pipsp','Nycsp')  and duration < 60:
                                    cond = float(sum(countspecies[species[trow['Id']]]))
                                    
                                    if cond != 0:
                                        cond = countspecies[species[trow['Id']]][0] / cond
                                    if cond < (9.0/10):
                                        countspecies[species[trow['Id']]][0] += 1
                                        train_files.append(path + x.split('.')[0])
                                        tmp = float(duration)
                                        train_durations.append(tmp)
                                        train_pos.append(np.array(calls))
                                        train_class.append(species[trow['Id']])
                                    else:
                                        countspecies[species[trow['Id']]][1] += 1
                                        test_files.append(path + x.split('.')[0])
                                        tmp = float(duration)
                                        test_durations.append(tmp)
                                        test_pos.append(np.array(calls))
                                        test_class.append(species[trow['Id']])
                                break



cleaning('1')
cleaning('2')
directory("/storage/Barba_Lux_2017/")
directory("/storage/Barba_Lux_2018/")
directory("/storage/LPB2018/", "found_LPB2018.csv")
directory("/storage/Barbalux_2016/", "found_Barbalux_2016.csv")
directory("/storage/Ecoduc20150801-04_CecileHerr/", "found_Ecoduc20150801-04_CecileHerr.csv")
directory("/storage/études_complémentaires/", 'found_études complémentaires.csv')
directory("/storage/plateau_Engeland/", 'found_plateau Engeland.csv')
directory("/storage/Plecobrux_SM4_cécile/","found_Plecobrux SM4 cécile.csv")
directory("/storage/TrouPicotIntérieurJuin2014/", "found_TrouPicotIntérieurJuin2014.csv")
directory("/storage/my_test/", "found_my_test.csv")
directory("/storage/CavesPahautAutomne2013/", "found_CavesPahautAutomne2013.csv")
directory("/storage/Copie_de_Brabantwallon2014/", "found_Copie de Brabantwallon2014.csv")
directory("/storage/Copie_de_Vesdre2014/", "found_Copie de Vesdre2014.csv")
directory("/storage/GueuleTOUT/", "found_GueuleTOUT.csv")
directory("/storage/JenneretTOUT/", "found_JenneretTOUT.csv")
directory("/storage/LIFEPrairiesBocageres_2013_TOUT_test/", "found_LIFEPrairiesBocageres_2013_TOUT_test.csv")
directory("/storage/LIFEPrairiesBocageres_2014/", "found_LIFEPrairiesBocageres_2014.csv")
directory("/storage/Plecobrux_ligne_161_Tout/", 'found_Plecobrux ligne 161_Tout.csv')
directory("/storage/Plecolux_2016-TOUT/", "found_Plecolux 2016-TOUT.csv")

directory ("/storage/SM2_Escaut2015/", "found_SM2_Escaut2015.csv")


train_durations = np.array(train_durations)
train_files = np.array(train_files)
train_pos = np.array(train_pos)
train_class = np.array(train_class)
test_durations = np.array(test_durations)
test_files = np.array(test_files)
test_pos = np.array(test_pos)
test_class = np.array(test_class)

np.savez("test.npz", train_durations=train_durations, train_files=train_files, train_pos=train_pos, train_class=train_class, test_durations=test_durations, test_files=test_files, test_pos=test_pos, test_class=test_class)
l = train_class

for team in [ele for ind, ele in enumerate(l,1) if ele not in l[ind:]]:
    count = 0
    for ele in l:
        if team == ele:
            count += 1
    print("{} {}".format(team, count))
    count =0
