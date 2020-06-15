#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from requests.auth import HTTPBasicAuth
import requests
import configparser

# local maven repository
upload_repo_path = None
# nexus server host
base_url = None
# nexus account
username = None
# nexus password
password = None
# nexus upload url
repo_server_url =None
# nexus retrival url
repo_browse_url = None
# upload specified file by dependencies.txt [True/False]
specified = None

def doUpload():
    if specified==True :
        dependencies = getSpecifiedDependencies()
        for path in dependencies:
            uploadLocalRepo(path)
    else:
        uploadLocalRepo(upload_repo_path)

def uploadLocalRepo(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if toUpload(root, name):
                print('uploading:' + root + '/' + name)
                uploadFile(root,name)

def toUpload(root, name):
    if name.endswith('.jar') or name.endswith('.pom'):
        root = root.replace('\\','/')
        url = repo_browse_url + root[len(upload_repo_path):len(root)]
        response = requests.get(url)
        if name in response.text:
            return False
        else:
            return True
    return False

def uploadFile(root, name):
    if name.endswith('.jar') or name.endswith('.pom'):
        root = root.replace('\\','/')
        url = repo_server_url + root[len(upload_repo_path):len(root)] + '/' + name
        path = root + '/' + name
        response = requests.put(url,data=open(path,'rb').read(), auth=HTTPBasicAuth(username,password))
        print(response)

def getSpecifiedDependencies():
    with open("dependencies.txt", "r", encoding="utf8") as f:
        return f.readlines()



if __name__=='__main__':
    cf = configparser.RawConfigParser()
    cf.read("config.ini", encoding="utf-8")
    cf.options("config")
    upload_repo_path = cf.get("config", "upload_repo_path")
    base_url = cf.get("config", "base_url")
    username = cf.get("config", "username")
    password = cf.get("config", "password")
    repo_server_url = cf.get("config", "repo_server_url")
    repo_browse_url = cf.get("config", "repo_browse_url")
    specified = cf.get("config", "specified")
    doUpload()
    