from __future__ import print_function

import datetime
import os
import uuid

import mysql.connector
from mysql.connector import errorcode

from nwd_crypto import NWD_Crypto


class NWD_DB:

  DB_NAME = 'NWD'
  INIT_LOGIN = "CREATE TABLE `UPP` (`email` varchar(256) NOT NULL,`password`varchar(64) NOT NULL,`user_id` varchar(64) NOT NULL,`sec_question` varchar(64) NOT NULL,`sec_answer` varchar(64) NOT NULL) ENGINE=InnoDB"
  INIT_IDSTORE = "CREATE TABLE `IDP` (`user_id` varchar(64) NOT NULL, `fname` varchar(40) NOT NULL, `lname` varchar(40) NOT NULL,`phone` varchar(20) NOT NULL,`email` varchar(256) NOT NULL,`datejoined` DATE NOT NULL) ENGINE=InnoDB"


  INIT_NEW_USER = "INSERT INTO UPP (email, password, user_id, sec_question, sec_answer) VALUES (%(email)s, %(password)s, %(user_id)s, %(sec_question)s, %(sec_answer)s)"
  INIT_NEW_IDP = "INSERT INTO IDP (user_id, fname, lname, phone, email, datejoined) VALUES (%(user_id)s, %(fname)s, %(lname)s, %(phone)s, %(email)s, %(datejoined)s)"


  GETUSER =  "SELECT user_id FROM UPP WHERE email = %(email)s "
  GETUSERID = "SELECT user_id FROM UPP WHERE email = %(email)s AND password = %(password)s"
  GETIDP = "SELECT fname, lname, phone, email, datejoined FROM IDP WHERE user_id = %(user_id)s"

  UPDATEPASSWORDRESETLINK = "UPDATE UPP SET sec_answer =  %(sec_answer)s WHERE email = %(email)s" 
  REDEEMPPASSWORDRESETLINK = "UPDATE UPP SET sec_answer = 'a', password=%(password)s WHERE sec_answer = %(sec_answer)s" 

  GETALLUSERS = "SELECT * FROM IDP"

  def open_db(self):
    return  mysql.connector.connect(user=os.environ['login'], password=os.environ['sqlp'], database=self.DB_NAME)

  def close_db(self,cnx,cursor):
    try:
      cursor.close()
    except:
      print("Ex Caught")
    cnx.close()

  def init_database(self):
    try:
      cnx = mysql.connector.connect(user=os.environ['login'], password=os.environ['sqlp'])
      cursor = cnx.cursor()
      cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
      self.close_db(cnx,cursor)
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

  def init_tables(self):
    cnx = self.open_db()
    cursor = cnx.cursor()
    cursor.execute(self.INIT_LOGIN)
    cursor.execute(self.INIT_IDSTORE)

    self.close_db(cnx,cursor)

  def init_all(self):  
    self.init_database()
    self.init_tables()

  def create_new_user(self,email,password,fname,lname,phone):
    cnx = self.open_db()

    cursor = cnx.cursor()
    uid = ""

    if self.user_exists(email,cursor) == False:

      CRYPTO = NWD_Crypto()
      uid = (uuid.uuid4().hex+uuid.uuid4().hex)
      user_login = {
        'email':email,
        'password': CRYPTO.Encrypt(password),
        'user_id': uid,
        'sec_question': "",
        'sec_answer': "a"
      }

      cursor.execute(self.INIT_NEW_USER, user_login)

      user_id = {
       'user_id':uid,
       'fname': fname,
       'lname': lname,
       'phone': phone,
       'email': email,
        'datejoined': datetime.datetime.now().strftime("%y-%m-%d")    
      }

      cursor.execute(self.INIT_NEW_IDP,user_id )
      cnx.commit()

    self.close_db(cnx,cursor)
    return uid
  
  def user_exists(self,email, cursor):
    user = {
      'email':email,
    }

    try:
      cursor.execute(self.GETUSER, user)
      for (user_id) in cursor:
        return True
    except:
      return False
    
    return False

  def authenticate_user(self,email,password):
    cnx = self.open_db()
    cursor = cnx.cursor()
    CRYPTO = NWD_Crypto()

    user = {
      'email':email,
      'password': CRYPTO.Encrypt(password),
    }

    cursor.execute(self.GETUSERID, user)

    uid = ""

    for (user_id) in cursor:
      uid = user_id
    
    self.close_db(cnx,cursor)

    return uid

  def get_user_info(self,user_id):
    cnx = self.open_db()
    cursor = cnx.cursor()
    CRYPTO = NWD_Crypto()

    idd = {
      'user_id':user_id,
    }

    cursor.execute(self.GETIDP, idd)

    user_info = {}

    for (fname, lname, phone, email,datejoined,) in cursor:
      user_info = {
        'user_id' : user_id,
        'fname' :  fname,
        'lname' :  lname, 
        'phone' : phone,
        'email': email, 
        'datejoined': str(datejoined)
      }
    
    self.close_db(cnx,cursor)

    return user_info


















  def init_password_reset(self,email,uuid):

    cnx = self.open_db()
    cursor = cnx.cursor()
    CRYPTO = NWD_Crypto()

    var = {
      'email':email,
      'sec_answer': uuid
    }
    cursor.execute(self.UPDATEPASSWORDRESETLINK, var)
    cnx.commit()
    self.close_db(cnx,cursor)

  def redeem_password_reset(self,password,uuid):

    cnx = self.open_db()
    cursor = cnx.cursor()
    CRYPTO = NWD_Crypto()

    var = {
      'password':CRYPTO.Encrypt(password),
      'sec_answer': uuid
    }
    cursor.execute(self.REDEEMPPASSWORDRESETLINK, var)
    cnx.commit()
    self.close_db(cnx,cursor)


  def get_all_users(self):
    cnx = self.open_db()
    cursor = cnx.cursor()

    cursor.execute(self.GETALLUSERS)

    user_info = []

    for (user_id,fname, lname, phone, email,datejoined,) in cursor:
      user_info.append({
        'user_id' : user_id,
        'fname' :  fname,
        'lname' :  lname, 
        'phone' : phone,
        'email': email, 
        'datejoined': str(datejoined)
      })
    
    self.close_db(cnx,cursor)

    return user_info

