# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 23:19:20 2016

@author: strider
"""

#!/usr/bin/env python2.7

from werkzeug.utils import secure_filename
import os, flask, mysql_dao, fileUpload
from flask import Flask, request, render_template, session, redirect 
from flask import send_from_directory, url_for 
from sqlalchemy.orm import sessionmaker
from enums import ApplicationStatus, UserType, messages, emailMessages
import utils
from flask import make_response



application = Flask(__name__)


@application.before_request
def before_request():
    global dbcon,engine,dbSession
    dbcon,engine = mysql_dao.createDatabaseConnection()
    Session = sessionmaker(bind=engine)
    dbSession = Session()

@application.teardown_request
def teardown_request(exception):
  global dbcon
  try:
    dbcon.close()
  except Exception:
    pass

@application.route('/')
def main():
    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        formDict = session['user']
        if formDict['UserType'] == UserType['Student'] :
          if formDict['ApplicationStatus'] == ApplicationStatus['IncompleteApplication']:
              universityList = mysql_dao.getUniversityList(dbcon)
              return render_template('first.html',formDict=formDict,universityList=universityList)
          elif formDict['ApplicationStatus'] == ApplicationStatus['ReferencesRequired2'] or formDict['ApplicationStatus'] == ApplicationStatus['ReferencesRequired1']:
              ReferencesDict = dict()
              ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
              return render_template('third.html', ReferencesDict = ReferencesDict)  
          elif formDict['ApplicationStatus'] == ApplicationStatus['UnderReview']:
              return render_template('underReview.html')
      
        elif formDict['UserType'] == UserType['Admin']:
          studentList = mysql_dao.getStudentList(dbcon)
          return render_template('studentList.html',studentList=studentList)
    


    
if __name__ == "__main__":
  application.secret_key = os.urandom(24)
  application.run(threaded=True)



