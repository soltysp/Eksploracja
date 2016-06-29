from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from datetime import time
from sqlalchemy import Column, Integer, String, Text, Float
import statistics
from sqlalchemy.orm import sessionmaker

from numpy import genfromtxt
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)


labels=['Emotion', 'Emotion_confidence', 'Sentence']
emotionsdata = pd.read_csv('emotions.csv', sep=';', names=labels)

#emotionsdata = pd.read_excel('emotions.xls', index_col=None, na_values=['-'])

global nrofrows
nrofemotions=len(emotionsdata.Emotion)
nrofrows=nrofemotions

@app.route("/")
def welcome():

    return render_template('welcome.html')



@app.route("/raw")
def show_raw():
    return render_template('raw.html', formdata=emotionsdata.iloc[1:nrofrows, :].as_matrix())

@app.route("/save", methods=['POST'])
def save():
    global nrofrows
    # Get data from FORM

    action=request.form['action']
    if action=="all":
        nrofrows = nrofemotions
    else:
        nrofrows = int(request.form['nrofrows'])
        if nrofrows > nrofemotions or nrofrows < 1:
            nrofrows = nrofemotions
    return redirect('/raw')

@app.route("/result")
def show_result():

    neutral = emotionsdata.loc[emotionsdata['Emotion']=="Neutral"]
    aggress = emotionsdata.loc[emotionsdata['Emotion']=="Aggression"]
    ambig = emotionsdata.loc[emotionsdata['Emotion']=="Ambiguous"]
    anger = emotionsdata.loc[emotionsdata['Emotion']=="Anger"]
    anticip = emotionsdata.loc[emotionsdata['Emotion']=="Anticipation"]
    awe = emotionsdata.loc[emotionsdata['Emotion']=="Awe"]
    contem = emotionsdata.loc[emotionsdata['Emotion']=="Contempt"]
    disappro = emotionsdata.loc[emotionsdata['Emotion']=="Disapproval"]
    disgust = emotionsdata.loc[emotionsdata['Emotion']=="Disgust"]
    fear = emotionsdata.loc[emotionsdata['Emotion']=="Fear"]
    joy = emotionsdata.loc[emotionsdata['Emotion']=="Joy"]
    love = emotionsdata.loc[emotionsdata['Emotion']=="Love"]
    optimism = emotionsdata.loc[emotionsdata['Emotion']=="Optimism"]
    remorse = emotionsdata.loc[emotionsdata['Emotion']=="Remorse"]
    sadness = emotionsdata.loc[emotionsdata['Emotion']=="Sadness"]
    submis = emotionsdata.loc[emotionsdata['Emotion']=="Submission"]
    surprise =emotionsdata.loc[emotionsdata['Emotion']=="Surprise"]
    trust =emotionsdata.loc[emotionsdata['Emotion']=="Trust"]


    a1 = ["Neutral", "Aggression", "Ambiguous", "Anger", "Anticipation", "Awe", "Contempt", "Disapproval", "Disgust", "Fear", "Joy", "Love", "Optimism", "Remorse", "Sadness", "Submission", "Surprise", "Trust"]

    a2 = [neutral.loc[:,'Emotion_confidence'].mean(axis=0), aggress.loc[:,'Emotion_confidence'].mean(axis=0), ambig.loc[:,'Emotion_confidence'].mean(axis=0), anger.loc[:,'Emotion_confidence'].mean(axis=0), anticip.loc[:,'Emotion_confidence'].mean(axis=0), awe.loc[:,'Emotion_confidence'].mean(axis=0), contem.loc[:,'Emotion_confidence'].mean(axis=0), disappro.loc[:,'Emotion_confidence'].mean(axis=0),
               disgust.loc[:,'Emotion_confidence'].mean(axis=0), fear.loc[:,'Emotion_confidence'].mean(axis=0), joy.loc[:,'Emotion_confidence'].mean(axis=0), love.loc[:,'Emotion_confidence'].mean(axis=0), optimism.loc[:,'Emotion_confidence'].mean(axis=0), remorse.loc[:,'Emotion_confidence'].mean(axis=0), sadness.loc[:,'Emotion_confidence'].mean(axis=0), submis.loc[:,'Emotion_confidence'].mean(axis=0),
               surprise.loc[:,'Emotion_confidence'].mean(axis=0), trust.loc[:,'Emotion_confidence']. mean(axis=0)]
    a3 = [len(neutral.loc[:,'Emotion_confidence']), len(aggress.loc[:,'Emotion_confidence']), len(ambig.loc[:,'Emotion_confidence']), len(anger.loc[:,'Emotion_confidence']), len(anticip.loc[:,'Emotion_confidence']), len(awe.loc[:,'Emotion_confidence']), len(contem.loc[:,'Emotion_confidence']), len(disappro.loc[:,'Emotion_confidence']), len(disgust.loc[:,'Emotion_confidence']), len(fear.loc[:,'Emotion_confidence']), len(joy.loc[:,'Emotion_confidence']), len(love.loc[:,'Emotion_confidence']),
          len(optimism.loc[:,'Emotion_confidence']), len(remorse.loc[:,'Emotion_confidence']), len(sadness.loc[:,'Emotion_confidence']), len(submis.loc[:,'Emotion_confidence']), len(surprise.loc[:,'Emotion_confidence']), len(trust.loc[:,'Emotion_confidence'])]

    data1 = a1
    data1.append(a2)
    #data1 = data1.values.tolist()
    data2 = a1
    data2.append(a3)
    #data2 = data2.values.tolist()

    return render_template('result.html', data1=data1, data2=data2)

if __name__ == "__main__":
    app.debug = True
    app.run()


# Create the database
engine = create_engine('sqlite:///formdata.db')
if not(engine.dialect.has_table(engine.connect(), "emotions")):
    Base.metadata.create_all(engine)

# Create the session
session = sessionmaker()
session.configure(bind=engine)
s = session()

try:
    file_name = "emotions.csv"
    data = Load_Data(file_name)

    for i in data:
        record = Emotions_Data(**{
            'emotions':i[0],
            'emotion_confidence':float(i[1]),
            'sentence':i[2],

        })
        s.add(record)  # Add all the records
        s.commit()  # Attempt to commit all the records
except:
    s.rollback()  # Rollback the changes on error
finally:
    app.run()
    s.close()  # Close the connection