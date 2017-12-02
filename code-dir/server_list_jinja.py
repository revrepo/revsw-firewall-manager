#!/usr/bin/python
"""

 REV SOFTWARE CONFIDENTIAL

 [2013] - [2016] Rev Software, Inc.
 All Rights Reserved.

 NOTICE:  All information contained herein is, and remains
 the property of Rev Software, Inc. and its suppliers,
 if any.  The intellectual and technical concepts contained
 herein are proprietary to Rev Software, Inc.
 and its suppliers and may be covered by U.S. and Foreign Patents,
 patents in process, and are protected by trade secret or copyright law.
 Dissemination of this information or reproduction of this material
 is strictly forbidden unless prior written permission is obtained
 from Rev Software, Inc.

"""

import sys
import traceback
import json
import requests
from pprint import pprint, pformat
import logging
import logging.handlers
import jinja2

# Settings
BASE_INFRADB_URL = "https://infradb.revsw.net"
USER = "apiro"
PASSWORD = "7pmlZ5axCwYe"
LOGGING_LEVEL = logging.DEBUG

# Setup logger
logging.basicConfig(format='%(name)s %(levelname)s %(asctime)-15s %(message)s')
logger = logging.getLogger('server_list_jinja')
logger.setLevel(LOGGING_LEVEL)
syslog_formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')
syslog_handler = logging.handlers.SysLogHandler(address = '/dev/log')
syslog_handler.setFormatter(syslog_formatter)
logger.addHandler(syslog_handler)

# Get arguments
try:
    TEMPLATE_FILE = sys.argv[1]
    OUTPUT_FILE = sys.argv[2]
except IndexError:
    logger.fatal("Please provide the name of the jinja template as the first parameter and the output file as the second parameter")
    exit(1)
    
# Get server list
try:
    server_list_url = "%s/api/servers_list/" % BASE_INFRADB_URL
    # disabling warnings because we are using untrusted certificate
    try:
        requests.packages.urllib3.disable_warnings()
    except:
        pass
    server_list_json = requests.get(server_list_url, auth=(USER, PASSWORD),verify=False)
except:
        logger.fatal("Failed getting server list from API, reason: %s" % sys.exc_info()[0])
        logger.fatal(traceback.format_exc())
        logger.fatal("Aborting")
        exit(1)       

if server_list_json.status_code != 200:
    logger.fatal("%d status code response from API, aborting." % server_list_json.status_code)
    exit(1)

try:
    server_list = json.loads(server_list_json.content)
except:
        logger.fatal("Failed decoding response from API, reason: %s" % sys.exc_info()[0])
        logger.fatal(traceback.format_exc())
        logger.fatal("Aborting")
        exit(1)

# Load jinja2 template
try:
    template_loader = jinja2.FileSystemLoader(searchpath="/")
    jinja_env = jinja2.Environment(loader=template_loader)
    jinja_template = jinja_env.get_template(TEMPLATE_FILE)
    jinja_output = jinja_template.render(dict({'server_list':server_list}))
except:
        logger.fatal("Failed rendering jinja template, reason: %s" % sys.exc_info()[0])
        logger.fatal(traceback.format_exc())
        logger.fatal("Aborting")
        exit(1)

# Writing output file
try:
    f = open(OUTPUT_FILE,"w")
    f.write(jinja_output)
    f.close()
except:
        logger.fatal("Failed creating output file, reason: %s" % sys.exc_info()[0])
        logger.fatal(traceback.format_exc())
        logger.fatal("Aborting")
        exit(1)
