#!/usr/bin/env python3
#
# RestMonitor.py - A proof of concept script to monitor the
# health of the webservers specified in the input file.
#
# This script requires Python V3.6.0 or higher and may fail with
# earlier versions.
#
# Save this file, the WebServerList file and the config file to
# the local directory and run from that directory with:
#
# python3 RestMonitor.py
#
#############################
#
# Copyright 2016
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Author:  Tom Sweeney
# Date:    12/26/2016
# Email:   tsweeney@alum.wpi.edu
#

import logging
from   logging.handlers import SysLogHandler
import sys
import urllib.parse
import urllib.request
import json
import getopt
import time
import smtplib
from  configparser import SafeConfigParser
import ssl

####
# Constants
####
LOG = logging.getLogger(__name__)
LOG_FILE = "RestMonitor.log"
CONFIG_FILE = "RestMonitor.config"
CONFIGDATA = SafeConfigParser()
SSL_UNVERIFIED_CONTEXT=ssl._create_unverified_context()
DEFAULT_CONTINUE_ON_ERROR = True

####
# Global Variables
####
continue_on_error = DEFAULT_CONTINUE_ON_ERROR
host_ip = ""
sender_email_address = ""
receiver_email_address = ""


def start_stdout_logging():
    ###
    # Initialize logging to console window.
    ###
    LOG.setLevel(logging.DEBUG)

    stdoutFormatter = logging.Formatter('%(message)s')
    stdOutHandler = logging.StreamHandler(sys.stdout)
    stdOutHandler.setLevel(logging.DEBUG)
    stdOutHandler.setFormatter(stdoutFormatter)

    LOG.addHandler(stdOutHandler)


def read_config_file(configFile):

    LOG.debug("\n############")
    LOG.info("Reading Configuration File")
    LOG.debug("############\n")

    try:
        CONFIGDATA.read(configFile)
    except Exception as e:
        LOG.error("Error reading config file")
        LOG.error(str(e))
        sys.exit()

    global continue_on_error
    global max_loops
    global sleep_time_seconds
    global sender_email_address
    global receiver_email_address

    try:
        continue_on_error = CONFIGDATA.getboolean('DEFAULT', 'CONTINUE_ON_ERROR')
        max_loops = CONFIGDATA.getint('DEFAULT', 'MAX_LOOPS')
        sleep_time_seconds = CONFIGDATA.getint('DEFAULT', 'SLEEP_TIME_SECONDS')
        sender_email_address = CONFIGDATA.get('DEFAULT', 'SENDER_EMAIL_ADDRESS')
        receiver_email_address = CONFIGDATA.get('DEFAULT', 'RECEIVER_EMAIL_ADDRESS')
    except Exception as e:
        LOG.error("Error reading data from the config file, please verify the file.\n")
        LOG.error(str(e))
        pass


def start_logfile_logging():
    ###
    # Initialize logging to log file.
    ###

    logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logFile = None

    try:
        logFile = CONFIGDATA.get('DEFAULT', 'LOG_FILE_PATH')
    except Exception as e:
        pass

    if not logFile:
        LOG.debug("Unable to read log file location from the config file, using default location.\n")
        logFile = LOG_FILE

    logHandler = logging.FileHandler(logFile)
    logHandler.setLevel(logging.INFO)
    logHandler.setFormatter(logFormatter)

    LOG.addHandler(logHandler)


def logout_exit(authToken, errorCode=0):
    """
    Logout and call sys.exit with error
    """
    sys.exit(errorCode)


def handle_nonfatal_error(authToken, exception, errorCode=2):
    """
    Show the error and continue or exit dependent
    on the value in the CONTINUE_ON_ERROR property
    """
    LOG.error(str(exception))
    if continue_on_error:
        LOG.info("Continuing since CONTINUE_ON_ERROR is configured as True.")
        return
    logout_exit(authToken, errorCode)


def send_email_notification(subject, messageBody):

    # Send the message via smtp.  This will need to
    # be changed to fit the local smtp server or
    # with real gmail creds.
    message = """\
From: %s
To: %s
Subject: %s
   
%s
""" % (sender_email_address, receiver_email_address, subject, messageBody)

    try: 
        #server = smtplib.SMTP('localhost')
        server = smtplib.SMTP("smtp.gmail.com:587")

        server.starttls()
        server.login('username@gmail.com', 'gmailpassword')
        server.sendmail(sender_email_address, receiver_email_address, message)
        server.quit()
    except Exception as e:
        LOG.info("Unable to send e-mail")


def verify_web_server(authToken, webserver):
    """
    Do a get for the provided webserver.
    webserver - webserver to check, should be the full address
    authtoken - authToken for the service, currently unused
    Returns the json response from the server and time for the request
    Raise exceptions if any REST API call failed
    """
    url = 'https://' + webserver
    headers = {'Accept':'application/json', 'Content-type':'application/json', 'auth': authToken}
    req = urllib.request.Request(url, None, headers)
    req.method = 'GET'

    webserverJson = []
    requestTime = 0
    try:
        startTime = time.time()
        f1 = urllib.request.urlopen(req, context=SSL_UNVERIFIED_CONTEXT)
        requestTime = time.time() - startTime
        for x in f1:
            webserverJson = json.loads(x.decode('utf-8'))
        f1.close()
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        send_email_notification("Rest System WebService Problem Alert [HTTPError]", "Server Issue with:" + webserver)
        LOG.error("Error [" + str(e.code) + "] for webserver: " + webserver)
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        send_email_notification("Rest System WebService Problem Alert [URLError]", "Server Issue with:" + webserver)
        LOG.error("URLError for webserver: " + webserver)
    except Exception as e:
        send_email_notification("Rest System WebService Problem Alert [Exception]", "Server Issue with:" + webserver)
        LOG.error("Error retrieving detailed information for webserver:" + webserver)

    if (requestTime > 2):
        send_email_notification("Rest System WebService Slowness Alert", "GET call exceeded desired requested time on Server:" + webserver)

    return webserverJson, requestTime



def usage():
    print ("\n")
    print ("Usage: " + sys.argv[0] + " -h | --help\n")
    print ("       " + sys.argv[0] + " [-c | --config config-file-path]\n")


####
# Main function
####
def main(argv):

    global host_ip
    configFile = CONFIG_FILE

    start_stdout_logging()

    try:
        opts, args = getopt.getopt(argv, "hc", ["help", "config="])
    except getopt.GetoptError as e:
        LOG.error("Error: " + e.msg + "\n")
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--config"):
            configFile = arg
        else:
            usage()
            sys.exit(2)

    LOG.info("Using this config file: " + configFile)

    #####
    # Read in properties from config file
    #####
    read_config_file(configFile)

    start_logfile_logging()

    authToken = ""
    for i in range(max_loops):
        webserverListFile = open('WebServerList.txt', "r")

        #Build list of webservers to check from WebServerList.txt file
        webservers = []
        for line in webserverListFile:
            if (line[0] != '#'):  # remove comment lines
                webservers.append(line.rstrip('\r\n'))
        webserverListFile.close()
    
        for webserver in webservers:
            LOG.info("Verifying Webserver [" + webserver + "]")
            returnJson, requestTime = verify_web_server(authToken, webserver)
            LOG.info ("Request Time: " + str(requestTime) + " seconds, Return Json: " + json.dumps(returnJson))
            print("\n") 

        if (i < max_loops - 1):
            print("Sleeping for " + str(sleep_time_seconds) + " seconds...", flush=True)
            time.sleep(sleep_time_seconds)

    print("\nRestMonitor Run completed")

if __name__ == "__main__":
    main(sys.argv[1:])

