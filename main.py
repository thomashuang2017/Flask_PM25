# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask , render_template,flash,redirect,url_for,session,request
from functools import wraps
from formclass import RegisterForm
from DBmgt import DoSQL
from Get_PM25 import Get_PM25
from Get_exinfo import Get_exinfo
from flask_apscheduler import APScheduler
from datetime import datetime
from scrapPM25 import scrapPM25
from config import config



app = Flask(__name__)
app.config.from_object(config['ScrapPM25Config'])

app.secret_key='secret123'

# 爬蟲PM25 排程
def job_1():
    scrapPM25().scrap_PM25_toDB()
    

# 主畫面
@app.route('/')
def homepage():
    return render_template('homepage.html')

# 使用者註冊
@app.route('/register',methods=['GET','POST'])
def register():
    
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():

        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # connect_db
        connect_db = DoSQL().get_conn()
        
        # confirm username is duplicate
        result,content = DoSQL().S_db("SELECT id FROM users WHERE username = %s",(username),1,connect_db)
        if result > 0:
            flash('Username is duplicated','danger')
            return render_template('register.html',form=form)
        # Not duplicate , insert db and going to homepage
        else:
            DoSQL().IUD_db("INSERT INTO users(username,email,password) VALUES(%s, %s, %s)",(username,email,password),1,connect_db)
            # is logged in
            session['login_in'] = True
            session['username'] = username
            flash('You are now registered','success')
            
             # close_db
            DoSQL().close_conn(connect_db)
            
            return redirect(url_for('map_view'))

    return render_template('register.html',form = form)


# 使用者登入
@app.route('/login',methods=['GET','POST'])
def login():
    
    if request.method =='POST':

        username = request.form['username']
        password = request.form['password']

        # connect_db
        connect_db = DoSQL().get_conn()
        
        result,data = DoSQL().S_db("SELECT id,password FROM users WHERE username = %s",[username],1,connect_db)

        if result > 0 :

            # 找這個使用者的 password
            user_password = data['password']

            # Compare Passwords
            if password == user_password:

                session['login_in'] = True
                session['username'] = username

                # close_db
                DoSQL().close_conn(connect_db)
                
                flash('You are now logged in','success')
                return redirect(url_for('map_view'))
            else:
                flash('Invalid login','danger')
                #error = 'Invalid login'
                return render_template('login.html')
        else:
            flash('Username not found','danger')
            #error = 'Username not found'
            return render_template('login.html')


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
    return redirect(url_for('homepage'))


# map_view
@app.route('/map_view')
@is_logged_in
def map_view():

    # connect_db
    connect_db = DoSQL().get_conn()
    
    # Get PM25
    PM25_value = Get_PM25(connect_db).Get_PM25() 
    
    # close_db
    DoSQL().close_conn(connect_db)
    dt = datetime.now(config['GetlocaltimeConfig'].tz)
#    dt = datetime.now()
    return render_template('map_view.html',value=PM25_value,dt=dt)


# ----------------------------------------------以上都不動 -------------------------------------------------------------------

#點選taiwan_map後的對應城市頁面
@app.route('/exInfo/<string:county_name>/',methods=['GET','POST'])
@is_logged_in
def exInfo(county_name):
    
    # connect_db
    connect_db = DoSQL().get_conn()

    # Get one PM25
    county_pm,time = Get_PM25(connect_db).Get_one_PM25(county_name)
    
    county = county_name
    county_pm = county_pm[0][time]
    
     # find county_past_pm25
    county_past_pm = Get_PM25(connect_db).Get_past_pm25(county_name)

    # find county_exinfo
    county_exinfo = Get_exinfo(connect_db).Get_county_exinfo(county_name)

    
    if request.method == 'POST':      
        # 先判斷有無重複，再塞入forloop，再insert
        # 缺 massage告訴使用者她選了甚麼
        
        result,user_id = DoSQL().S_db("SELECT id FROM users WHERE username = %s",session['username'],1,connect_db)
        user_ex_id = request.form.getlist('exinfo_id_list')
        print(user_ex_id)
        
        #避免沒打勾
        if len(user_ex_id)>0:
            #判斷重複的ex_id
            sql = "SELECT ex_id FROM user_favorite_exinfo AS u1 WHERE exists(SELECT id FROM users AS u2 WHERE u2.id=%s and u1.ID=u2.ID and u1.ex_id=%s )"
            ex_id_repeat = []
            for i in range(len(user_ex_id)):
                    result,content = DoSQL().S_db(sql,(user_id['id'],user_ex_id[i]),2,connect_db)
                    if result > 0:
                        ex_id_repeat.append(content[0]["ex_id"])
            #排除重複值
            for i in range(0,len(ex_id_repeat)):
                user_ex_id.remove(str(ex_id_repeat[i]))    
            #dict insert比較快
            ex_id = []
            for i in range(0,len(user_ex_id)):
                ex_id.append({'id':str(user_id['id']),'ex_id':user_ex_id[i]})
    
            SQL = "INSERT INTO user_favorite_exinfo VALUES(%(id)s,%(ex_id)s)"
            DoSQL().IUD_db(SQL,ex_id,2,connect_db)
                   
            #flash('Add'+str(user_ex_id)+ 'success'+'but repeat:'+str(ex_id_repeat),'success')
            flash('Add bookmark success,please checked private page','success')
            # close_db
            DoSQL().close_conn(connect_db)
        else:
            
            return render_template('exInfo.html',county=county , pm=county_pm ,exinfo=county_exinfo,past_pm=county_past_pm)
            
    return render_template('exInfo.html',county=county , pm=county_pm ,exinfo=county_exinfo,past_pm=county_past_pm)
    

