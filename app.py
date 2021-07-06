from flask import Flask, request, render_template
import re
import pandas as pd
from config import config
from utils import web_utils
from datetime import datetime
import numpy as np
import json
import logging
import os
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if not os.path.exists(config.working_path + config.logging_path):
    os.mkdir(config.working_path + config.logging_path)
handler = logging.FileHandler(config.working_path + config.logging_path + "/server_log.txt")
handler.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(handler)

app = Flask(__name__)

df_svd = web_utils.item_feature_loading(svd_path=config.svd_path)

# load item feature
df_App = pd.read_csv(config.game_info_path).set_index("AppID")


@app.route('/')
@app.route('/index')
def index():
    items, rating_map = web_utils.init_user_page(uid="kevin",
                                                 df_App=df_App,
                                                 max_title_len=config.max_title_len,
                                                 num_show=config.num_show,
                                                 seed=config.seed)
    with open(f"{config.R_ui_path}kevin.json", "w")as fp:
        json.dump(rating_map, fp=fp, indent=2)

    return render_template("index.html", buffer=items, current_user="kevin")


@app.route('/loadmore', methods=["get"])
def load_more():
    uid = request.args.get("uid")
    with open(f"{config.R_ui_path}{uid}.json", "r")as fp:
        rating_map = json.load(fp=fp)
    s_ids = sorted(rating_map, key=lambda x: rating_map[x])
    msg = web_utils.gen_msg(df_App, config.max_title_len, s_ids)
    items = [msg.pop() for _ in range(config.num_more_load)]

    for sid in [str(x[0]) for x in items]:
        rating_map.pop(sid)
    with open(f"{config.R_ui_path}{uid}.json", "w")as fp:
        json.dump(rating_map, fp=fp, indent=2, sort_keys=False)
    print("len rating ", len(rating_map))
    outputs = ""
    for current_item in items:
        Appid, name, pic, price, url, genre = current_item
        outputs += web_utils.load_more_formatting(pic=pic, name=name, price=price,
                                                  url=url, appid=Appid, other=genre)
    return outputs


@app.route('/update_like', methods=['post'])
def update_like():
    data = request.form
    logger.info(f"> user {data.get('uid')} {data.get('type')} "
                f"{data.get('AppName')}, time: {datetime.now()}")

    with open(f"{config.R_ui_path}{data.get('uid')}.json", "r")as fp:
        rating_map = json.load(fp)
    rating_map = web_utils.update_item_weight(data.get('aid'),
                                              rating_map,
                                              df_svd=df_svd,
                                              top_k=config.top_knn,
                                              temperature=config.temperature,
                                              type=data.get('type'))
    with open(f"{config.R_ui_path}{data.get('uid')}.json", "w")as fp:
        json.dump(rating_map, fp=fp, indent=2)
    return 'None'


@app.route('/update_uid', methods=["post"])
def update_uid():
    uid = request.form.get('uid')
    # TODO 用户个性化展示
    items, rating_map = web_utils.init_user_page(uid=uid,
                                                 df_App=df_App,
                                                 max_title_len=config.max_title_len,
                                                 num_show=config.num_show,
                                                 seed=config.seed)
    with open(f"{config.R_ui_path}{uid}.json", "w")as fp:
        json.dump(rating_map, fp=fp, indent=2)
    return render_template("index.html", buffer=items, current_user=str(uid))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
