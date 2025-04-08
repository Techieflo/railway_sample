import yt_dlp
from flask import Flask, jsonify, request
from pyngrok import ngrok, conf

# Set up ngrok auth token
conf.get_default().auth_token = "2vPdx6TtqOk0m91T03yRmyi3ZC5_4ZAvUDWedsxNeFVGshtyw"  # Replace with your ngrok token

# Create Flask app
app = Flask(__name__)

def get_download_links(video_url):
    ydl_opts = {
        'format': 'best',  # Get the best available quality (combined video + audio)
        'quiet': True,  # Suppress output
        'noplaylist': True,  # Don't process playlists
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            if info and 'url' in info:
                return {"video_audio_url": info.get('url', None)}
            else:
                return None
    except Exception as e:
        return str(e)

@app.route('/get_download_links', methods=['GET'])
def get_download_links_api():
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({'error': 'URL parameter is missing'}), 400

    download_links = get_download_links(video_url)

    if isinstance(download_links, dict):
        return jsonify({'download_links': download_links})
    else:
        return jsonify({'error': download_links}), 500

# Run server with ngrok
if __name__ == "__main__":
    public_url = ngrok.connect(5005)
    print(f" * ngrok tunnel available at: {public_url}")

    app.run(port=5005)
