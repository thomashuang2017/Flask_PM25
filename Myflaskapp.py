# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask , render_template,flash,redirect,url_for,session,request
from functools import wraps
from formclass import RegisterForm
from DBmgt import DoSQL
from PM25 import PM25
from exinfo import exinfo

 

app = Flask(__name__)
app.secret_key='secret123'


# 主畫面
@app.route('/')
def homepage():
    return render_template('homepage.html')

# 關於頁面
#About fuck off

# 使用者註冊
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():

        username = form.username.data
        email = form.email.data
        password = form.password.data
        # address

        # confirm username is duplicate
        result,content = DoSQL().S_db("SELECT * FROM users WHERE username = %s",(username),1)
        if result > 0:
            flash('Username is duplicated','danger')
            return render_template('register.html',form=form)
        # Not duplicate , insert db and going to homepage
        else:
            DoSQL().IUD_db("INSERT INTO users(username,email,password) VALUES(%s, %s, %s)",(username,email,password),1)
            # is logged in
            session['login_in'] = True
            session['username'] = username
            flash('You are now registered','success')
            return redirect(url_for('map_view'))

    return render_template('register.html',form = form)


# 使用者登入
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':

        username = request.form['username']
        password = request.form['password']

        # username not found , password error , success login

        result,data = DoSQL().S_db("SELECT * FROM users WHERE username = %s",[username],1)

        if result > 0 :

            # 找這個使用者的 password
            user_password = data['password']

            # Compare Passwords
            if password == user_password:

                session['login_in'] = True
                session['username'] = username


                flash('You are now logged in','success')
                return redirect(url_for('map_view'))
            else:
                error = 'Invalid login'
                return render_template('login.html',error = error)
        else:
            error = 'Username not found'
            return render_template('login.html',error = error)


    return render_template('login.html')
s
# Check 使用者是否有登入
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'login_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized,Please log in','danger')
            return redirect(url_for('login'))
    return wrap


# 登出
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('homepage'))

# ----------------------------------------------以上都不動 -------------------------------------------------------------------


# map_view
@app.route('/map_view')
@is_logged_in
def map_view():

    PM25_value = PM25().Get_PM25() 
    return render_template('taiwan_map.html',value=PM25_value)


#點選taiwan_map後的對應城市頁面
@app.route('/exInfo/<string:county_name>/')
@is_logged_in
def exInfo(county_name):

    # find county_pm
    county_pm,time = PM25().Get_one_PM25(county_name)
    #print(county_name)
    county = county_name
    county_pm = county_pm[0][time]

    # find county_exinfo
    county_exinfo = exinfo().Get_county_exinfo(county_name)

    # find county_past_pm25
    county_past_pm = PM25().Get_past_pm25(county_name)

    return render_template('exInfo.html',county=county , pm=county_pm ,exinfo=county_exinfo,past_pm=county_past_pm)

# 推薦頁面
@app.route('/recommand',methods=['GET','POST'])
@is_logged_in
def render_recommand():
        #----------------互動頁無動作server丟值
    min_county = PM25().Get_min_county()
    pm,_ = PM25().Get_one_PM25(min_county)
    recommand_exinfo = exinfo().Get_county_exinfo(min_county)
    
    if request.method == 'POST':
        
        result,user_id = DoSQL().S_db("SELECT id FROM users WHERE username = %s",session['username'],1)
        favorite_exinfo = request.form.getlist('link0')
        #---------------重複選取解決方法
        sql = "SELECT ex_id FROM user_favorite_exinfo AS u1 WHERE exists(SELECT * FROM users AS u2 WHERE u2.id=%s and u1.ID=u2.ID and u1.ex_id=%s )"
        ex_id_repeat = []
        for i in range(len(favorite_exinfo)):
                result,ex_id = DoSQL().S_db(sql,(user_id['id'],favorite_exinfo[i]),2)
                if result > 0:
                    #ex_id_repeat.append(ex_id)
                    ex_id_repeat.append(ex_id[0]["ex_id"])
                    
        #------ ex_id 回傳該user目前記錄的ex_id 
        #result,ex_id = DoSQL().S_db(sql,user_id['id'],2)
        if len(ex_id_repeat) > 0 :
            #flash('重複選取','danger')
            return render_template('about.html',ex_id_repeat=ex_id_repeat)
        
    return render_template('recommand.html',min_county=min_county,recommand_exinfo=recommand_exinfo,pm=pm)
        
# 使用者個人葉面
@app.route('/user_private')
@is_logged_in
def user_private():
	
    _,userdata = DoSQL().S_db("SELECT * FROM users WHERE username=%s",session['username'],2)
    #user_id = userdata[0]["id"]
    #favorite_exinfo =[]
    
    _,favorite_exinfo = DoSQL().S_db("select * from exinfo as e1 where exists(select * from user_favorite_exinfo as u1 where u1.ex_id=e1.ex_id and u1.id=%s)",userdata[0]["id"],2)
    _,select_county = DoSQL().S_db("select distinct county from exinfo as e1 where exists(select * from user_favorite_exinfo as u1 where u1.ex_id=e1.ex_id and u1.id=%s)",userdata[0]["id"],2)
    #favorite_county = [] # unique county
    #for i in range(0,len(select_county)):
    #    favorite_county.append(select_county[i]["county"]) 
    #set_favorite_county=set(favorite_county)
    #favorite_county=list(set_favorite_county)
    
    
    return render_template('user_private.html',userdata=userdata,favorite_exinfo=favorite_exinfo,favorite_county=select_county)


if __name__ == '__main__':

    app.run(host='127.0.0.1',port=81,debug=True)
