from flask import Flask, request, jsonify
import yt_dlp
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL gerekli'}), 400
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info.get('url')
            filename = info.get('title', 'video')
            
            return jsonify({
                'status': 'success',
                'url': download_url,
                'filename': f"{filename}.mp4",
                'title': filename
            })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

4. **"Commit changes"** tıklayın

---

## Adım 4: requirements.txt Ekleyin

1. Yine **"Add file"** → **"Create new file"**
2. **Dosya adı:** `requirements.txt`
3. Şu satırları yapıştırın:
```
Flask==2.3.2
yt-dlp==2023.11.16
Werkzeug==2.3.6
gunicorn==21.2.0
```

4. **"Commit changes"** tıklayın

---

## Adım 5: Render.com'da Ücretsiz Hosting

1. https://render.com/ adresine gidin
2. **Sign up** (GitHub hesabı ile giriş yapabilirsiniz)
3. **"New +"** → **"Web Service"** seçin
4. **"Connect GitHub"** seçin
5. `video-downloader-api` repository'sini seçin
6. Ayarlar:
   - **Name:** `video-downloader-api`
   - **Runtime:** `Python`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Free tier** seçin
7. **"Create Web Service"** tıklayın

Sunucu başlayacak. 2-3 dakika bekleyin.

---

## Adım 6: API URL'sini Kopyalayın

Render dashboard'da, deployment başarılı olunca şöyle bir link göreceksiniz:
```
https://video-downloader-api-xxx.onrender.com
