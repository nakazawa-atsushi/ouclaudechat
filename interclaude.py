import openai
import json
import os
import tempfile
import requests
import simpleaudio
import queue
import threading
import random
import time

import gesture
from chatv3claude import chat
# from message.message_u1r3 import message
from message2.messageCv4 import message


class WhisperMic:
  def __init__(self):
    self.vv_queue = queue.Queue()
    self.gpt_queue = queue.Queue()
    self.wav_switch = True
    self.vv_switch = True
    self.gpt_switch = True
    self.speaker_num = 0  #num=0はユーザー
    self.mute = False
    self.message = message()
    print("aa")


    # openai.api_key = os.environ["OPEN_API_KEY"]
  
  def prevv(self):
    while True:
      if not self.gpt_switch and not self.vv_switch and not self.wav_switch:
          self.gpt_switch = True
          self.vv_switch = True
          self.wav_switch = True
          print("wav end")
          # print(f"gpt:{self.gpt_switch},vv:{self.vv_switch},wav{self.wav_switch}")     
          return
      
      # print(f"Checking gpt_queue size: {self.gpt_queue.qsize()}, gpt_switch: {self.gpt_switch}")
      # time.sleep(1) #この遅延で競合しなくなるらしい⇒嘘でした
      if self.gpt_queue.qsize() == 0 and self.gpt_switch == False:
        # print("vv stop")
        self.vv_switch = False
        # print(f"gpt:{self.gpt_switch},vv:{self.vv_switch},wav{self.wav_switch}")     
        continue

      # print("get before")
      try:
        # print("try")
        text = self.gpt_queue.get_nowait()
      except queue.Empty:
        time.sleep(0.1)
        # print("pass")
        continue
      
      # text = self.gpt_queue.get_nowait()
      # text = self.gpt_queue.get()
      
      # print("get after")
      if self.speaker_num == 1:
        voice = self.voicevox(text,2)
      if self.speaker_num == 2:
        voice = self.voicevox(text,3)
      if self.speaker_num == 3:
        voice = self.voicevox(text,29)
      
      self.vv_queue.put_nowait(voice)
      
  def voicevox(self,text,speker_ID):
    host = "127.0.0.1" # "localhost"でも可能だが、処理が遅くなる
    port = 50021
    voice = bytes()
    # self.gpt_switch = True
    print("f")
    params = (
        ("text", text),
        ("speaker", speker_ID) # 音声の種類をInt型で指定
    )
    response1 = requests.post(
        f"http://{host}:{port}/audio_query",
        params=params
    )

    response2 = requests.post(
        f"http://{host}:{port}/synthesis",
        headers={"Content-Type": "application/json"},
        params=params,
        data=json.dumps(response1.json())
    )   
    print("ff")
    voice = response2.content
    return voice
        

  def wavplay(self):
    print("a")
    
    print("b")
    while True:
      if self.vv_queue.qsize() == 0 and self.vv_switch == False:
          self.wav_switch = False
          # print(self.gpt_switch)
          # print(self.vv_switch)
          # print(self.wav_switch)
          print("wav stop")
          # continue

      # try:      
      #   audio = self.vv_queue.get_nowait()
      # except:
      #   continue
      
      # audio = self.vv_queue.get_nowait()
      audio = self.vv_queue.get()      
      with tempfile.TemporaryDirectory() as tmp:
        print("g")
        with open(f"{tmp}/audi.wav", "wb") as f:
          f.write(audio)
          wav_obj = simpleaudio.WaveObject.from_wave_file(f"{tmp}/audi.wav")
          play_obj = wav_obj.play() #Starts playback of the audio
          play_obj.wait_done() #Waits for the playback job to finish before returning.
          print("h")
          # print(f"gpt:{self.gpt_switch},vv:{self.vv_switch},wav{self.wav_switch}")          
      # time.sleep(0.5) #この遅延で競合しなくなるらしい

  def switchcheck(self):
    return
    import time
    while True:
      print(f"gpt:{self.gpt_switch}, vv:{self.vv_switch}, wav:{self.wav_switch}")
      print(f"Checking gpt_queue size: {self.gpt_queue.qsize()}, gpt_switch: {self.gpt_switch}, gpt_queue.empty: {self.gpt_queue.empty()}")
      time.sleep(4)


  def text(self):
    thread_wav = threading.Thread(target=self.wavplay, daemon=True)
    thread_wav.start()
    
    # messagesa = []
    # messagesb = []
    # messagesc = []


    # with open('commu_gesturever2.txt','r',encoding='UTF-8') as f:
    #   command = f.read()
    
    # speaker_numDC = 00  #重複確認（Duplicate Confirmation）用，同じ人が連続で話さないようにする
    thread_s = threading.Thread(target=self.switchcheck, daemon=True)
    thread_s.start()
    
    speakerlist = list(range(1,4))  #ある程度平等に会話の機会があるようにしている，ただのランダム生成だとずっと2人だけ話したりするかも
    random.shuffle(speakerlist)
    print("DC")

    while True:
      
      if self.mute == True:
        continue
      # print("start")
      # print("messge:", end = "")
      # x = input()
      # x.encode('utf-8')
      x = input("message:")
      x.encode('utf-8')
      # messagesa,messagesb,messagesc=message(messagesa,messagesb,messagesc,x,0)
      self.message.append_context(x, 0)

      speakerlist = list(range(1,4))  #ある程度平等に会話の機会があるようにしている，ただのランダム生成だとずっと2人だけ話したりするかも
      random.shuffle(speakerlist)
      print("DC")

      for i in range(len(speakerlist)):
        emotion_flag = False
        print(speakerlist)
        self.speaker_num = speakerlist.pop(0)
        if not speakerlist:
          speker_next = 0
        else:
          speker_next = speakerlist[0]
        # if self.speaker_num == speaker_numDC: #前試行と同じ番号なら一度飛ばす
        #   print("miss")
        #   continue
        # speaker_numDC = self.speaker_num  #前試行と違う番号ならDCを書き換えて番号を記憶する
        
        gesture.direction(self.speaker_num,speker_next)
        
        print("tambo")
        
        thread2 = threading.Thread(target=self.prevv, daemon=True)
        thread2.start()
        print("kawa")
        total = ""
        print("miti")
        system , lastconv = self.message.prompt(self.speaker_num)
        # print(system)
        if self.speaker_num == 1:
          name = "四国メタン(average)"
        elif self.speaker_num == 2:
          name = "ずんだもん(selfcenter)"
        elif self.speaker_num == 3:
          name = "ナンバーセブン(reserve)"

        # print("lastconv")
        # print(lastconv)
        
        for talk in chat(system, lastconv):
          # print(f'四国めたん:{talk}')
          self.gpt_queue.put_nowait(talk)
          total += talk
          print(f'{name}: {total}')
          if emotion_flag == False and len(total) > 20:
            emotion_flag = True
            gesture.emotion(total,self.speaker_num)
        # messagesa,messagesb,messagesc=message(messagesa,messagesb,messagesc,total,self.speaker_num)
        self.gpt_switch = False

        self.message.append_context(total, self.speaker_num)
          
        """
        elif self.speaker_num == 2:
          for talk in chat(messagesb):
            # print(f'ずんだもん:{talk}')
            self.gpt_queue.put_nowait(talk)
            total += talk
            print(f'ずんだもん:{total}')
            if emotion_flag == False and len(total) > 20:
              emotion_flag = True
              gesture.emotion(total,self.speaker_num)
          messagesa,messagesb,messagesc=message(messagesa,messagesb,messagesc,total,self.speaker_num)
          
        elif self.speaker_num == 3:
          for talk in chat(messagesc):
            # print(f'ナンバー7:{talk}')
            self.gpt_queue.put_nowait(talk)
            total += talk
            print(f'ナンバー7:{total}')
            if emotion_flag == False and len(total) > 20:
              emotion_flag = True
              gesture.emotion(total,self.speaker_num)
          messagesa,messagesb,messagesc=message(messagesa,messagesb,messagesc,total,self.speaker_num)"""
        
        print("Toggle vv")
        self.gpt_switch = False
        thread2.join()
        print("thread stop")
      
