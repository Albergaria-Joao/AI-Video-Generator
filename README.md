# AI-Powered Short Video Generator
#### Video Demo:  https://youtu.be/t46MXgPe-wA
#### Description:

<h2> Introduction to the project </h2>

Hello there! My name is João Albergaria, I'm a 20-year-old Computer Engineering undergraduate from Brazil. I began this course in my vacation in December of 2024 and completed it in January, when I began the development of the final project. With the start of the new semester, however, I did not have much free time, so I only managed to finish it now.

As the name suggests, this is an automatic short video generator, which only requires the user to simply choose the subject, duration, size (e.g., 1920x1080) and whether they want subtitles.

My primary source of inspiration was a YouTube video by Fuji Code, in which he built something similar using ChatGPT and Pexels API. My project differs in that it uses the Deepseek R1 model (free) and Google Images search. Additionally, my generator accepts multiple inputs for greater customization of the video, while his requires only the subject.

<h2> Explanation </h2>

<h3> app.py </h3>

Here, I used the Flask framework for the application. It is a short code, being used to tie all of the JavaScript and Python interaction via AJAX, and to execute all of the functions involving the AI model and the assembly of the video itself in scriptgen.py.
It is worth noting that there is a try/except structure in case of exceptions, which will most likely be caused by lack of tokens for the model (they are replenished daily).

<h3> index.html </h3>

This is the front-end web page, whose visuals were mostly built using Bootstrap — with the exception of the loading animation, which was sourced from <a href="https://www.w3schools.com/howto/howto_css_loader.asp" target="_blank">W3 Schools</a>.
The "logo" for the project was made using Canva, and the options for the video are in a `<form>` tag which is submitted upon clicking the blue "Generate" button, activating the `generateVidRequest(event)` function in main.js.
There is also an empty div with the id of "container-vid", where the loading animation and, later, the generated video will be displayed.

<h3> main.js </h3>

This JavaScript file is responsible for handling the interaction between what the user sees (the parameters they change, the command to start generating) and what is processed in the backend - the generation of the script and audio file, the image search, subtitle burning and video assembly.
Here, I used the AJAX technique in order to dynamically update the contents of the page without having to reload it. So, when the user clicks the "Generate" button, the `generateVidRequest(event)` function disables all user input and fetches /generating-vid with the chosen parameters through JSON. The Flask app.py receives them, and starts the generation pipeline through the methods imported from scriptgen.py. The video and its proportion are then sent back and displayed accordingly, and the user input is re-enabled so that they may generate other videos.

Other minor functions are one that replaces values in strings of text using Jinja, and another which updates the label of seconds when the user moves the duration range marker.

<h3> scriptgen.py </h3>

This is where the magic happens. To execute it, an API key for the Deepseek R1 free model is needed, which can be obtained from <a href="https://www.openrouter.ai" target="_blank">OpenRouter</a>. 

The first method is `generate_script()`, which uses a prompt to generate the script of the video based on a given subject for the chosen duration. There are many clauses to specify that the model must generate only the script, without special characters. All of it, as well as the other methods involving the AI model, is wrapped in a loop that is only broken when text is actually generated (as a recurring error during the early stages of development was that sometimes only an empty string `""` would be returned).
Upon completion of the script, gTTS is used to generate text-to-speech audio from it. The result does not always fit within the intended duration, but this difference is not big enough that it might be a problem.

Then, this script is summarized in `summarize_script()` so that it may be used to generate the queries (`generate_queries`) for the image search. This is especially useful when the subject is vague (such as "curious fact about ...") and the model itself chooses what the video will talk about, ensuring that the images are actually relevant.
The image search uses a library called `icrawler` and its method GoogleImageCrawler, going through each query and downloading them to the imgs folder. The number of pictures is the rounded value of the duration divided by 2. Each of them is then resized to fit the video size chosen in the beginning.

`assemble_vid` is responsible for tying it all up. It puts the images in sequence, adds the audio and subtitles (which are created in the `generate_subtitles()` method using the whisper library for recognition of speech) in case the user checked their checkbox. All of this is done using MoviePy, a library which acts as an editor of sorts. In order to be used, the developer must have the IMAGEMAGICK binary installed in their computer (which was not obvious at first).

The video is then rendered into the static/video/ folder and displayed for the user to watch and download.

<h2> Videos that inspired or helped me </h2>
<ul>
  <li><a href="https://youtu.be/mkZsaDA2JnA?si=OvdqXsp783EcghXL" target="_blank">I Automated YouTube Shorts with Python - Fuji Codes</a></li>
  <li><a href="https://youtu.be/Q2d1tYvTjRw?si=S_w6Tjri-X0a4V35" target="_blank">Automated Video Editing with MoviePy in Python - NeuralNine</a></li>
  <li><a href="https://youtu.be/ZmSb3LZDdf0?si=S9veDqVQ1q1nEyPW" target="_blank">Making Automatic YouTube videos with Python - Shifty the Dev</a></li>
  <li><a href="https://youtu.be/flD7gJSY9z4?si=hGmCv7K_Vl8qt6Bf" target="_blank">DeepSeek R1 API in Python: Chat Tutorial for Real-Time Reasoning & History Context - Coding Together</a></li>
</ul>