# 推薦頁面
@app.route('/recommand',methods=['GET','POST'])
@is_logged_in
def render_recommand():
 
    connect_db = DoSQL().get_conn()
    
    min_county = Get_PM25(connect_db).Get_min_county()
    pm,_ = Get_PM25(connect_db).Get_one_PM25(min_county)
    recommand_exinfo = Get_exinfo(connect_db).Get_county_exinfo(min_county)
    if request.method == 'POST':      
        # 先判斷有無重複，再塞入forloop，再insert
        # 缺 massage告訴使用者她選了甚麼
        
        result,user_id = DoSQL().S_db("SELECT id FROM users WHERE username = %s",session['username'],1,connect_db)
        user_ex_id = request.form.getlist('exinfo_id_list')
        #避免沒打勾
        if len(user_ex_id)>0:
            #判斷重複的ex_id
            sql = "SELECT ex_id FROM user_favorite_exinfo AS u1 WHERE exists(SELECT id FROM users AS u2 WHERE u2.id=%s and u1.ID=u2.ID and u1.ex_id=%s )"
            ex_id_repeat = []
            for i in range(len(user_ex_id)):
                    result,content = DoSQL().S_db(sql,(user_id['id'],user_ex_id[i]),2,connect_db)
                    if result > 0:
                        ex_id_repeat.append(content[0]["ex_id"])
            #排除重複值
            for i in range(0,len(ex_id_repeat)):
                user_ex_id.remove(str(ex_id_repeat[i]))    
            #dict insert比較快
            ex_id = []
            for i in range(0,len(user_ex_id)):
                ex_id.append({'id':str(user_id['id']),'ex_id':user_ex_id[i]})
    
            SQL = "INSERT INTO user_favorite_exinfo VALUES(%(id)s,%(ex_id)s)"
            DoSQL().IUD_db(SQL,ex_id,2,connect_db)
                   
#            flash('Add'+str(user_ex_id)+ 'success'+'but repeat:'+str(ex_id_repeat),'success')
            flash('Add bookmark success,please checked private page','success')
            # close_db
            DoSQL().close_conn(connect_db)
        else:
            return render_template('recommand.html',min_county=min_county,recommand_exinfo=recommand_exinfo,pm=pm)
    return render_template('recommand.html',min_county=min_county,recommand_exinfo=recommand_exinfo,pm=pm)

        
# 使用者個人葉面
@app.route('/user_private',methods=['GET','POST'])
@is_logged_in
def user_private():
    
    # connect_db
    connect_db = DoSQL().get_conn()
    
    #userdata : user detail
    _,userdata = DoSQL().S_db("SELECT id,username,email FROM users WHERE username=%s",session['username'],2,connect_db)
    
    
    favorite_exinfo = Get_exinfo(connect_db).Get_user_exinfo(userdata[0]['id'])
    #單獨select不重複的county值 
#    _,select_county = DoSQL().S_db("select distinct county from exinfo as e1 where exists(select * from user_favorite_exinfo as u1 where u1.ex_id=e1.ex_id and u1.id=%s)",userdata[0]["id"],2,connect_db)
    #刪除方法
    if request.method == 'POST':
        
        try:
            #delete_exinfo =[] 存放要刪除的選項value
            delete_exinfo = request.form.getlist('exinfo_id_list')
            Get_exinfo(connect_db).Delete_user_exinfo(userdata[0]['id'],delete_exinfo)
    
            
            favorite_exinfo = Get_exinfo(connect_db).Get_user_exinfo(userdata[0]['id'])
#            _,select_county = DoSQL().S_db("select distinct county from exinfo as e1 where exists(select * from user_favorite_exinfo as u1 where u1.ex_id=e1.ex_id and u1.id=%s)",userdata[0]["id"],2,connect_db)
            
            # close_db
            DoSQL().close_conn(connect_db)
            
        except: 
#            return render_template('user_private.html',userdata=userdata,favorite_exinfo=favorite_exinfo,favorite_county=select_county)
            flash('Please check your options','danger')
            return render_template('user_private.html',userdata=userdata,favorite_exinfo=favorite_exinfo)
        
        flash('Update success','success')
#        return render_template('user_private.html',userdata=userdata,favorite_exinfo=favorite_exinfo,favorite_county=select_county)
        return render_template('user_private.html',userdata=userdata,favorite_exinfo=favorite_exinfo)
#    return render_template('user_private.html',userdata=userdata,favorite_exinfo=favorite_exinfo,favorite_county=select_county)
    return render_template('user_private.html',userdata=userdata,favorite_exinfo=favorite_exinfo)

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='127.0.0.1',port=8080,debug=True)
    
