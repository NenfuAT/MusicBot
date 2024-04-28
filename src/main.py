# 必要モジュールのインポート
import discord
from discord import app_commands
import os
import get_mp3

TOKEN = os.environ['BOT_TOKEN']

musics=[]
loop=False
count=0

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

@tree.command(name='dis', description='VCからボットを退出させます')
async def disconnect(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    if voice_client is not None:
        channel_name = voice_client.channel.name
        await voice_client.disconnect()  # ボイスチャンネルを切断
        await interaction.response.send_message(f'{channel_name}から切断しました')
    else:
        await interaction.response.send_message('ボットがVCにいる必要があります')

@tree.command(name="add", description="URLから再生リストに追加します")
@app_commands.describe(url="Yotubeのリンク")
async def add(interaction: discord.Interaction, url: str):
        voice_client = interaction.guild.voice_client
        if voice_client is not None:
            await interaction.response.defer()
            global musics
            result,musics = await get_mp3.get_mp3(url,musics)  # 処理が終わるまで待機
            await interaction.followup.send(f"{result}")  # 結果をユーザーに知らせる
        else:
            await interaction.response.send_message('ボットがVCにいる必要があります')

@tree.command(name="list", description="再生リストを表示します")
async def show_playlist(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client is not None:
        # 再生リストが空かどうかを確認
        if not musics:
            await interaction.response.send_message("再生リストは空です")
        else:
            # 再生リストを番号付きで表示
            playlist = "\n".join([f"{index + 1}. {title}" for index, title in enumerate(musics)])  # インデックス番号を付ける
            await interaction.response.send_message(f"再生リスト:\n{playlist}")
    else:
        await interaction.response.send_message('ボットがVCにいる必要があります')

@tree.command(name="play", description="再生リストから曲を再生します")
async def play(interaction: discord.Interaction):
    # 再生終了を検知するためのコールバック関数
    async def on_audio_end(interaction, error):
        if error:
            print("Error:", error)
        else:
            global count
            count += 1
            
            if count < len(musics):
                voice_client = interaction.guild.voice_client
                voice_client.play(discord.FFmpegPCMAudio(musics[count]), after=lambda e: client.loop.create_task(on_audio_end(interaction, e)))
                await interaction.edit_original_response(content=f"再生中: {musics[count]}")
            else:
                await interaction.edit_original_response(content="再生が終了しました。")
                await interaction.voice_client.disconnect()

    global count
    count = 0

    # 再生終了を検知するためのコールバックをラップ
    async def on_audio_end_wrapper(error):
        await on_audio_end(interaction, error)

    voice_client = interaction.guild.voice_client

    if voice_client is None or not voice_client.is_connected():
        await interaction.response.send_message("ボイスチャンネルに参加していません")
        return

    # 音声再生中かどうか確認
    if voice_client.is_playing():
        await interaction.response.send_message("既に再生中です。")
        return


    if not musics:
        await interaction.response.send_message("再生リストが空です")
        return

    song_path = musics[count]

    # 最初の曲を再生し、afterにラップされたコールバックを指定
    voice_client.play(discord.FFmpegPCMAudio(song_path), after=lambda e: client.loop.create_task(on_audio_end_wrapper(e)))

    await interaction.response.send_message(f"再生中: {song_path}")


@tree.command(name="loop", description="再生リスト内の曲をループをON/OFFします")
async def loop(interaction: discord.Interaction):
    if(loop==False):
        loop==True
        await interaction.response.send_message(f"ループON")
    if(loop==True):
        loop==False
        await interaction.response.send_message(f"ループOFF")
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

