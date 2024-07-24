import json
import os
import shutil
import subprocess
import sys
import threading
from readJson import read_json_file
from settingsManager import HISTORY_FILENAME, PROMPTS_FOLDER, TEMPLATES_FOLDER

history = HISTORY_FILENAME
prompts_dictionary = {}
possible_prompts = []
