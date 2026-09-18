# Node.jsのLTSバージョンをベースイメージとして使用
FROM node:lts

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install pug sass typescript ts-loader astro --save-dev

# プロジェクトの残りの部分をコピー
# COPY . .

EXPOSE 3000

# コンテナを実行するコマンドを設定（必要に応じて変更）
# CMD ["npm", "run", "dev"]