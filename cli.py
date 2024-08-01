#!/usr/bin/env python3

from interclaude import WhisperMic

#　interrobot2ver2　がGPT同士2人
# interrobot2ver5　がGPT同士3人
# interrobot2ver6　がGPT同士3人,性格あり
# interrobot2ver7_2　がGPT同士3人,性格あり
# interrobot2ver8　がuser1人，GPT同士3人,性格あり，テキスト入力，userも平等に順番が回ってくる
#


def main():
    mic = WhisperMic()
    mic.text()        

if __name__ == "__main__":
    main()

