#!/bin/bash
rm nohup.out
touch nohup.out
nohup /usr/local/natapp/natapp -authtoken=fa923b8b5784fda1 &
