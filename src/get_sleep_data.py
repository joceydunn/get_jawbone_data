'''
    .. module:: get_sleep_data

    :synopsis: Example code to demonstrate how to "GET" JSON data from Jawbone UP API
    
    .. moduleauthor:: Jocelyn T. Dunn <joceydunn2@gmail.com>
    
'''

import sys
from access_jawbone import *

def main():
    
    '''
        To compile this example code, run the command: ``python get_sleep_data.py user_email user_password https://jawbone.com/nudge/api/users/@me/sleeps? &``
        
    * **EXAMPLE_1 :** "GET" the bulk of sleep event data
        * Use :py:func:`access_jawbone.args_store` to receive the command-line arguments
            * arg1 - ``user_email`` associated with Jawbone account
            * arg2 - ``user_password`` associated with Jawbone account
            * arg3 - ``data request url`` for this example ``https://jawbone.com/nudge/api/users/@me/sleeps?``
        * Run :py:func:`access_jawbone.authenticate` for secure access to jawbone data
            :returns: ``security token``
        * Employ :py:func:`access_jawbone.get_data` to "GET" sleep data from Jawbone API
            :returns: ``user xid, event xid, date, sleep time, awake time, number of awakenings, duration of sleep event, quality score, etc.``
        * Operate on JSON data dictionary and use JSON.dumps to print in readable format
        * Convert timestamps into a readable format with :py:func:`access_jawbone.format` function
        * Create list of sleep events 'xid' which serve as the input for **EXAMPLE_2**
            :returns: ``'xid' for each sleep event``
            
    * **EXAMPLE_2 :** "GET" detailed data about sleep phases
        * Operate on the list of sleep events 'xid' obtained in **EXAMPLE_1**
        * Insert sleep event ``xid[item]`` into detailed data request url ``'https://jawbone.com/nudge/api/sleeps/' + xid[item] + '/ticks'``
        * Employ :py:func:`access_jawbone.get_data` to "GET" detailed sleep phase data
            :returns: ``timing of sleep phases (1=awake, 2=light sleep, 3=sound sleep)``

    '''

    #EXAMPLE_1: Get sleep data from url 'https://jawbone.com/nudge/api/users/@me/sleeps?'

    # Use 'args_store' function to save the command-line arguments: :arg1:, :arg2:, :arg3:
    [user, passwd, link] = args_store(sys.argv)

    # Run 'authenticate' function for access to jawbone data
    token = authenticate(user, passwd)

    # Run 'get_data' function to submit JSON request to jawbone API
    # Note adding '&limit=50' to data_url changes the output limit (default is limit=10)
    link = link + ('&limit=15')
    data = get_data(link, token)

    # Operate on the returned JSON data as a python dictionary
    # Note that, for this data_url, the returned JSON data contains "meta" and "data"
    meta = data['meta']
    data2 = data['data']
    
    # Use JSON.dumps to print the resturned JSON data in a readable format
    # Use 'format' function to convert timestamps into a readable format

    print '\n\n' + "SLEEP DATA for " + user
    print "Fetched on " + str(format(meta['time']))

    # Print "meta"
    print '\n' + "META"
    print json.dumps(meta, indent=4, sort_keys=True)

    # Print keys of "data" dictionary
    print '\n' + "KEYS"
    print json.dumps(data2.keys(), indent=4, sort_keys=True)

    # Note that, for this "data", the keys include "size", "link", and "items"
    items = data['data']['items']
    size = data['data']['size']

    # Print the "size" (or number of "items")
    print '\n' + "SIZE"
    print json.dumps(size, indent=4, sort_keys=True)

    # Print the most recent sleep event (which is the first "item")
    item = 0
    print '\n' + "ITEM " + str(item+1) + " of " + json.dumps(size, indent=4, sort_keys=True)
    print json.dumps(items[item], indent=4, sort_keys=True)

    # Store the sleep event 'xid' for each "item"
    print '\n' + "LIST OF SLEEP EVENTS: 'xid' for each ITEM"
    # Note that 'xid' are used in EXAMPLE_2 to get more detailed data about each sleep event
    xid = []
    for row in items:
        xid.append(row['xid'])
    
    print json.dumps(xid, indent=4, sort_keys=True)

    #EXAMPLE_2: Get sleep phases, by adding event 'xid' into url 'https://jawbone.com/nudge/api/sleeps/[xid]/ticks'

    # Need 'xid' from the list of sleep events obtained in EXAMPLE_1
    item = 0
    # Add 'xid' to the data_url request for detailed information about each sleep event
    link2 = str('https://jawbone.com/nudge/api/sleeps/' + xid[item] + '/ticks')

    # Run 'get_data' functon with this new data request link
    data2 = get_data(link2, token)
    print '\n' + "SLEEP PHASES for ITEM " + str(item+1)
    print json.dumps(data2, indent=4, sort_keys=True)

if __name__ == '__main__':
    
    main()

    