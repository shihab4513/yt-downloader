from flask import Flask, request, jsonify, render_template_string
import yt_dlp

app = Flask(__name__)

# Single-file layout: This serves the HTML frontend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live YouTube Downloader</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #f9f9f9; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        h2 { color: #ff0000; margin-top: 0; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        button { background: #ff0000; color: white; border: none; width: 100%; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        button:disabled { background: #ccc; }
        .loading { display: none; color: #666; margin: 10px 0; font-style: italic; }
        .format-list { margin-top: 20px; }
        .format-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; border: 1px solid #eee; margin-bottom: 5px; border-radius: 6px; }
        .dl-link { background: #28a745; color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-size: 14px; font-weight: bold; }
    </style>
</head>
<body>
<div class="card">
    <h2>🔴 Video Format Extractor</h2>
    <input type="text" id="videoUrl" placeholder="Paste YouTube link here...">
    <button id="btn" onclick="fetchFormats()">Extract Formats</button>
    <div class="loading" id="loader">Fetching direct video streams from YouTube...</div>
    <div class="format-list" id="output"></div>
</div>

<script>
async function fetchFormats() {
    const url = document.getElementById('videoUrl').value.trim();
    const btn = document.getElementById('btn');
    const loader = document.getElementById('loader');
    const output = document.getElementById('output');
    
    if(!url) return alert('Please enter a URL');
    
    btn.disabled = true;
    loader.style.display = 'block';
    output.innerHTML = '';
    
    try {
        const res = await fetch(`/get-formats?url=${encodeURIComponent(url)}`);
        const data = await res.json();
        
        if(data.error) throw new Error(data.error);
        
        data.formats.forEach(f => {
            const item = document.createElement('div');
            item.className = 'format-item';
            item.innerHTML = `
                <div><strong>${f.resolution}</strong> (${f.ext})</div>
                <a class="dl-link" href="${f.url}" target="_blank" download>Download</a>
            `;
            output.appendChild(item);
        });
    } catch(err) {
        alert('Error: ' + err.message);
    } finally {
        btn.disabled = false;
        loader.style.display = 'none';
    }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get-formats')
def get_formats():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400
        
    ydl_opts = {
        'skip_download': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats_list = []
            
            # Filter and grab formats that contain both video and audio together
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                    formats_list.append({
                        "resolution": f.get('format_note', 'Unknown'),
                        "ext": f.get('ext', 'mp4'),
                        "url": f.get('url') # This is the raw direct download link
                    })
            
            # Reverse so highest resolution appears first
            return jsonify({"formats": formats_list[::-1]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
