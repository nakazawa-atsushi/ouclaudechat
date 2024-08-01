import datetime

class message:
    def __init__(self) -> None:
        dt_now = datetime.datetime.now()
        self.dt = dt_now.strftime("%Y-%m-%dT%H-%M-%S.%f")
        self.num = 00
        self.update_path()
        self.m = []
        
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
        with open(self.path,'r',encoding='UTF-8') as f:
            prompt = f.read()
        with open(f"message2/context/{self.dt}.txt",'r',encoding='UTF-8') as f:
            # totalall = f.read()
            conversation = f.read().splitlines()  #conv_sofarは配列f
            total = ""
            total2 = ""
            for i in conversation[:-2]:   #後ろから2個目まで取得
                total += i  #足し合わせる
            for i in conversation[-2:]: #後ろから2個だけ取得
                total2 += i
        

        system = f'''{prompt}
Do not repeat the same conversation as the one that immediately preceded it.
Be proactive in developing the conversation.
下記はここまでの会話です
{total}
{self.name}として必ず発言してください
'''

        # m.append({"role": "user", "content":f"[{self.name}としての発言]"})
        # print(prompt)
        # print('total2')
        # print(total2)
        # print(conversation)
        # print(totalall)
        return system, total2


    def append_context(self, text, speaker_num):
        self.num = speaker_num
        self.update_path()
        
        with open(f"message2/context/{self.dt}.txt",'a',encoding='UTF-8') as f:
            f.write(f"[{self.name}としての発言]\n")
            f.write(f"{text}\n")
        
        # self.m.append({"role": "user", "content":f"[{self.name}としての発言]"})  
        # self.m.append({"role": "user", "content":text})

        print("append")