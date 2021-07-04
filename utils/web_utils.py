


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
    game_name_list = applist[applist.AppID.apply(lambda x: x in selected_ids)].AppName.tolist()
    game_name_list = [process_title(x, max_title_len) for x in game_name_list]
    game_pic_list = applist[applist.AppID.apply(lambda x: x in selected_ids)].Picture.tolist()
    msg = list(zip(game_name_list, game_pic_list))
    # TODO add price,
    return msg