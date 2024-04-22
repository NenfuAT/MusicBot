# python version number:3.9.16
FROM python:3.9.16

# 作業ディレクトリ
WORKDIR /python/src/app/

# ローカルからコンテナへコピー
COPY ./src .

# upgrade pip コマンド
RUN pip install --upgrade pip 

# python ライブラリのインストール
RUN pip install -r requirements.txt