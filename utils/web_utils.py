import numpy as np

def process_title(title, max_title_len):
    if len(title) > max_title_len:
        return title[:max_title_len - 3] + "..."
    else:
        return title


def gen_msg(applist, max_title_len, selected_ids):
    """
    :param applist: data frame
    :param selected_ids: AppID to recommended
    :return: list of tuple (AppName, picture, )
    """
    df_selected_game = applist.loc[selected_ids]
    l_name = df_selected_game.AppName.tolist()
    l_name = [process_title(x, max_title_len) for x in l_name]
    l_view = df_selected_game.Picture.tolist()
    l_url = df_selected_game.url.tolist()
    l_price = df_selected_game.final_price.tolist()
    l_genre = df_selected_game.Genre.tolist()
    msg = list(zip(selected_ids,l_name, l_view, l_price, l_url,l_genre))
    return msg


def load_more_formatting(pic, name, price, url, Appid, other ="todo: adding tag"):
    template = f'<div class="item">' \
               f'<div class="img_block">' \
               f'<img src="{pic}" alt="item" />' \
               f'</div><div class="name_block">' \
               f'<h2>{name}</h2></div>' \
               f'<div class="game_tag">{other}</div><div>' \
               f'<a  class="price"><em>${price}</em>' \
               f'</a><a class="details" ' \
               f'onclick="load_detail(\'{url}\',\'{Appid}\',\'{name}\')">' \
               f'<em>Details>></em></a></div></div>'
    return template


def update_item_weight(item_name):
    """
    update recommend item weight when user click
    :param item_name: AppName
    :return:
    """
    pass


def knn(appid, df_svd, top_k):
    """
    return k nearest item for one app based on content
    :param df_svd:
    """
    V_i = df_svd.loc[appid].values
    norm = np.linalg.norm(V_i) * np.linalg.norm(df_svd, axis=1)
    similar = np.dot(df_svd.values, V_i) / norm
    ids = np.argsort(similar)[::-1]
    return list(df_svd.index[ids])[1:top_k]