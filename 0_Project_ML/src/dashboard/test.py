import streamlit as st

import pandas as pd

import requests
import webbrowser

import sys
import os

# Helpers
abspath = os.path.abspath
dirname = os.path.dirname
sep = os.sep

current_folder = dirname(abspath(__file__))
for i in range(1): current_folder = dirname(abspath(current_folder))
print(current_folder)