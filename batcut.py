import subprocess
import csv
import datetime
import shutil
#from pydub import AudioSegment

def batcut(directory, filename, drow):
    timer = [0]
    previous_end_call = 0
    previous_start_call = 0
    max_timer = 45
    error = False
    sub = subprocess.Popen("soxi " + directory + filename, shell=True, stdout=subprocess.PIPE)
    ret = sub.stdout.read()
    print(type(ret))
    ret = ret.split("\n")
    
    duration = ret[5].split(' : ')[1].split("=")[0].split(':')
    duration = float(duration[0]) * 3600 + float(duration[1]) * 60 + float(duration[2])
    with open(directory + "individual_results/_" + filename.split(".wav")[0] + "-sceneRect.csv", 'r') as calls:
        csv_call = csv.DictReader(calls, delimiter=',') 
        for row in csv_call:
            end_call = row['LabelEndTime_Seconds']
            start_call = row['LabelStartTime_Seconds']
            
            if not '.' in end_call:
                end_call = float(end_call)/1000
            else :
                end_call = float(end_call)
                
            if not '.' in start_call:
                start_call = float(start_call)/1000
            else :
                start_call = float(start_call)
           
            if end_call - start_call > max_timer:
                print("ERROOOOR")
                error = True
            elif start_call - timer[-1] > max_timer:
                count = (start_call - timer[-1]) // max_timer
                while count > 0:
                    timer.append(timer[-1] + max_timer)
                    count -= 1
                if end_call - timer[-1] > max_timer:
                    interval = start_call - (max_timer - (end_call - start_call)) / 2
                    timer.append(interval)
                
            elif start_call - timer[-1] < max_timer and end_call - timer[-1] > max_timer:
                timer.append((previous_end_call + start_call)/2)
               
            previous_end_call = end_call
            previous_start_call = start_call

        while duration - timer[-1] > max_timer:
            timer.append(timer[-1] + max_timer)
        timer.append(duration)
                
    with open(directory + "individual_results/_" + filename.split(".wav")[0] + "-sceneRect.csv", 'r') as calls:
        csv_call = csv.DictReader(calls, delimiter=',') 
        ind_b = 0
        ind_e = 1
        if timer[1] > max_timer:
            print("Timer[1] trop grand")
        for row in csv_call:
            end_call = row['LabelEndTime_Seconds']
            start_call = row['LabelStartTime_Seconds']
            
            if not '.' in end_call:
                end_call = float(end_call)/1000
            else :
                end_call = float(end_call)
                
            if not '.' in start_call:
                start_call = float(start_call)/1000
            else :
                start_call = float(start_call)
                
            while ind_e < len(timer) and start_call >= timer[ind_e]:
                ind_b += 1
                ind_e += 1
                
            
            if ind_e < len(timer) and not(timer[ind_b] <= start_call and end_call <=  timer[ind_e]):
                print("ERROOOR  Start : " + str(timer[ind_b]) + " call : " + str(start_call) + " - " + str(end_call) + "   End : " + str(timer[ind_e]))
                error = True
            
    fn = ["Directory", "File", "Id"] 
    if error:
        with open('error.csv', 'a') as error:
            csv_error = csv.DictWriter(error, fieldnames=fn)
            csv_error.writerow(drow)
    else:
        with open('ok.csv', 'a') as to_cut:
            csv_cut = csv.DictWriter(to_cut, fieldnames=fn)
            tmp_name = drow['File'].split(".wav")[0]
            """actual_audio = AudioSegment.from_wav(directory + filename)
            for i in range(1,len(timer)):
                drow['File'] = tmp_name + "_" + str(i) + ".wav"
                csv_cut.writerow(drow)
                begin = timer[i-1]*1000
                end = timer[i]*1000
                new_audio = actual_audio[begin : end]
                new_audio.export("/home/maxime/Documents/memoire/batnpz/" + drow['File'], format="wav")
            """
            
 
def findcut():
    with open('cut.csv', 'r') as cut:
        csv_reader = csv.DictReader(cut, delimiter=',')        
        for row in csv_reader:
            batcut(row["Directory"], row['File'], row)


#batcut("/home/batmen/batnpz/", "38.wav", {"Directory" : "flip", "File" : "test.wav", "Id" : "etetet"})
batcut("/home/maxime/Documents/memoire/batnpz/", "38.wav", {"Directory" : "/home/maxime/Documents/memoire/batnpz/", "File" : "38.wav", "Id" : "etetet"})
#findcut()
