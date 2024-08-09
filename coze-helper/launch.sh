#!/bin/sh

BASE=/app
NAME=coze

cd $BASE
echo "waitting fetch $fetch"
curl -s "$fetch" -o helper.zip && unzip helper.zip

cd $BASE/${NAME}-helper
sed -i 's/puppeteerArgs\.push/\/\/ puppeteerArgs\.push/g' src/index.ts
sed -i 's/headless: false,/headless: "new",/g' src/index.ts

npm install && npm run start