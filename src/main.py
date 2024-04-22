# 必要モジュールのインポート
import discord
from discord import app_commands
import os

TOKEN = os.environ['BOT_TOKEN']

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    # アクティビティを設定 
    new_activity = f"テスト" 
    await client.change_presence(activity=discord.Game(new_activity)) 
    # スラッシュコマンドを同期 
    await tree.sync()

# メッセージ受信時に動作する処理
@tree.command(name='neko', description='猫が鳴きます')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('にゃーん')


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
