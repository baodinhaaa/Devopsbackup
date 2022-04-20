from importlib.machinery import SOURCE_SUFFIXES
from logging import exception
from logging.handlers import RotatingFileHandler
import os,re,shutil,sys
import subprocess
import fnmatch


### Define app directory and action ###
action = sys.argv[1]
app_name = sys.argv[2]
nginx_config_mod = sys.argv[3]  
env = ''        
## Insert text to modify
if len(sys.argv[3])>0:    
    if nginx_config_mod == "y":
        php_upstream = sys.argv[4]
        nodejs_upstream = sys.argv[5]
        cobr_upstream = sys.argv[6]
        env = sys.argv[7]
        set = sys.argv[8]
    elif nginx_config_mod == "n":
        env = sys.argv[4]
        set = sys.argv[5]
## Define environment   
    
#### Find the app directory and move to it ###
def get_root_app():
    pattern = app_name
    for root, dirs, files in os.walk(r"C:/Users/hung/"):
        for dirname in fnmatch.filter(dirs, pattern):
                path_app = os.path.join(root,dirname) # Path from specified directory
                root_app = os.path.abspath(path_app)  # Path from root directory
                print("App directory: " + root_app)
                return root_app  ## Return the path of helm chart
### Modify nginx config ###
def modify_nginx():
    global php_upstream, nodejs_upstream, cobr_upstream
    ### Find template file ###            
    conf_file = "site-nodejs-template.conf"
    def find_root_conf():
        for root, dirs, files in os.walk(r"C:/Users/hung/Desktop/Devops/"):
            for filename in fnmatch.filter(files, conf_file):
                path_conf = os.path.join(root,filename)
                root_conf = os.path.abspath(path_conf)
                #print("Config file directory: " + root_conf)
                return root_conf  ## Return the file with abspath     
    src_file = str(find_root_conf())
    #print(type(src_file))
    des_file = get_root_app() + "/site-nodejs.conf"
    shutil.copy2(src_file, des_file) #Copy template file to app directory for modify
    # Replace text
    def replace(des_file): 
        ## Open and modify copied file
        with open(des_file, "r+") as file:
            file_contents = file.read()
            # Compile and modify php upstream  
            file_contents = re.sub("fastcgi_pass .*", "fastcgi_pass %s"%sys.argv[4] + ";" , file_contents )
            # Compile and modify nodejs upstream      
            file_contents = re.sub("proxy_pass http://.*nodejs.*;", "proxy_pass %s"%sys.argv[5] + ";", file_contents ) 
            # Compile and modify cobrowser upstream      
            file_contents = re.sub("proxy_pass http://.*cobr.*;", "proxy_pass %s"%sys.argv[6] + ";", file_contents ) 
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
    #print("helm " + action + " " + app_name + " . " + "-f " + env
    ## Action
    if action=="un" :
        action = "uninstall"
        print("Executing command: helm " + action + " " + app_name + " . " " --set " + str(set) + " -f " + env )
        subprocess.call("helm " + action + " " + app_name)
    elif action=="in"   :
        action = "install"
        print("Executing command: helm " + action + " " + app_name + " . " " --set " + str(set) + " -f " + env )
        subprocess.call("helm " + action + " " + app_name + " . " " --set " + str(set) + " -f " + env )
        
    elif action=="up":
        action = "upgrade"
        print("Executing command: helm " + action + " " + app_name + " . " + "-f " + env)
        subprocess.call("helm " + action + " " + app_name + " . " + "-f " + env)
    elif action=="tem":
        action = "template"
        subprocess.call("helm " + action + " " + app_name + " . " + "--debug" + " -f " + env + " --set " + str(set))
        print("Command executed: helm " + action + " " + app_name + " . " + "--debug" + " -f " + env + " --set " + str(set))
    elif action=="list" :
        print("Helm list")
        subprocess.call("helm " + action)
    # else: 
    #     print("Invalid action")     
while True:
     try: 
        ## Calling modify function outside the loop
        if nginx_config_mod == "y":
            modify_nginx()     
            install()
            break
        else:
           install() 
        break       
     except FileNotFoundError:
        print('''The location of the app could not be found.\nYou must define folder that contain helm chart.\nPlease try again!''')
        continue
    