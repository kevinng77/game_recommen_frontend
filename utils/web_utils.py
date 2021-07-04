


def process_title(title,max_title_len):
    if len(title)>max_title_len:
        return title[:max_title_len-3] + "..."
    else:
        return title


def gen_msg(applist,max_title_len,selected_ids):
    """
    :param applist: data frame
    :param selected_ids: AppID to recommended
    :return: list of tuple (AppName, picture, )
    """
    df_selected_game = applist[applist.AppID.apply(lambda x: x in selected_ids)]

    l_name = df_selected_game.AppName.tolist()
    l_name = [process_title(x, max_title_len) for x in l_name]
    l_view = df_selected_game.Picture.tolist()
    l_url = df_selected_game.url.tolist()
    l_price = df_selected_game.final_price.tolist()
    msg = list(zip(l_name, l_view, l_price,l_url))
    # TODO add price,
    return msg

def load_more_formatting(pic,name,price,url):
    template = f'<div class="item">' \
               f'<div class="img_block">' \
               f'<img src="{pic}" alt="item" />' \
               f'</div><div class="name_block">' \
               f'<h2>{name}</h2></div><div>' \
               f'<a  class="price">Price: <em>${price}</em>' \
               f'</a><a class="details" ' \
               f'onclick="window.open(\'{url}\')">' \
               f'<em>Details>></em></a></div></div>'
    return template