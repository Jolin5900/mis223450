# Dockerfile

# 使用官方的 Python 3.13 最小映像檔作為基礎
FROM python:3.13-slim

# 安裝系統依賴 (編譯器、PortAudio 和 FFmpeg)
# build-essential 包含了 gcc, g++ 等編譯工具
RUN apt-get update && \
    apt-get install -y build-essential portaudio19-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /usr/src/app

# 複製依賴文件並安裝 Python 函式庫
COPY requirements.txt .
# --no-cache-dir 節省空間
RUN pip install --no-cache-dir -r requirements.txt

# 複製其餘程式碼
COPY . .

# 執行 Django 設置 (收集靜態檔案和資料庫遷移)
# 注意：您的 collectstatic 和 migrate 應該在 build 階段運行，而不是 start 階段。
RUN python manage.py collectstatic --no-input
# 暫時不運行 migrate，因為通常這應該在服務啟動後運行，但如果您的 settings.py 設置要求它，可以保留。
# 這裡先省略 migrate，因為 migrate 最好在單獨的 “Job” 或啟動時執行，避免競爭條件。

# 暴露服務端口
EXPOSE $PORT

# 啟動命令 (這是容器運行時執行的命令)
# $PORT 環境變數由 Render 自動注入
CMD gunicorn system.wsgi:application --bind 0.0.0.0:$PORT