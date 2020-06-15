from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, jsonify
from pytube import YouTube
import os

# Flask parameters
application = app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
MYDIR = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = 'static/videos/'


# Main page
@app.route('/', methods=['post', 'get'])
def index():
    if request.method == 'POST':
        link = request.form.get('link')
        try:
            # object creation using YouTube which was imported in the beginning
            yt = YouTube(link)
        except:
            flash("Connection Error")  # to handle exception
            return render_template('index.html', ask=True)

        available = []
        resolutions = ['144p', '360p', '240p', '480p', '720p', '1080p']
        for res in resolutions:
            if yt.streams.filter(res=res, progressive="True").first():
                available.append(res)
        return render_template('index.html', link=link, title=yt.title, resolutions=available,
                               thumbnail=yt.thumbnail_url, ask=False)
    return render_template('index.html', ask=True)


# route for downloading the video to the server


# dynamic download link
@app.route('/videos/<path:filename>')
def download_file(filename):
    return send_from_directory(MYDIR + "/" + app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# route for downloading the video to the server
@app.route('/api/<string:video_id>/<string:resolution>')
def api(video_id, resolution):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        stream = yt.streams.filter(res=resolution, progressive="True").first()
        name = ''.join(i for i in yt.title if i.isalpha())
        stream.download('static/videos', name)

        return jsonify({'link': f'/videos/{name}.mp4'})
    except:
        return jsonify({'Api request status': '400 (Bad Request)'})


if __name__ == '__main__':
    app.run(debug=True)
