from flask import Flask, request,render_template
import json
from datetime import datetime
import re
import pandas as pd
import random
from config import config
from utils import web_utils

app = Flask(__name__)

# game_url = https://store.steampowered.com/app/{ID}/{Name}
applist = pd.read_csv("exist_game.csv")

selected_ids = random.choices(applist.AppID,k=50)
print(selected_ids)
msg = web_utils.gen_msg(applist,config.max_title_len,selected_ids)
@app.route('/')
@app.route('/index')
def index():

    return render_template("index.html",names = msg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
