import joblib
import os
import os.path
from os import path
import discord
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from discord.ext import commands
from discord.ext import commands



positive = ['admiration', 'surprise','curiosity','desire','amusement', 'approval', 'caring', 'excitement','gratitude','joy', 'love', 'optimism', 'pride', 'relief']
negative = ['anger', 'annoyance', 'confusion','disappointment', 'disapproval', 'disgust', 'embarrassment', 'fear',  'grief', 'nervousness',  'realization', 'remorse', 'sadness']
emotions=["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise"]  
admiration_list=[] 
admiration_idx=0
admiration_val=0
amusement_list=[] 
amusement_idx=0
amusement_val=0
anger_list=[] 
anger_idx=0
anger_val=0
annoyance_list=[]
annoyance_idx=0
annoyance_val=0
approval_list=[]
approval_idx=0
approval_val=0
caring_list=[] 
caring_idx=0
caring_val=0
confusion_list=[] 
confusion_idx=0
confusion_val=0
curiosity_list=[] 
curiosity_idx=0
curiosity_val=0
desire_list=[] 
desire_idx=0
desire_val=0
disappointment_list=[] 
disappointment_idx=0
disappointment_val=0
disapproval_list=[] 
disapproval_idx=0
disapproval_val=0
disgust_list=[]
disgust_idx=0
disgust_val=0
embarrassment_list=[]
embarrassment_idx=0
embrassment_val=0
excitement_list=[] 
excitement_idx=0
excitement_val=0
fear_list=[] 
fear_idx=0
fear_val=0
gratitude_list=[] 
gratitude_idx=0
gratitude_val=0
grief_list=[] 
grief_idx=0
grief_val=0
joy_list=[] 
joy_idx=0
joy_val=0
love_list=[]
love_idx=0
love_val=0
nervousness_list=[]
nervousness_idx=0
nervousness_val=0 
optimism_list=[] 
optimism_idx=0
optimism_val=0
pride_list=[] 
pride_idx=0
pride_val=0
realization_list=[] 
realization_idx=0
realization_val=0
relief_list=[] 
relief_idx=0
relief_val=0
remorse_list=[] 
remorse_idx=0
remorse_val=0
sadness_list=[] 
sadness_idx=0
sadness_val=0
surprise_list=[]
surprise_idx=0
surprise_val=0
neutral_list=[]
neutral_idx=0
neutral_val=0
basepath="/content/drive/MyDrive/raahee_activity_recommendations/"
t=0
for emotion in emotions:
  filepath=basepath+emotion
  responsepath=filepath+"_responses.xlsx"
  if(os.path.exists(responsepath)):
     df=pd.read_excel(responsepath)
     emotion+="_list"
     for i in df['Unnamed: 0']:
        globals()[emotion].append(i)

  else:
    gifpath=filepath+"_gifs.xlsx"
    if(os.path.exists(gifpath)):
       df=pd.read_excel(gifpath) 
       emotion+="_list"
       for i in df['Unnamed: 0']:
         globals()[emotion].append(i)  

    else:
       moviepath=filepath+"_movies.xlsx"
       if(os.path.exists(moviepath)):
         df=pd.read_excel(moviepath)
         emotion+="_list"
         val=emotion
         val+="_val"
         globals()[val]=1
         t=1
         for i in df['Unnamed: 0']:
           globals()[emotion].append(i) 
       else:
         bookpath=filepath+"_books.xlsx"
         t=2
         val=emotion
         val+="_val"
         globals()[val]=2
         if(os.path.exists(bookpath)):
           df=pd.read_excel(bookpath)
           emotion+="_list"
           for i in df['Unnamed: 0']:
             globals()[emotion].append(i) 


client = discord.Client()
bot = commands.Bot(command_prefix='!')



#classifier = pipeline("text-classification",model='bhadresh-savani/bert-base-go-emotion')

   
def getEmotion(message):
  return classifier(message)[0]["label"]    

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('!pm'):
        await message.channel.send('')
         
    else:
       print(message.author)
       t=0
       msg = message.content
      
       print(msg)
       response = getEmotion(msg)
       print(response)
       ans=""
       greeting=""
       val=response+"_list"
       idx=response+"_idx"
       temp=response+"_val"
       print(idx)
       print(temp)
       print(globals()[temp])
       if response in positive:
            greeting = "Great to hear that <@{0.author.id}> !!!\n".format(message)
       elif response in negative:
            greeting = "<@{0.author.id}> I can completely understand what you're going through\n".format(message)
       if(globals()[temp]==1):
          greeting+="This movie made my day, hope it turns out the same for you too !\n"
       if(globals()[temp]==2):
           greeting+="I really enjoyed reading this book, I guess you must read it too!\n"
       t=0
       if(globals()[idx]<len(globals()[val])):
          ans=globals()[val][globals()[idx]]
          globals()[idx]+=1
       else:
         globals()[idx]=0
         if(len(globals()[val])!=0):
          ans=globals()[val][0]
         globals()[idx]+=1 

       await message.channel.send(greeting+ans)    

client.run(os.getenv("TOKEN"))
