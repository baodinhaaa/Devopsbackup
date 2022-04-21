import subprocess
import os,re
os.chdir(r"C:/Users/hung/Desktop/Devops/k8s/Matomo-Mysql K8s/matomo/template/")
import glob
files = glob.glob("dpl-*.txt")

# files = os.listdir()
print(files)
# filenames = []
# for file in files:
#     nn = re.findall("^dpl-.*.txt$", file)
#     if nn: filenames.append(nn[0])
# print(filenames)
filenames = files
with open('output.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile: 
            outfile.write(infile.read())
        outfile.write("\n---\n")

# open(r"dpl-nginx-lhc.yaml")
# for file in files:
#     if re.match(r"dpl-*\.yaml", "rw"):
#         list.append(file)
#         with open(r"dpl-nginx-lhc.yaml") as filename:
#             #x = "---".join(list)
#             subprocess.run("cat" + list + ">>","deploymentall.yaml")
