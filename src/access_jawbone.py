'''
    .. module:: access_jawbone
    
    :synopsis: Use python to connect to Jawbone UP API, request, load, and process JSON data
    
    .. moduleauthor:: Jocelyn T. Dunn <joceydunn2@gmail.com>
    
'''

import sys
import urllib
import urllib2
import json
import datetime

def args_store(args):
    
    '''
        ``args_store`` receives command-line arguments
        
        run command: ``python get_data.py user_email user_password data_url``
        
            :param file: ``get_data.py``, create script similar to ``get_sleep_data.py`` example
            :param arg1: ``user_email``
            :param arg2: ``user_password``
            :param arg3: ``data_url``, visit `Jawbone Data Endpoints <https://jawbone.com/up/developer/endpoints>`_ to see options
    '''
    
    user = str(args[1])
    passwd = str(args[2])
    link = str(args[3])
    return user, passwd, link

def authenticate(user, passwd):
    
    '''
        ``aunthenticate`` provides secure access to Jawbone user data
        
            :param input_user: email address from **arg1**
            :param input_password: password from **arg2**
            :returns: security token that is required for accessing Jawbone user data
    '''
    
    username = user
    password = passwd
    url = 'https://jawbone.com/user/signin/login'
    params = urllib.urlencode({
                              'email': username,
                              'pwd': password,
                              'service': 'nudge'
                              })
    
    tokenresponse = urllib2.urlopen(url, params)
    data = json.load(tokenresponse)
    token_num = data["token"]
    return token_num

def get_data(link, token):
    
    '''
        ``get_data`` is envoked to "GET" JSON data from Jawbone API
        
            :param url: data request link from **arg3**, see options at `Jawbone Data Endpoints <https://jawbone.com/up/developer/endpoints>`_
            :param token: security token (returned from 'authenticate' function)
            :returns: ``requested Jawbone data in JSON format``
    '''
    
    url = link
    token_num = token
    opener = urllib2.build_opener()
    opener.addheaders.append(('x-nudge-token', token_num))
    dataresponse = opener.open(url)
    data = json.load(dataresponse)
    return data

def format(entry):
    
    '''
        ``format`` is helpful for converting epoch timestamp into readable datetime format
        
            :param entry: epoch timestamp
            :returns: ``datetime in 'YYYY-MM-DD HH:MM:SS' format``
    '''
    
    t = datetime.datetime.fromtimestamp(float(json.dumps(entry))).strftime('%Y-%m-%d %H:%M:%S')
    f_entry = str(t)
    return f_entry

