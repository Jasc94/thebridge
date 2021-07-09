from flask import Flask, request, render_template, Response

import pandas as pd

import sys, os, argparse

# Helpers
abspath = os.path.abspath
dirname = os.path.dirname
sep = os.sep

# Path modification
current_folder = dirname(abspath(__file__))
for i in range(1): current_folder = dirname(abspath(current_folder))
sys.path.append(current_folder)

# Utils
import utils.folder_tb as fo
import utils.apis_tb as ap


server_password = "jonathan"

##################################################### FLASK FUNCTIONS #####################################################
##### RUN THE SERVER
if __name__ == "__main__":
    # Enter password through terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", type = str,
                        help = "password to run the server", required = True)
    args = parser.parse_args()

    # if password is ok, run the server
    if args.password == server_password:
        ap.main()
    else:
        print("Wrong password... Please try again")