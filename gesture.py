import openai
import os
from telnetlib import Telnet


openai.api_key = os.environ["OPENAI_API_KEY"]

def signal(sig,host):
    return
    HOST = host #有線のとき："172.28.66.91"
    try:
        tn = Telnet(HOST,10001)
        if "joy" in sig or "喜び" in sig: #
            tn.write(b"1\n")
        if "curiosity"  in sig or "好奇心" in sig: #elif
            tn.write(b"2\n")
        if "sadness" in sig or "悲しみ" in sig: #
            tn.write(b"3\n")
        if "anger" in sig or "怒り" in sig: #
            tn.write(b"4\n")
        if "neutral" in sig :
            tn.write(b"5\n")
        if "0" in sig:
            tn.write(b"0\n")
        if "00" in sig:
            tn.write(b"00\n")
            
        if "migi" in sig:
            tn.write(b"migi\n")
        if "massugu" in sig:
            tn.write(b"massugu\n")
        if "hidari" in sig:
            tn.write(b"hidari\n")
        tn.close()
    except Exception:
        print("Telnet不良")
    

def host(sig,speaker):
    if speaker == 1:
        host = "192.168.2.102"
        signal(sig,host)
    elif speaker == 2:
        host = "192.168.2.105"
        signal(sig,host)
    elif speaker == 3:
        host = "192.168.2.106"
        signal(sig,host)
    

def emotion(text,speaker):
    with open('commu_emotion.txt', 'r', encoding='UTF-8') as f:
            command = f.read()
    messages = [
        {"role": "system", "content": command},
        {"role": "user", "content": "今日は楽しかったです"},
        {"role": "assistant", "content": "joy"},
        {"role": "user", "content": "それは大変ですね"},
        {"role": "assistant", "content": "sadness"},
        {"role": "user", "content": text}
    ]
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    res = completion.to_dict()
    emo = res['choices'][0]['message']['content']
    print(f'emotion:{emo}')
    host(emo,speaker)


def direction(speaker,next):
    if speaker == 1:
        if next == 0:
            host("migi",speaker)
        elif next == 3:
            host("massugu",speaker)
        elif next == 2:
            host("hidari",speaker)
    elif speaker == 2:
        if next == 1:
            host("migi",speaker)
        elif next == 0:
            host("massugu",speaker)
        elif next == 3:
            host("hidari",speaker)
    elif speaker == 3:
        if next == 2:
            host("migi",speaker)
        elif next == 1:
            host("massugu",speaker)
        elif next == 0:
            host("hidari",speaker)