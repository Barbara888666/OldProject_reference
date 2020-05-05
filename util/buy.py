import os
from flask import Flask, render_template, request, flash, Blueprint

bought=Blueprint('bought',__name__)
@bought.route('/buy/', methods=['GET', 'POST'])
def buy():
    return "Coming Soon...."






