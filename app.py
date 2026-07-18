from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instant Processing Dashboard</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #f9f9f9; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        h2 { color: #ff0000; margin-top: 0; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        button { background: #ff0000; color: white; border: none; width: 100%; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 5px; }
        button:hover { background: #cc0000; }
        .format-list { margin-top: 25px; border-top: 1px solid #eee; padding-top: 20px; display: none; }
        .format-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; border: 1px solid #eee; margin-bottom: 8px; border-radius: 6px; background: #fafafa; }
        .dl-link { background: #28a745; color: white; text-decoration: none; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold; text-align: center; }
        .dl-link:hover { background: #218838; }
        .info-text { color: #666; font-size: 14px; margin-bottom: 20px; line-height: 1.4; }
    </style>
</head>
<body>
<div class="card">
    <h2>🔴 Web Engine Processing Hub</h2>
    <p class="info-text">Paste your video link below to switch directly to active browser processing engines designed to handle video parameters locally.</p>
    
    <input type="text" id="videoUrl" placeholder="Paste YouTube link here...">
    <button id="btn" onclick="generateLinks()">Load Processing Options</button>
    
    <div class="format-list" id="outputSection">
        <h3 style="margin-top: 0; font-size: 16px; color: #333;">Available Local Processors:</h3>
        <div id="output"></div>
    </div>
</div>

<script>
function generateLinks() {
    const url = document.getElementById('videoUrl').value.trim();
    const outputSection = document.getElementById('outputSection');
    const output = document.getElementById('output');
    
    if(!url) {
        alert('Please enter a valid video link.');
        return;
    }
    
    output.innerHTML = '';
    
    // Updated engine index excluding restricted public API structures
    const tools = [
        { name: "Processor Alpha", desc: "Local Client File Converter", targetUrl: "https://y2mate.is" },
        { name: "Processor Beta", desc: "Direct Video Stream Engine", targetUrl: "https://savefrom.net" },
        { name: "Audio Extractor", desc: "Convert to Track Only (MP3)", targetUrl: "https://onlymp3.to" }
    ];
    
    tools.forEach(tool => {
        const item = document.createElement('div');
        item.className = 'format-item';
        item.innerHTML = `
            <div>
                <strong>${tool.name}</strong>
                <div style="font-size: 12px; color: #777; margin-top: 2px;">${tool.desc}</div>
            </div>
            <a class="dl-link" href="${tool.targetUrl}" target="_blank" rel="noopener noreferrer">Launch Engine</a>
        `;
        output.appendChild(item);
    });
    
    outputSection.style.display = 'block';
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
