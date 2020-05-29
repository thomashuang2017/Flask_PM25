# Flask_PM25
-------------------------------------------------------------------------
## 系統特色
1. 即時公布PM2.5資料  
2. 提供全台展演活動  
3. 推薦給您健康的展演活動  
4. 專屬個人收藏展演活動  

## 系統開發環境
1.	作業系統：Microsoft  Windows 10
2.	資料庫：GCP MYSQL Server
3.	開發軟體：
(1).	專案類型：Flask
(2).	程式語言：Python
(3).	擴充套件：jquery-1.8.3min.js
          jquery.flot.min.js


## 系統架構
1. 利用Flask做web後端的開發，依照MVC架構進行開發
2. Python爬取政府的opendata，開發一個整合每小時PM25 data和全台展覽活動 data的使用者互動網站
3. 使用 GCP 的 mySQL作為資料庫
4. 系統用GCP的App engine佈署上線

## 系統畫面
![image](https://github.com/thomashuang2017/Flask_PM25/blob/master/pic/1.png)
![image](https://github.com/thomashuang2017/Flask_PM25/blob/master/pic/2.png)
![image](https://github.com/thomashuang2017/Flask_PM25/blob/master/pic/3.png)
![image](https://github.com/thomashuang2017/Flask_PM25/blob/master/pic/4.png)
![image](https://github.com/thomashuang2017/Flask_PM25/blob/master/pic/5.png)
![image](https://github.com/thomashuang2017/Flask_PM25/blob/master/pic/6.png)

在github更新的步驟:(先刪除pycache)
1. 先clone這個專案(不是download是clone)
2. 改程式碼
3. 改完後先commit
4. 最後在push (如果出現 Try pull before push代表你沒有先pull or clone)

(如果有private的error代表你勾到 keep private code的選項)

如果你要到某一個版本
git checkout 版本代號

 
