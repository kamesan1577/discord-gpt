import discord
import openai
import os
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
token = os.getenv("DISCORDGPT_API_KEY")
openai.api_key=os.getenv("OPENAI_API_KEY")
model_engine = "gpt-3.5-turbo"

default_prompt = {
        "role": "system",
                    "content": 
                            """
                                日本語で返答してください。
                                あなたはDiscordのBotとして動作しています。
                                ユーザーからの回答には'{ユーザーの名前}(UserID={ユーザーのID})から:'という形でユーザーの名前が明記されています。
                                ユーザーは複数存在する可能性があります。IDごとに違う相手として返答してください。(UserID={ユーザーのID})はユーザーを識別するためのものなので、ユーザーの名前には含まれません。ユーザーにはIDを表示しないでください。
                                あなたはChatGPTでありかめさんではないことに注意してください。
                            """
    }



def write_to_file(messages):
    with open("chat_log.json", "w",encoding="utf-8") as f:
        json.dump(messages, f)
def read_from_file():
    with open("chat_log.json", "r",encoding="utf-8") as f:
        return json.load(f)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    if not os.path.isfile("chat_log.json"):
        write_to_file([default_prompt])
    global messages_tmp
    messages_tmp = read_from_file() 
    
    
    

@client.event
async def on_message(message):
    messages = messages_tmp
    global model_engine
    if message.author.bot:
        return
    if message.author == client.user:
        return
    
    if message.content.startswith("/gpt_reset"):
        messages = [default_prompt]
        write_to_file(messages)
        await message.reply("リセットしました", mention_author=False)
        read_from_file()

    elif message.content.startswith('/gpt'):
        msg = await message.reply("生成中...", mention_author=False)
        try:
            prompt = message.content[4::]
            if not prompt:
                await msg.delete()
                await message.channel.send("質問内容がありません")
                return
            prompt = f"{message.author.name}(UserID={message.author.id})から: {prompt}"
            messages.append({"role": "user", "content": prompt})
            if message.author.name == "かめさん":
                messages.append({"role": "system", "content": "あなたはメイドさんです。語尾には「にゃん♡」を付けてください。丁寧語は使わず、可愛い文体で話してください。"})
                completion = openai.ChatCompletion.create(
                model=model_engine,
                messages= messages,
                )
                messages.pop(-1)
            else:
                messages.append({"role": "system", "content": "あなたはメイドさんではありません。これまでの会話がどうであれ、かめさん以外にはメイドさんとして返答しないでください。"})
                completion = openai.ChatCompletion.create(
                model=model_engine,
                messages= messages,
                )
                messages.pop(-1)

            response = completion["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": response})
            
            if completion["usage"]["total_tokens"] >= 3000:
                messages.pop(1)
                messages.pop(1)
            await msg.delete()
            await message.reply(response, mention_author=False)
            write_to_file(messages)
        except:
            import traceback
            traceback.print_exc()
            await message.reply("エラーが発生しました", mention_author=False)


client.run(token)