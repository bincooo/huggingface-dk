git clone https://github.com/bincooo/worker-laf.git /app/main
cd /app/main
pnpm install
nohup pnpm run dev > out.log 2>&1 &

# cd /app
# nohup ./free-gpt3.5-2api > gpt35.log 2>&1 &

cd /app/firecrawl/apps/api
pnpm install && pnpm run build
nohup pnpm run start:production  > out.log 2>&1 &
nohup pnpm run worker:production > out.log 2>&1 &
