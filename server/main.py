from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd
import numpy as np
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from keras.api._v2.keras.layers import Dense, Activation, Dropout
from keras.api._v2.keras.optimizers import Adam
from keras.api._v2.keras.metrics import Accuracy
from keras.api._v2.keras.models import Sequential
from keras.api._v2.keras.layers import Dense, Dropout

from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report,accuracy_score,roc_curve,confusion_matrix

from csv import writer
from sklearn.preprocessing import StandardScaler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

@app.get('/checkProf/{uname}')
def check(uname: str):
  BASE_URL = "https://www.instagram.com/"

  target = uname

  driver = webdriver.Chrome()
  driver.maximize_window()
  driver.implicitly_wait(21)

  try:
    driver.get(BASE_URL + target)

    bioElement = WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    data = WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
    val = data.find_elements(By.TAG_NAME, 'li')
    
    posts = int(val[0].text.split()[0].replace(',', ''))
    followers = int(val[1].text.split()[0].replace(',', ''))
    following = int(val[2].text.split()[0].replace(',', ''))
    bios = bioElement.text
    fullName = WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.x1lliihq'))).text

    a = len(target)
    a = str(a).replace(',', '')
    UserNameLen = len(target)
    UserNameLen = float(UserNameLen)

    nameList = fullName.split()
    wordCount = len(nameList)

    if fullName == target:
      sameName = int(True)
    else:
      sameName = int(False)
    driver.close()

    thingsToAdd = [UserNameLen, wordCount, sameName, len(bios), posts, followers, following, 0]

    with open('test.csv', 'a', newline='') as f_object:
      writer_object = writer(f_object)
      writer_object.writerow(thingsToAdd)
  except:
    print(f"{target} is missing. ")

  insta_df_train = pd.read_csv('./train.csv')
  insta_df_test = pd.read_csv("./test.csv")

  X_train = insta_df_train.drop(columns = ['fake'])
  y_train = insta_df_train['fake']

  X_test = insta_df_test.drop(columns = ['fake'])
  y_test = insta_df_test['fake']

  scaler_x = StandardScaler()
  X_train = scaler_x.fit_transform(X_train)
  X_test = scaler_x.transform(X_test)

  """ y_train = tf.keras.utils.to_categorical(y_train, num_classes = 2)
  y_test = tf.keras.utils.to_categorical(y_test, num_classes = 2)
 """
  model = Sequential()
  model.add(Dense(50, input_dim=7, activation='relu'))
  model.add(Dense(150, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(150, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(25, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(2,activation='softmax'))

  model.summary()

  model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

  predicted = model.predict(X_test)
  ans = predicted[-1]

  array = np.array(ans)
  integer_array = np.round(array).astype(int)
  integer_array = integer_array[1:]

  if(integer_array == 0):
    check = 'fake'
  else:
    check = 'real'

  """ if(integer_array == 0):
    check = 'real'
  else:
    check = 'fake' """
  
  return {
    'followers': followers, 
    'following': following, 
    'posts': posts, 
    'check': check
  }