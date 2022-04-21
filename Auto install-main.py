from importlib.machinery import SOURCE_SUFFIXES
from logging import exception
from logging.handlers import RotatingFileHandler
import os,re,shutil,sys
import subprocess
import fnmatch
#
nginx_config_mod = sys.argv[1]  
env = ''    
app_name = ''
action = ''
find = ''
replace_key = ''
replace_value = ''
php_upstream = ''
nodejs_upstream = ''
cobr_upstream = ''
set = ''  
     
#### Insert y first if you want to modify nginx config:
if sys.argv[1] == "y":
    action = sys.argv[2]
    app_name = sys.argv[3]
    php_upstream = sys.argv[4]
    nodejs_upstream = sys.argv[5]
    cobr_upstream = sys.argv[6]
    env = sys.argv[7]
    set = sys.argv[8]
    ### If want to modify other text in Nginx config ###
    if len(sys.argv[9]) > 1 :
        find = sys.argv[9]
        replace_key = sys.argv[10]
        if len(sys.argv[11]) > 1:
            replace_value = sys.argv[11]
    ### Print value you want to modify ###
    print("PHP upstream: %s"%php_upstream + 
        "\nNodejs upstream: %s"%nodejs_upstream + 
        "\nCoBrowser upstream: %s"%cobr_upstream +
        "\nOther replace:%s"%find + " to " + replace_key)
#### If you only want to list or uninstall ####
elif sys.argv[1]=="list": 
    action = sys.argv[1]
    print("Helm list")
    subprocess.call("helm " + action)
    sys.exit()
elif sys.argv[1] == "un":
    app_name = sys.argv[2]
    print("Executing command: helm " + "uninstall" + " " + app_name  )
    subprocess.call("helm " + "uninstall" + " " + app_name)
    sys.exit()
#### If install or upgrade without modify nginx config ####
else :
    action = sys.argv[1]
    app_name = sys.argv[2]  
    env = sys.argv[3]
    set = sys.argv[4]
                       
#### Find the app directory and move to it ###
def get_root_app():
    pattern = app_name
    for root, dirs, files in os.walk(r"C:/Users/hung/"):
        for dirname in fnmatch.filter(dirs, pattern):
                path_app = os.path.join(root,dirname) # Path from specified directory
                root_app = os.path.abspath(path_app)  # Path from root directory
                print("App directory: " + root_app)
                return root_app  ## Return the path of helm chart
            
#### Modify nginx config ####
def modify_nginx():
    global php_upstream, nodejs_upstream, cobr_upstream  ## Get some variable from ouside
    ### Find template file ###            
    conf_file = "site-nodejs-template.conf" ## Config file parttern
    def find_root_conf():
        for root, dirs, files in os.walk(r"C:/Users/hung/Desktop/Devops/"):
            for filename in fnmatch.filter(files, conf_file):
                path_conf = os.path.join(root,filename)
                root_conf = os.path.abspath(path_conf)
                return root_conf  ## Return the file with abspath     
    src_file = str(find_root_conf()) ## Template config file found from find_root_conf()
    des_file = get_root_app() + "/site-nodejs.conf"  ## Destination folder from get_root_app() + des file
    shutil.copy2(src_file, des_file) #Copy template file to app directory for modify
    # Replace 
    def replace(des_file): 
        ## Open and modify copied file
        with open(des_file, "r+") as file:
            file_contents = file.read()
            ## If you insert y first 
            if sys.argv[1] == "y":
                if len(sys.argv[4]) > 1:
                    file_contents = re.sub("fastcgi_pass .*", "fastcgi_pass %s"%sys.argv[4] + ";" , file_contents )
                ## Modify nodejs upstream   
                if len(sys.argv[5]) > 1:  
                    file_contents = re.sub("proxy_pass http://.*nodejs.*;", "proxy_pass %s"%sys.argv[5] + ";", file_contents ) 
                ## Modify cobrowser upstream  
                if len(sys.argv[6]) > 1:   
                    file_contents = re.sub("proxy_pass http://.*cobr.*;", "proxy_pass %s"%sys.argv[6] + ";", file_contents ) 
                ## If you want to modify some other text in conf file
                if len(sys.argv[9]) > 1:
                    file_contents = re.sub(find, replace_key + " " + replace_value  , file_contents )
            file.seek(0)
            file.truncate()
            file.write(file_contents)
    ## Calling function to replace
    replace(des_file)  
### Install ###
def install():    
    global env, action, app_name       
    os.chdir(str(get_root_app()))
    ## Define environment with values file
    if env=="prod":
        env = "values-Prod.yaml"
    elif env=="dev":
        env = "values-Dev.yaml"
    elif env=="qa":
        env = "values-QA.yaml"
    ## Action
    if action=="install" or action=="template" or action=="upgrade" :
        if len(set) > 1 and len(env) > 1: # if insert set 
            print("Executing command: helm " + action + " " + app_name + " . " "--set " + str(set) + " -f " + env )
            subprocess.call("helm " + action + " " + app_name + " . " " --set " + str(set) + " -f " + env )  
        elif len(set) < 2 and len(env) > 1 : # If insert env but not insert set:
            print("Executing command: helm " + action + " " + app_name + " . -f " + env )
            subprocess.call("helm " + action + " " + app_name + " . -f " + env )
        elif len(set) > 1 and len(env) < 2:
            print("Executing command: helm " + action + " " + app_name + " . --set " + str(set))
            subprocess.call("helm " + action + " " + app_name + " . --set " + str(set) )
        else :
            print("Executing command: helm " + action + " " + app_name + " . ")
            subprocess.call("helm " + action + " " + app_name + " . " ) 
            
#### Finally,after collected essential condition ####
#### call theo 2 main_action function: modify_nginx() and install() ####
try: 
    ## Calling modify function outside the loop
    if nginx_config_mod == "y":
        modify_nginx()     
        install()
        sys.exit()
    else:
        install() 
        sys.exit()
except FileNotFoundError:
    print('''The location of the app could not be found.\nYou must define folder that contain helm chart.\nPlease try again!''')
