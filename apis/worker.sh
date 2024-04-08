git clone https://github.com/bincooo/worker-laf.git /app/main
cd /app/main
pnpm install
nohup pnpm run dev > out.log 2>&1 &