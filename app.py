from flask import Flask, request, render_template
import re
import pandas as pd
import random
from config import config
from utils import web_utils
from datetime import datetime


app = Flask(__name__)

# init app data
applist = pd.read_csv(config.game_info_path).set_index("AppID")


selected_ids = random.choices(applist.index, k=1000) # test
selected_ids[0] = 524490 # test
msg = web_utils.gen_msg(applist, config.max_title_len, selected_ids)
current_id = config.num_show


@app.route('/')
@app.route('/index')
def index():
    # TODO 初始化，展示热门商品 most pop
    return render_template("index.html", buffer=msg[:config.num_show])


@app.route('/loadmore')
def load_more():
    global current_id
    outputs = ""
    for i in range(config.num_more_line * 3):
        current_item = msg[current_id + i]
        name, pic, price, url = current_item
        outputs += web_utils.load_more_formatting(pic=pic, name=name, price=price,
                                                  url=url)
    current_id += config.num_more_line * 3
    return outputs


@app.route('/click')
def click():
    text = request.args.get('msg')
    # TODO 通过用户点击更新推荐列表，加大同类商品比重
    print(text)
    print(datetime.now())
    return 'None'


@app.route('/update_uid',methods=["post"])
def update_uid():
    user = request.form.get('uid')
    print(user)
    # TODO 用户个性化展示
    # user_interest_ids = get_user_interest(user)
    selected_ids[0] = 791950
    # 791950 / Hiking_Simulator_2018
    user_interest = web_utils.gen_msg(applist, config.max_title_len, selected_ids)
    return render_template("index.html", buffer=user_interest[:config.num_show])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
