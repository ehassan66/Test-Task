import os
import shutil
import argparse
import datetime
import time

source_dir = r"C:\Python311\VeeamTask\source"
destination_dir = r"C:\Python311\VeeamTask\target"
#Delete funtion when delete a file/folders from source then its impact on target
def delete(src_dir, rep_dir, log_writer):
    for root, dirs, files in os.walk(rep_dir):
        rel_dir = os.path.relpath(root, rep_dir)
        src_dir = os.path.join(src_dir, rel_dir)
        rep_dir = os.path.join(rep_dir, rel_dir)
        if not os.path.exists(src_dir):
            shutil.rmtree(rep_dir, ignore_errors=True)
            print('removed directory '+str(rep_dir))
            log_writer.write('removed directory '+str(rep_dir)+'\n')
            continue
        for file in files:
            rep_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(src_dir, file)
            if not os.path.exists(dst_file_path):
                os.remove(rep_file_path)
                print('removed ', file)
                log_writer.write('removed '+ str(file)+'\n')


#Copy and replace funtion from source directory to target directory.
def copy_replace(src_dir, rep_dir, log_writer):
    for root, dirs, files in os.walk(src_dir):
        rel_dir = os.path.relpath(root, src_dir) #get the raltive path of source directory. 
        dst_dir = os.path.join(rep_dir, rel_dir) #join the replica directory with raltive path
        os.makedirs(dst_dir, exist_ok=True)
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_dir, file)
            if os.path.exists(dst_path) and os.stat(src_path).st_mtime <= os.stat(dst_path).st_mtime:
                continue  # skip files that are already synchronized
            shutil.copy2(src_path, dst_dir)
            print('copied', file)
            log_writer.write('copied '+ str(file)+'\n')
#Main Sync Funtion
def sync(source_dir, destination_dir, log_file_name, sync_interval):
    while (True):
        print("synching at "+str(datetime.datetime.now()))
        with open(log_file_name, 'w') as log_writer:
            copy_replace(source_dir, destination_dir, log_writer)
            delete(source_dir, destination_dir, log_writer)
        time.sleep(sync_interval)

# print(os.path.exists("C:\Python311\VeeamTask\folder1\."))
# print(os.path.exists("C:\Python311\VeeamTask\folder1"))



parser = argparse.ArgumentParser(description='Sync two folders periodically')
parser.add_argument('source_dir', metavar='SRC_DIR', help='the source folder path')
parser.add_argument('destination_dir', metavar='REP_DIR', help='the replica folder path')
parser.add_argument('-i', '--interval', metavar='SECONDS', type=int, default=60,
                    help='the sync interval in seconds')
parser.add_argument('-l', '--log', metavar='LOGFILE', help='the log file path')

args = parser.parse_args()
print(args.source_dir)
print(args.destination_dir)
print(args.interval)
print(args.log)


sync(args.source_dir, args.destination_dir, args.log, args.interval)

# How to pas parameters in command line argument. 
#-l='abc.log' -i=10 "C:\Python311\VeeamTask\source" "C:\Python311\VeeamTask\target"
