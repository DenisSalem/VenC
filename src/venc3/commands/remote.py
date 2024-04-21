#! /usr/bin/env python3

#    Copyright 2016, 2024 Denis Salem
#
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

import os
import ftplib

from venc3.prompt import notify
from threading import Lock

LOCK = Lock()

BATCH = {}

def cross_thread_lookup(item, action):
    if not len(item):
        return False
      
    global BATCH
    global LOCK
    LOCK.acquire()
    ret = False
    for session_id in BATCH.keys():
        if action == "to_create":
            if item in BATCH[session_id]["to_create"].keys():
                BATCH[session_id]["to_create"][item]["priority"] += 1
                ret |= True
                break
        else:
            for key in BATCH[session_id]["to_delete"].keys():
                if item != key and len(item.split('/')) < len(key.split('/')):
                    BATCH[session_id]["to_delete"][key]["priority"] += 1
                    ret |= True
                    break

    LOCK.release()
    return ret
        
def ftp_session(session_id, blog_configuration, username, user_passwd):
        ftp = ftplib.FTP()
        ftp.encoding = blog_configuration["ftp_encoding"]
        ftp.connect(blog_configuration["ftp_host"], blog_configuration["ftp_port"], timeout=10)
        ftp.login(user=username, passwd=user_passwd)
        global BATCH
        global LOCK
        from venc3.prompt import get_formatted_message
        pwd = blog_configuration["paths"]["ftp"]
        to_create = BATCH[session_id]["to_create"]
        to_delete = BATCH[session_id]["to_delete"]
        while len(to_create.keys()):
            for item in sorted(to_create.keys(), key=lambda x:to_create[x]["priority"], reverse=True):
                path = item.split('/')
                if len(path) == 1 or not cross_thread_lookup('/'.join(path[:-1]), "to_create"):
                    try:
                        if to_create[item]["type"] == "dir":
                            ret = ftp.mkd(pwd+item)
                            
                        else:
                            ret = ftp.storbinary("STOR "+pwd+item, open("blog/"+item, 'rb'))
                            
                    except Exception as e:
                        ret = '\033[0m\033[91m'+str(e)
                        
                    LOCK.acquire()
                    notify(("exception_place_holder", "FTP SESSION {0}: {1}: ".format(session_id, pwd+('/' if item[0] != '/' else '')+item)+str(ret)))
                    del to_create[item]
                    LOCK.release()    

                break                    

        while len(to_delete.keys()):
            for item in sorted(to_delete.keys(), key=lambda x:to_delete[x]["priority"], reverse=True):
                if not cross_thread_lookup(item, "to_delete"):
                    try:
                        if to_delete[item]["type"] == "dir":
                            ret = ftp.rmd(pwd+item)
                            
                        else:
                            ret = ftp.delete(pwd+item)
                            
                    except Exception as e:
                        ret = '\033[0m\033[91m'+str(e)
                        
                    LOCK.acquire()
                    notify(("exception_place_holder", "FTP SESSION {0}: {1}: ".format(session_id, pwd+('/' if item[0] != '/' else '')+item)+str(ret)))
                    del to_delete[item]
                    LOCK.release() 
                    
                break

        ftp.quit()
        
def get_local_files(directory):
    items = list()
    for item in os.listdir(directory):
        items.append(
            (
                directory+"/"+item,
                {
                    "type": "dir" if os.path.isdir(directory+"/"+item) else "file",
                    "modify": os.path.getmtime(directory+"/"+item),
                    "size": os.path.getsize(directory+"/"+item)
                }
            )
        )
        
        if items[-1][1]["type"] == "dir":
            items += get_local_files(directory+"/"+item)
            
    return items
        
def get_remote_files(ftp):
    items = list()
    for item in ftp.mlsd():
        filename, info = item
        if not filename in [".", ".."]:
            if info["type"] == "dir":
                cwd = ftp.pwd()
                ftp.cwd(ftp.pwd()+"/"+filename)
                items.append((ftp.pwd(), info))
                items += get_remote_files(ftp)
                ftp.cwd(cwd)
                
            else:
                pwd = ftp.pwd()
                items.append((pwd+("/" if len(pwd) > 1 else "")+filename, info))
            
    return items

