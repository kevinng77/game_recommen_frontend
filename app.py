from flask import Flask, request, render_template
import re
import pandas as pd
import random
from config import config
from utils import web_utils
from datetime import datetime
import numpy as np


app = Flask(__name__)

df_svd = web_utils.item_feature_loading(svd_path=config.svd_path)

np.random.seed(config.seed)
# load item feature
df_App, rating_map = web_utils.item_info_loading(game_info_path=config.game_info_path)
selected_ids = sorted(rating_map, key=lambda x: rating_map[x])
msg = web_utils.gen_msg(df_App, config.max_title_len, selected_ids)
init_items = [msg.pop() for _ in range(config.num_show)]


@app.route('/')
@app.route('/index')
def index():
    global df_App, rating_map, msg
    np.random.seed(config.seed)
    # load item feature
    df_App, rating_map = web_utils.item_info_loading(game_info_path=config.game_info_path)
    selected_ids = sorted(rating_map, key=lambda x: rating_map[x])
    msg = web_utils.gen_msg(df_App, config.max_title_len, selected_ids)
    # 初始化商品
    init_items = [msg.pop() for _ in range(config.num_show)]
    for sid in [x[0] for x in init_items]:
        rating_map.pop(sid)
    return render_template("index.html", buffer=init_items, current_user="kevin")


@app.route('/loadmore')
def load_more():
    global rating_map
    items = [msg.pop() for _ in range(config.num_more_load)]
    for sid in [x[0] for x in items]:
        rating_map.pop(sid)
    outputs = ""
    for current_item in items:
        Appid, name, pic, price, url, genre = current_item
        outputs += web_utils.load_more_formatting(pic=pic, name=name, price=price,
                                                  url=url, appid=Appid, other=genre)
    return outputs


@app.route('/click', methods=['post'])
def click():
    global rating_map, msg
    Appid = request.form.get('aid')
    AppName = request.form.get('AppName')
    print(Appid, AppName)
    print(datetime.now())
    rating_map = web_utils.update_item_weight(Appid,
                                              rating_map,
                                              df_svd=df_svd,
                                              top_k=config.top_knn,
                                              temperature=config.temperature,
                                              type="click")
    s_ids = sorted(rating_map, key=lambda x: rating_map[x])
    msg = web_utils.gen_msg(df_App, config.max_title_len, s_ids)
    return 'None'


@app.route('/update_like', methods=['post'])
def update_like():
    global rating_map, msg
    Appid = request.form.get('aid')
    AppName = request.form.get('AppName')
    like_type = request.form.get('type')
    print(Appid, AppName)
    print(datetime.now())
    rating_map = web_utils.update_item_weight(Appid,
                                              rating_map,
                                              df_svd=df_svd,
                                              top_k=config.top_knn,
                                              temperature=config.temperature,
                                              type=like_type)
    s_ids = sorted(rating_map, key=lambda x: rating_map[x])
    msg = web_utils.gen_msg(df_App, config.max_title_len, s_ids)
    return 'None'

@app.route('/update_uid', methods=["post"])
def update_uid():
    user = request.form.get('uid')
    print(user)
    # TODO 用户个性化展示
    # user_interest_ids = get_user_interest(user)
    selected_ids[0] = 791950
    # 791950 / Hiking_Simulator_2018
    user_interest = web_utils.gen_msg(df_App, config.max_title_len, selected_ids)
    return render_template("index.html", buffer=user_interest[:config.num_show], current_user=str(user))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
