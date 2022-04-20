import os,fnmatch,shutil,re,argparse
from traceback import format_list
# pattern = "nginx-app"
# for root, dirs, files in os.walk("./"):
#     for dirname in fnmatch.filter(dirs, pattern):
#         print(root)
#             # fname = os.path.join(root,dirname)
#             # print(os.path.abspath(fname))

all_args = argparse.ArgumentParser()
all_args.add_argument("-x", "--Value1", required=True)
args = vars(all_args.parse_args())
print("Product is {}".format(int(args['Value1']) ))

# pattern = "lhc-install"
# for root, dirs, files in os.walk(r"C:/Users/hung/Desktop/Devops/"):
#     for dirname in fnmatch.filter(dirs, pattern):
#             path = os.path.join(root,dirname)
#             print("App directory: " + os.path.abspath(path))
# conf_file = "site-nodejs-template.conf"
# for root, dirs, files in os.walk(r"C:/Users/hung/Desktop/Devops/"):
#             for filename in fnmatch.filter(files, conf_file):
#                     path_conf = os.path.join(root,filename)
#                     root_conf = os.path.abspath(path_conf)
#                     print("Config file directory: " + root_conf)
            
# # ch_dir = os.chdir(os.path.abspath(path))

# ### Modify nginx config ###
# def modify_nginx():
#     # Replace text
#     def replace(src_file, des_file):
#         shutil.copy2(src_file, des_file)  #Copy template file to app directory for modify
        
#         ## Open and modify copied file
#         with open(des_file, "r+") as file:
#             file_contents = file.read()
            
#             # Compile and modify php upstream
#             # text_pattern = re.findall("fastcgi_pass", file_contents)     
#             file_contents = re.sub("proxy_pass .*;", "proxy_pass "+"hung123;", file_contents) 
            
#             # # Compile and modify nodejs upstream 
#             # #text_pattern = re.compile(re.escape(text_njs), flags)     
#             # file_contents = re.sub("proxy_pass http://.*nodejs.*;", "proxy_pass %s"%sys.argv[5], file_contents ) 
            
#             # # Compile and modify cobrowser upstream 
#             # #text_pattern = re.compile(re.escape(text_cobr), flags)     
#             # file_contents = re.sub("proxy_pass cobrowser.*;", "proxy_pass %s"%sys.argv[6], file_contents ) 
            
#             file.seek(0)
#             file.truncate()
#             file.write(file_contents)
    
#     src_file = "C:/Users/hung/Desktop/Devops/K8s/lhc-template/conf/nginx/site-nodejs-template.conf"
#     des_file = "C:/Users/hung/Desktop/Devops/K8s/lhc-install/site-nodejs.conf"      
#     ## Calling function to replace
#     replace(src_file, des_file)  
# modify_nginx()