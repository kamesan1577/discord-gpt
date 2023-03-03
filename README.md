# discord-gpt
## 概要
チャットGPTくんと楽しくお話できるDiscord Botです。
メッセージを送ったユーザーを判別することができるため、複数人が参加するサーバーでも使用可能です。
## 使用方法
### Discord上での使用方法
-/gpt {任意のテキスト}
  - GPTくんとの会話
- /gpt_reset
  - 会話履歴のリセット
### ターミナルでの設定(Ubuntu 22.04,Bash)
```
//環境変数の設定
$ export OPENAI_API_KEY="{OpenAIのAPIキー}"
$ export DISCORDGPT_API_KEY="{DiscordのAPIトークン}"

//Botの立ち上げ
//discord-gptのディレクトリ内で実行してください
$ pip install -r requirements.txt
$ python3 main.py
```

## 注意点
現段階ではインスタンスごとに会話履歴を保存する機能がないため、信頼できる友人がいるサーバーにのみ導入してください。
誰に見られても恥ずかしくないやりとりをしましょう。

また、GPTくんはかめさん以外にはメイドさんとして振る舞わないように設定されています。メイドさんになってほしい場合はソースコードを書き換えてください。
