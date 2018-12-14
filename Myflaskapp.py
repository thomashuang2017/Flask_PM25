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
@app.route('/about')
def about():
    return render_template('about.html')

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
    return redirect(url_for('login'))

# ----------------------------------------------以上都不動 -------------------------------------------------------------------


# map_view
@app.route('/map_view')
@is_logged_in
def map_view():


    PM25_value,time = PM25().Get_PM25() # return County and PM25 {'county': '南投縣', 'pm3': 26}
    # ---------------
    # PM25_value = {'county': '南投縣', 'pm3': 26}
    # time = datatime%9 (ex: 14:00 % 9 = 5)
    # 所以你剖析是 PM25_value['time']
    #
    # ---------------
    #PM25_interval = PM25().Get_county_intervel()
    # return {'county': '南投縣', 'interval': 0}
    #PM25_min_county = PM25().Get_min_county()
    # return 臺東縣


    return render_template('taiwan_map.html')



@app.route('/exInfo/<string:county_name>/')
@is_logged_in
def exInfo(county_name):

    # find county_pm
    county_pm,time = PM25().Get_one_PM25(county_name)
    county = county_name
    county_pm = county_pm[0][time]

    # find county_exinfo
    county_exinfo = exinfo().Get_county_exinfo(county_name)



    # find county_past_pm25
    # 醜到爆
    county_past_pm = PM25().Get_past_pm25(county_name)
    a = county_past_pm[0]['county']
    pm0=county_past_pm[0]['pm0']
    pm1=county_past_pm[0]['pm1']
    pm2=county_past_pm[0]['pm2']
    pm3=county_past_pm[0]['pm3']
    pm4=county_past_pm[0]['pm4']
    pm5=county_past_pm[0]['pm5']
    pm6=county_past_pm[0]['pm6']
    pm7=county_past_pm[0]['pm7']
    pm8=county_past_pm[0]['pm8']

    return render_template('exInfo.html', a = a, pm0=pm0 , pm1=pm1 , pm2=pm2 , pm3=pm3 , pm4=pm4, pm5=pm5, pm6=pm6, pm7=pm7 , pm8=pm8 ,county=county , pm=county_pm ,exinfo=county_exinfo,past_pm=county_past_pm)


# recommand
@app.route('/recommand',methods=['GET','POST'])
@is_logged_in
def render_recommand():
    min_county = PM25().Get_min_county()
    pm,_ = PM25().Get_one_PM25(min_county)
    recommand_exinfo = exinfo().Get_county_exinfo(min_county)
    
    return render_template('recommand.html',min_county=min_county,recommand_exinfo=recommand_exinfo,pm=pm)


@app.route('/test2',methods=['GET','POST'])
def test():
    min_county = PM25().Get_min_county()
    pm,_ = PM25().Get_one_PM25(min_county)
    recommand_county = exinfo().Get_county_exinfo(min_county)
    
    return render_template('test2.html',min_county=min_county,recommand_county=recommand_county)


def Post_user_favorite():
     if request.method =='POST':
        username = request.form['username']

        recommand = request.form.getlist('exinfo')
        sql = "INSERT INTO RECOMMAND VALUE(%(USER)s,%(EXINFO)s)"
        DoSQL.IUD_db(sql,username,recommand,2)



     return render_template('exInfo.html',pm=pm,recommand_county=recommand_county)


@app.route('/user_private')
@is_logged_in
def user_private():

    SQL = "SELECT * FROM users WHERE username=%s"
    _,userdata = DoSQL().S_db(SQL,session['username'],2)

	# --------------------------------
    # user favorite exinfo
    #
    # --------------------------------


    return render_template('user_private.html',userdata=userdata)


if __name__ == '__main__':

    app.run(host='127.0.0.1',port=81,debug=True)
