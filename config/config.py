import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--max_title_length", default=50, type=int)
parser.add_argument("--num_lines_load", default=4, type=int,
                    help="number of lines to load when click load more")
parser.add_argument("--num_lines_init", default=8, type=int,
                    help="number of lines to show when init")
parser.add_argument("--temperature",type=float,default=0.7,
                    help="0 to 1, How strong you want to recommend based on user click")
parser.add_argument("--top_knn", default=50, type=int)
parser.add_argument("--seed",default=777,type=int)

args = parser.parse_args()


num_per_line = 3  # fixed to html design
exclude = ['AppName','Genre','Tags','Developer','Publisher','ReviewInfo','ReviewStatus',
           'ReleaseDate','IsFree','Price','ReviewSum','ReviewNum','Picture','url','tag_list']

max_title_len = args.max_title_length
num_show = num_per_line * args.num_lines_init
num_more_load = num_per_line * args.num_lines_load

# file path
game_info_path = "data/steam_game_url_pic.csv"
svd_path = "data/svd_d100.csv"

temperature = args.temperature
top_knn = args.top_knn
seed = args.seed
