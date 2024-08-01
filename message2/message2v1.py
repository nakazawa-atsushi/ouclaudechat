import datetime

class message:
    def __init__(self) -> None:
        dt_now = datetime.datetime.now()
        self.dt = dt_now.strftime("%Y-%m-%dT%H-%M-%S.%f")
        self.num = 00
        self.update_path()
        
    def update_path(self):
        if self.num == 1:
            self.path = 'cluster/average_metan.txt'
            self.name = "四国メタン"
        elif self.num == 2:
            self.path = 'cluster/rolemodel_zunda.txt'
            self.name = "ずんだもん"
        elif self.num == 3:
            self.path = 'cluster/researve_No7.txt'
            self.name = "ナンバーセブン"
        elif self.num == 0:
            self.path = None
            self.name = "ユーザー"
        else:
            self.path = None

    def prompt(self, speaker_num):
        self.num = speaker_num
        self.update_path()
        m = []
        with open(self.path,'r',encoding='UTF-8') as f:
            prompt = f.read()
        with open(f"message2/context/{self.dt}.txt",'r',encoding='UTF-8') as f:
            conversation = f.read().splitlines()  #conv_sofarは配列f
            total = ""
            total2 = ""
            for i in conversation[:-1]:   #後ろから2個目まで取得
                total += i  #足し合わせる
            for i in conversation[-1:]: #後ろから2個だけ取得
                total2 += i
            
        m.append({"role": "system", "content": prompt})    
        m.append({"role": "system", "content": """Do not repeat the same conversation as the one that immediately preceded it.
Be proactive in developing the conversation."""})
        m.append({"role": "system", "content": "下記はここまでの会話です"})
        m.append({"role": "system", "content":total})   
        m.append({"role": "system", 
                   "content":f"""{self.name}として下記の[YOUR OUTPUT]を埋める出力をしてください．
80文字以内で応答してください．
**********
[{self.name}としての発言]
[YOUR OUTPUT]
**********"""})
        m.append({"role": "system", "content":f"""下記は直前の会話です．{self.name}として必ず発言すること.
Do not repeat the same conversation as the one that immediately preceded it.lang:ja"""})
        m.append({"role": "system", "content":total2})
        m.append({"role": "assistant", "content":f"[{self.name}としての発言]"})
        print("prompt")
        
        return m

    def append_context(self, text, speaker_num):
        self.num = speaker_num
        self.update_path()
        
        with open(f"message2/context/{self.dt}.txt",'a',encoding='UTF-8') as f:
            f.write(f"[{self.name}としての発言]\n")
            f.write(f"{text}\n")
        
        print("append")