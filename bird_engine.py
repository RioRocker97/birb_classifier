import argparse,tqdm,time,threading,subprocess,shutil,os
from yolo_detect import prepareYolo,runYolo
#subprocess.run('cls',shell=True)
def progress_bar():
    for i in tqdm.tqdm(range(100),ncols=70,desc="anything"):
        num=0
        for i in range(0,1000000):
            num+=1
def progress_bar2():
    for i in tqdm.tqdm(range(100),ncols=70,desc="something"):
        num=0
        for i in range(0,10000):
            num+=1
def my_progress(name,rag):
    for i in tqdm.tqdm(range(100),ncols=70,desc=name):
        num=0
        for i in range(0,rag):
            num+=1
def cmd_usage():
    arg = argparse.ArgumentParser(usage="Something")
    opt = arg.parse_args()
    return opt
# just trying out tqdm with muti-thred . IDK im suck at mutithreading
def test_fx():
    task1 = threading.Thread(target=my_progress,args=("Task 1",1000000))
    task2 = threading.Thread(target=my_progress,args=("Task 2",10000))
    task3 = threading.Thread(target=my_progress,args=("Task 3",100000))
    task4 = threading.Thread(target=my_progress,args=("Task 4",100000))
    task1.start()
    task2.start()
    task3.start()
    task4.start()
# real deal
def preload():
    if not os.path.exists(os.getcwd()+'/birb_model/'):
        os.makedirs(os.getcwd()+'/birb_model/')
        my_progress("Get all model",100000)
    if not os.path.exists(os.getcwd()+'/temp/'):
        os.makedirs(os.getcwd()+'/temp/')


if __name__ == "__main__":
    subprocess.run('cls',shell=True)
    preload()

# everything goes here
# i want this to be beautiful while running in CMD

