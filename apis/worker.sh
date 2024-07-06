#!/bin/sh

cd /app/firecrawl/apps/api
pnpm install && pnpm run build
nohup pnpm run start:production  > /app/out.log 2>&1 &
nohup pnpm run worker:production > /app/out.log 2>&1 &


git clone https://github.com/bincooo/worker-laf.git /app/main
cd /app/main
pnpm install
pnpm dev
