# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 20:10:48 2018

@author: gaga
"""

from wtforms import Form,StringField,TextAreaField,PasswordField,validators

# 註冊的 form class
class RegisterForm(Form):
    
    username = StringField('Username',[validators.Length(min=4,max=10)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    password = PasswordField('Password',[
            validators.Length(min=1,max=10),
            validators.DataRequired(),
            validators.EqualTo('confirm',message = 'Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
        