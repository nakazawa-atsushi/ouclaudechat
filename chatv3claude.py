import anthropic
import os

def chat(system="",messages="",settings="",max_tokens=2000,temperature=0.,top_p=.1,presence_penalty=0.,frequency_penalty=0.):

    # やり取りの管理
    """
    messages = messages if messages is not None else []
    if settings and not messages:
      messages.append({"role": "system", "content": settings})    
    messages.append({"role": "user", "content": text})
    """
    client = anthropic.Anthropic()
    

    response_text = ""
    total_text = ""
    length = 0

    print(f"system:{system}")
    print(f"送信する単語：{messages}")

    # APIを叩く、streamをTrueに
    with client.messages.stream(
        model="claude-3-opus-20240229", 
        max_tokens=2000,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content":messages}]
    ) as resp:
      for content in resp.text_stream:
        if total_text.endswith(("。", "？", "！")) and length > 70:
          print("70 over")
          break
        response_text += content
        total_text += content
        for split_word in ["、","。", "？", "！"]:
          if split_word in response_text:
            # print(f'res:{response_text}')
            length = length+len(response_text)
            yield response_text
            response_text = ""

    
    """
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
    """