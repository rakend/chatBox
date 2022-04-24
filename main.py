#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render(self,template,**kw):
        t=jinja_env.get_template(template)
        self.write(t.render(**kw))
        

class Chat(db.Model):
    name=db.StringProperty(required=True)
    all_post=db.TextProperty(required=True)
    datetime=db.DateTimeProperty(auto_now_add=True)

class MainHandler(Handler):
    def error(self,user_name="",user_text="",error="",allposts=""):
        allposts=db.GqlQuery("SELECT * FROM Chat ORDER BY datetime DESC LIMIT 50")
        self.render('final.html',user_name=user_name,user_text=user_text,error=error,p=allposts)
        
    def get(self):
            self.error()

    def post(self):
        name=self.request.get("name")
        textarea=self.request.get("textarea")

        if name and textarea:
            p=Chat(name=name,all_post=textarea)
            p.put()
            self.redirect("/")
        else:
            self.error(user_name=name,user_text=textarea,error="we need both the entries to be filled!")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


















