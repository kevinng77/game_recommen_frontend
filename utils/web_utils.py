import numpy as np
import pandas as pd


def item_info_loading(game_info_path):
    # load app info
    df_App = pd.read_csv(game_info_path).set_index("AppID")
    app_rate = np.random.rand(len(df_App))
    AppIDs = list(df_App.index)
    rating_map = {AppIDs[i]: app_rate[i] for i in range(len(AppIDs))}
    return df_App, rating_map


def item_feature_loading(svd_path):
    # load item feature
    df_svd = pd.read_csv(svd_path, index_col=0)
    return df_svd


def process_title(title, max_title_len):
    if len(title) > max_title_len:
        return title[:max_title_len - 3] + "..."
    else:
        return title


def gen_msg(df_app, max_title_len, selected_ids):
    """
    :param max_title_len: max length for title to show.
    :param df_app: data frame
    :param selected_ids: AppID to recommended
    :return: list of tuple (AppName, picture, )
    """
    df_selected_game = df_app.loc[selected_ids]
    l_name = df_selected_game.AppName.tolist()
    l_name = [process_title(x, max_title_len) for x in l_name]
    l_view = df_selected_game.Picture.tolist()
    l_url = df_selected_game.url.tolist()
    l_price = df_selected_game.final_price.tolist()
    l_genre = df_selected_game.Genre.tolist()
    msg = list(zip(selected_ids, l_name, l_view, l_price, l_url, l_genre))
    return msg


def load_more_formatting(pic, name, price, url, appid, other="todo: adding tag"):
    template = f'<div class="item">' \
               f'<div class="img_block">' \
               f'<img src="{pic}" alt="item" />' \
               f'</div><div class="name_block">' \
               f'<a>{name}</a></div>' \
               f'<div class="game_tag">{other}' \
               f'<a class="dislike" onclick="update_like(\'{appid}\',\'{name}\',\'dislike\')">' \
               f'<img src="static/dislike.png"></a>' \
               f'<a class="like" onclick="update_like(\'{appid}\',\'{name}\',\'like\')">' \
               f'<img src="https://cdn0.iconfinder.com/data/icons/twitter-ui-flat/48/Twitter_UI-24-256.png">' \
               f'</a></div><div>' \
               f'<a  class="price"><em>${price}</em></a>' \
               f'<a class="details" ' \
               f'onclick="load_detail(\'{url}\',\'{appid}\',\'{name}\')">' \
               f'<em>Details>></em></a></div></div>'
    return template


def update_item_weight(appid, rating_map, df_svd, top_k, temperature, type="click"):
    """
    update recommend item weight when user click
    :return:
    """
    print(type)
    list_similar_app, item_sim = knn(int(appid), df_svd, top_k)
    for i in range(len(list_similar_app)):
        similar_app = list_similar_app[i]
        similar_level = item_sim[i]
        try:
            if type == "click":
                if similar_level > 0:
                    print(similar_level * temperature, end=" ")
                    rating_map[similar_app] *= (1 + similar_level * temperature)
            elif type == "dislike":
                rating_map[similar_app] /= (1.1 + similar_level * temperature)
            else:
                if similar_level > 0:
                    print(similar_level * temperature, end=" ")
                    rating_map[similar_app] *= (1 + 2 * similar_level * temperature)
        except KeyError:
            continue
    return rating_map


def knn(appid, df_svd, top_k):
    """
    return k nearest item for one app based on content
    """
    V_i = df_svd.loc[appid].values
    norm = np.linalg.norm(V_i) * np.linalg.norm(df_svd, axis=1)
    similar = np.dot(df_svd.values, V_i) / norm
    ids = np.argsort(similar)[::-1]
    item_sim = similar[ids]
    return list(df_svd.index[ids])[1:top_k], item_sim[1:top_k]
