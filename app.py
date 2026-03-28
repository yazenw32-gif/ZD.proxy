import os
from flask import Flask, Response, request
import requests

app = Flask(__name__)

@app.route('/stream')
def stream_video():
    video_url = request.args.get('url') 
    if not video_url:
        return "No URL provided", 400

    # هيدرز لخدع السيرفرات العراقية (سينمانا وشاشتي)
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12)',
        'Referer': 'https://shashety.com/',
        'X-Requested-With': 'com.shashety.app'
    }
    
    try:
        # طلب الفيديو وتمريره للمشغل (Streaming)
        req = requests.get(video_url, headers=headers, stream=True, timeout=15)
        
        def generate():
            for chunk in req.iter_content(chunk_size=1024*1024):
                yield chunk

        return Response(generate(), content_type=req.headers.get('Content-Type'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # بورت 10000 هو المطلوب لسيرفرات الـ Cloud
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

