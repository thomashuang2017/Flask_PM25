# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 00:23:31 2018

@author: willy
"""

from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
#        """ on_start is called when a Locust start before any task is scheduled """
        self.client.post("/login", {
            "username": "willy",
            "password": "71128269"
        })


#    def on_stop(self):
#        """ on_stop is called when the TaskSet is stopping """
#        self.logout()
#
#    @task(1)
#    def login(self):
#                 self.client.post("/login", {
#            "username": "willy",
#            "password": "71128269"
#        })

#
#    def logout(self):
#           self.client.post("/login", {
#            "username": "willy",
#            "password": "71128269"
#        })

    @task(1)
    def homepage(self):
        self.client.get("/")
    @task(1)
    def map_view(self):
        self.client.get("/map_view")        
    @task(1)
    def recommand(self):
        self.client.get("/recommand")
    @task(1)
    def register(self):
        self.client.get("/register")
    @task(1)
    def private(self):
        self.client.get("/user_private")
    @task(1)
    def exinfo(self):
        self.client.get("/exInfo/花蓮縣/")
#    @task(1)
#    def login(self):
#        self.client.post("/login")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = "https://hidden-eyrie-71902.herokuapp.com"
    #host = "http://localhost:81"
    min_wait = 1000 #ms
    max_wait = 2000
#    task_set = UserAction
    
#  locust -f Pressure_test/locustfile.py --host=http://localhost:8888