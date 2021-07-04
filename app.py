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
applist = pd.read_csv(config.game_info_path)


selected_ids = random.choices(applist.AppID, k=1000)
msg = web_utils.gen_msg(applist, config.max_title_len, selected_ids)
current_id = config.num_show
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",buffer = msg[:config.num_show])

@app.route('/loadmore')
def load_more():
    global current_id
    outputs = ""
    for i in range(config.num_more_line*3):
        current_item = msg[current_id+i]
        name,pic,price,url = current_item
        outputs += web_utils.load_more_formatting(pic=pic,name=name,price=price,
                                                  url= url)
    current_id += config.num_more_line*3
    return outputs

@app.route('/click')
def click():
    text = request.args.get('msg')
    # TODO 通过用户点击更新推荐列表
    print(text)
    return 'None'
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
