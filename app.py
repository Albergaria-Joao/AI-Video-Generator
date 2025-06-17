from flask import Flask, jsonify, render_template, request
import os
from scriptgen import generate_script, generate_queries, get_img_crawler, assemble_vid, get_audio_duration, summarize_script


app = Flask("__name__")
app.secret_key = os.getenv("APP_KEY")


tokens = True

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/generating-vid", methods=["POST"])
def generate_vid():
    global tokens
    
    try:
        subject = request.json.get('vid_subject', 'Subject not provided')
        length = request.json.get('vid_length', 'Length not provided')
        check = request.json.get('sub_check', 'Check not provided')
        size = request.json.get('size', 'Size not provided')
        proportion = request.json.get('proportion', 'Proportion not provided')

        size_array = size.split("-")

        if (int(length) > 60):
            length = 60
        script = generate_script(subject, length)
        qtt = int(get_audio_duration("audio/audio.mp3"))/2
        summary = summarize_script(script)
        raw_queries = generate_queries(summary, qtt)
        print(subject)
        print(length)
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"vid": "ERROR"})
    get_img_crawler(raw_queries)
    assemble_vid(qtt, check, int(size_array[0]), int(size_array[1]))
    return jsonify({"vid": "../static/video/video.mp4", "proportion": proportion})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)