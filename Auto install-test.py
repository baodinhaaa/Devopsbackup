from logging import exception
import os,re,shutil
from platform import node
import subprocess



## Define app directory
app_name = input("Define app name to apply: ")
#nginx_config_mod = input("Modify nginx config? (y),(n):" )          
## Insert text to modify    
php_upstream = input("PHP upstream(Template service:port): ")
nodejs_upstream = input("Nodejs helper upstream(Tepmlate http://nodejshelper:port/socketcluster/): ")

## Define action    
action = input("Action: ")
## Define envasdfasdf
env = input("Define environment to apply: ")  
  
### Modify nginx config ###
def modify_nginx():
    global php_upstream, nodejs_upstream
    ## Replace text
    def replace(src_file, des_file, text_php, subs_php, text_njs, sub_njs, flags=0):
        shutil.copy2(src_file, des_file)  #Copy template file to app directory for modify
        
        ## Open and modify copied file
        with open(des_file, "r+") as file:
            file_contents = file.read()
            
            # Compile and modify php upstream
            text_pattern = re.compile(re.escape(text_php), flags)     
            file_contents = text_pattern.sub(subs_php, file_contents)  
            
            # Compile and modify nodejs upstream 
            text_pattern = re.compile(re.escape(text_njs), flags)     
            file_contents = text_pattern.sub(sub_njs, file_contents)
            
            # Compile and modify cobrowser upstream 
            text_pattern = re.compile(re.escape(text_cobr), flags)     
            file_contents = text_pattern.sub(sub_cobr, file_contents)
            
            file.seek(0)
            file.truncate()
            file.write(file_contents)
    
    src_file = "C:/Users/hung/Desktop/Devops/K8s/lhc-template/conf/nginx/site-nodejs.conf"
    des_file =  "C:/Users/hung/Desktop/Devops/K8s/" + app_name + "/site-nodejs.conf"
    # Replace text for PHP_upstream
    text_php = "fastcgi_pass php:9000"
    subs_php = ("fastcgi_pass " + php_upstream)
    
    
    # Replace text for nodejs_upstream
    text_njs = "http://nodejshelper:8000/socketcluster/"
    sub_njs =   "http://lhc-nodejshelper:8000/socketcluster/"
    # Replace text for cobrowser
    text_cobr = "proxy_pass http://cobrowse:31130/"
    sub_cobr = "proxy_pass http://" + app_name + "-cobrowser:31130/"
        
    ## Calling function to replace
    replace(src_file, des_file, text_php, subs_php, text_njs, sub_njs)  

### Install ###
def install():    
    global env, action, app_name           
    os.chdir(r"C:/Users/hung/Desktop/Devops/K8s/" + app_name)
    print("App directory: " + os.getcwd())
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
        subprocess.call("helm " + action + " " + app_name)
    elif action=="in"   :
        action = "install"
        subprocess.call("helm " + action + " " + app_name + " . " + "-f " + env)
        #print("helm " + action + " " + app_name + " . " + "-f " + env)
    elif action=="up":
        action = "upgrade"
        subprocess.call("helm " + action + " " + app_name + " . " + "-f " + env)
    elif action=="tem":
        action = "template"
        subprocess.call("helm " + action + " " + app_name + " . " + "--debug" + " -f " + env )
    elif action=="list" :
        subprocess.call("helm " + action)
    else: 
        print("Invalid action")       
while True:
    try: 
        ## Calling modify function outside the loop
        modify_nginx()     
        
        ## Calling the install function outside the loop
        install()
        break       
    except FileNotFoundError:
        print('''The location of the app could not be found.\nYou must define folder that contain helm chart.\nPlease try again!''')
        continue
    except OSError:
       print("OSerror, try again!")
       continue