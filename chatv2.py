import openai
import os

def chat(messages=[],settings="",max_tokens=2000,temperature=0.,top_p=.1,presence_penalty=0.,frequency_penalty=0.):

    # やり取りの管理
    """
    messages = messages if messages is not None else []
    if settings and not messages:
      messages.append({"role": "system", "content": settings})    
    messages.append({"role": "user", "content": text})
    """
    openai.api_key = os.environ["OPEN_API_KEY"]
    
    # APIを叩く、streamをTrueに
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        stream=True)
        
    length = 0
    
    # 返答を受け取り、逐次yield
    response_text = ""
    total_text = ""
    for chunk in resp:
      if total_text.endswith(("。", "？", "！")) and length > 70:
        print("70 over")
        break
      
      if chunk:
        content = chunk['choices'][0]['delta'].get('content')
        if content:
          response_text += content
          total_text += content
          # print(f'res1:{response_text}')
          for split_word in ["、","。", "？", "！"]:
            if split_word in response_text:
              # print(f'res:{response_text}')
              length = length+len(response_text)
              yield response_text
              response_text = ""
    print(length)