import os
from random import randint
import subprocess
import numpy as np
import shutil
import time

num_of_mutation = 10000
mutation_method = 0
directory = os.getcwd()


def read_image_file(input_image_file):
    file = open(input_image_file, "rb")
    byte = list(file.read())
    file.close()
    return bytearray(byte)


def mutate_imagefile(buff):
    buff_len = len(buff)
    mutation_pos = randint(0, buff_len - 1)
    if mutation_method == 0:
        buff[mutation_pos] = randint(0, 255)
        return buff
    else:
        length_of_mutation = randint(3, int(buff_len/2))
        for i in range(1, length_of_mutation):
            if (mutation_pos+i) >= buff_len:
                mutation_pos = 0
            if mutation_method == 1:
                buff[mutation_pos+i] = 0
            elif mutation_method == 2:
                buff[mutation_pos+i] = 255
        return buff


def save_mutated_imagefile(buff_mutated, filename):
    file = open(filename, "wb")
    file.write(buff_mutated)
    file.close()


def run_target_program(input_file, output_file):
    cmd = ["./jpgbmp", input_file, output_file]
    run = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output, stderr = run.communicate()
    #print(output)
    return output


def delete_file(file):
    file_path = os.path.join(directory, file)
    if os.path.exists(file_path):
        os.remove(file_path)


def analyze_output_target_program(output, bug_count, bug_type, input_file, output_file):
    s = output.decode()
    #print(s)
    if 'Bug' in s:
      bug_num = int(s[19:20])
      print(s[19:20])
    
    if 'Bug' not in s:
        delete_file(input_file)
        delete_file(output_file)
    
    #return bug_type
    elif 'Bug' in s:
        #bug_num = int(s.split(" ")[1][1])
        bug_count[bug_num-1] += 1

        bug_file_name = input_file.split('.')[0] + "-{}.jpg".format(bug_num)
        os.rename(input_file, bug_file_name)
        print(s + "Bug found by {0} and  renamed to {1}".format(input_file, bug_file_name))

        if bug_num not in bug_type:
            bug_type.append(bug_num)
    
    return bug_type



def save_test_files():
    if not os.path.isdir("Backup"):
        os.mkdir("Backup")
    timestamp = time.strftime("%Y-%b-%d__%H_%M_%S", time.localtime())
    path = os.path.join(directory, "Backup", "{}".format(timestamp))
    os.makedirs(path)
    files = os.listdir(directory)
    for file in files:
        if ("test" in file) and (".jpg" in file):
            src = os.path.join(directory, file)
            dst = os.path.join(path, file)
            shutil.move(src, dst)
    print("All test Files which trigerred bugs are moved to Backup: {}".format(path))


def main():
    bug_count = np.zeros(8)
    bug_type = []
    total_num_bug = 8
    for i in range(num_of_mutation):
        buff = read_image_file("cross.jpg")
        buff_mutated = mutate_imagefile(buff)
        mutated_filename = "test{}.jpg".format(i)
        save_mutated_imagefile(buff_mutated, mutated_filename)

        output_file = "test{}.bmp".format(i)
        output_target_program = run_target_program(mutated_filename, output_file)

        bugs_found = analyze_output_target_program(output_target_program, bug_count, bug_type, mutated_filename, output_file)
        if len(bugs_found) == 8:
            print("Success in trigerring All {} bugs, exiting program".format(8))
            break
    print("*********Result*******************************************")
    print("Total number of mutated file:", i+1)
    print("Total number of files that triggered bug:", bug_count.sum())
    for i in range(total_num_bug):
        print("Bug{} count:{}".format(i+1, bug_count[i]))

    if len(bugs_found) != 0:
        save_test_files()


if __name__ == '__main__':
    main()