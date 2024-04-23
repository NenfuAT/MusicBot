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
    
@tree.command(name='join', description='ユーザーがいるVCにボットを参加させます')
async def join(interaction: discord.Interaction):
    # ボイスクライアントを取得
    voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)

    # 既存のボイスチャンネル接続を切断
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()  # ボイスチャンネルを切断
    # ユーザーがボイスチャンネルにいるか確認
    if interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.response.send_message('ボイスチャンネルに参加している必要があります')
        return  # 参加していない場合、何もせず終了
    # ユーザーのボイスチャンネルを取得
    voice_channel = interaction.user.voice.channel 
    
    if voice_channel is not None:
        # ボイスチャンネルに接続
        await voice_channel.connect()  # ボットがボイスチャンネルに接続
        await interaction.response.send_message(f'{voice_channel.name}に参加しました')

@tree.command(name='disconnect', description='VCからボットを退出させます')
async def join(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    if voice_client is not None:
        channel_name = voice_client.channel.name
        await voice_client.disconnect()  # ボイスチャンネルを切断
        await interaction.response.send_message(f'{channel_name}から切断しました')
    else:
        await interaction.response.send_message('ボイスチャンネルに接続していません')
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
