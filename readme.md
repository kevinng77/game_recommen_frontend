# Game recommender

```c
.
├── app.py
├── config
│   └── config.py
├── data
├── model  //recommender models
├── natapp.sh  // nat tool. You might select other nat tools
├── readme.md
├── static
│   ├── index.css
│   └── list.png
├── templates
│   └── index.html
└── utils
    └── web_utils.py
```

## To run

````python
python app.py --temperature 0.5 --num_lines_load 4 --num_lines_init 8
# or flask run
````

Design consideration: [Blog - Once you click link of "dog", there will millions more. : 0]()

## How like or dislike work?

If you click **like** for one item, the rating for other similar items will be increased, such that they are more likely to be recommended. Click detail for one item will result in slightly increase on similar item score.

## Screen shot

The design style is similar to steam official, click details to view details **in steam official website**.

![sample.jpg](https://i.loli.net/2021/07/06/4Nw6nY2sSxbyeKM.jpg)

user id update bar

![userbat.jpg](https://i.loli.net/2021/07/06/gUhDEcTKrtWwlby.jpg)

## Reference

[CSDN - 右侧边栏right bar](https://blog.csdn.net/wenjiusui8083/article/details/79053397)

[Codepen - jQuery. Fly to cart effect.](https://codepen.io/elmahdim/pen/tEeDn)