def print_ftp_response(response):
        notify(
            (
                "exception_place_holder",
                str(response).replace("\n","\n      ")
            )
        )
        
def remote_copy(params):
    import getpass

    from venc3.datastore.configuration import get_blog_configuration
    from venc3.l10n import messages
    
    blog_configuration = get_blog_configuration()
    
    if not "ftp_host" in blog_configuration.keys():
        from venc3.prompt import die
        die(("undefined_variable", "ftp_host", "blog_configuration.yml"))
        
    if len(blog_configuration["ftp_host"]) == 0:
        from venc3.prompt import die
        die(("invalid_value_in_setting", blog_configuration["ftp_host"], "ftp_host"))
    
    try:
        ftp = ftplib.FTP()
        ftp.encoding = blog_configuration["ftp_encoding"]
        print_ftp_response(ftp.connect(blog_configuration["ftp_host"], blog_configuration["ftp_port"], timeout=10))
        print_ftp_response(ftp.sendcmd("FEAT"))
        username = input("VenC: "+messages.username)
        user_passwd = getpass.getpass(prompt="VenC: "+messages.user_passwd)
    
        if not "ftp" in blog_configuration["paths"].keys():
            from venc3.prompt import die
            die(("undefined_variable", "ftp", "blog_configuration.yml"))
          
        print_ftp_response(ftp.login(user=username,passwd=user_passwd))
        print_ftp_response(ftp.cwd(blog_configuration["paths"]["ftp"]))
        notify(("sync_ftp_directory",))
        ftp_base_path = blog_configuration["paths"]["ftp"]
        local_files = { item[0][len(os.getcwd()+"/blog"):] : item[1] for item in get_local_files(os.getcwd()+"/blog") }
        remote_files = { item[0][len(ftp_base_path)+(1 if len(ftp_base_path) > 1 else 0):] : item[1] for item in get_remote_files(ftp) }
        ftp.quit()

        to_delete = {}
        to_create = {}
        
        for item in local_files.keys():
            if not item in remote_files.keys() or (remote_files[item]["type"] != "dir" and local_files[item]["size"] != int(remote_files[item]["size"])):
                to_create[item] = local_files[item]
                to_create[item]["priority"] = 0
        
        for item in remote_files.keys():
            if len(item) and not item in local_files.keys():
                to_delete[item] = remote_files[item]
                to_delete[item]["priority"] = 0

        if len(to_delete.keys()) == 0 and len(to_create.keys()) == 0:
            notify(("nothing_to_do",))
            return
            
        # INIT BATCHS
        global BATCH
        to_create_chunk_size = (len(to_create.keys()) // blog_configuration["ftp_sessions"]) + 1
        to_delete_chunk_size = (len(to_delete.keys()) // blog_configuration["ftp_sessions"]) + 1
        worker_threads = []
        from threading import Thread
        for session_id in range(0, blog_configuration["ftp_sessions"]):
            BATCH[session_id] = {
                # The following code is so DREADFUL it becomes cute. No ? Well... Maybe not...
                "to_create": { tuple(to_create.keys())[0] : to_create.pop(tuple(to_create.keys())[0]) for i in range(0, to_create_chunk_size if to_create_chunk_size < len(to_create.keys()) else len(to_create.keys())) },
                "to_delete": { tuple(to_delete.keys())[0] : to_delete.pop(tuple(to_delete.keys())[0]) for i in range(0, to_delete_chunk_size if to_delete_chunk_size < len(to_delete.keys()) else len(to_delete.keys())) }
            }
                
            worker_threads.append(
                Thread(
                    target=ftp_session, args=(session_id, blog_configuration, username, user_passwd)
                )
            )
            
        for thread_worker in worker_threads:
            thread_worker.start()

        for thread_worker in worker_threads:
            thread_worker.join()
            
    except Exception as e:
        from venc3.prompt import die
        die(("exception_place_holder", str(e)))
