# AI-Powered Short Video Generator
#### Video Demo:  <URL HERE>
#### Description:

<h1> Introduction to the project </h1>

Hello there! My name is João Albergaria, I'm a 20-year-old Computer Engineering undergraduate from Brazil. I began this course in my vacations in December of 2024 and completed it in January, starting the development of the final project. With the beginning of the new semester, however, I did not have much free time, so I only finished it now.

As its name implies, it is an automatic short video generator which only requires that the user choose the subject, duration, size (e.g. 1920x1080) and whether they want subtitles.

My primary source of inspiration was a YouTube video by Fuji Code, in which he achieves something similar using ChatGPT and Pexels API. His project differs from mine in the fact that I used the Deepseek R1 model (free) and Google Images search. Mine also receives multiple inputs for better customization of the video, while his uses only the subject.

<h1> Explanation </h1>

<h2> app.py </h2>

Here, I used the Flask framework for the application. It is a short code, being used to tie all of the JavaScript and Python interaction (AJAX), and to execute all of the functions involving the AI model and the assembly of the video itself in scriptgen.py.
It is worth noting that there is a try/catch structure in case of exceptions, which will most likely be caused by lack of tokens for the model (they are replenished the next day).

<h2> index.html </h2>

This is the web page itself, whose visuals were mostly made using Bootstrap — with the exception of the loading animation, which I got from <a href="https://www.w3schools.com/howto/howto_css_loader.asp" target="_blank">W3 Schools</a>.
The "logo" for the project was made using Canva, and the options for the video are a `<form>` tag which is submitted upon clicking the blue "Generate" button, activating the generateVidRequest(event) function in main.js.
There is also an empty div with the id of "container-vid", where the loading animation and, later on, the generated video will be displayed.

<h2> main.js </h2>

This JavaScript file is responsible for handling the interaction between what the user sees (the parameters they change, the command to start generating) and what is processed in the backend - the generation of the script and audio file, the image search, subtitle burning and video assembly.
Here, I used the AJAX technique in order to dynamically update the contents of the page without having to reload it. So, when the user clicks the "Generate" button, the generateVidRequest(event) function fetches /generating-vid with a few parameters through JSON. The Flask app.py receives them, and starts the generation pipeline through the methods imported from scriptgen.py. The video and its proportion are then sent back and displayed accordingly.

Other minor functions are one that replaces values in strings of text using Jinja, and another which updates the label of seconds when the user moves the input range marker for the duration.

<h2> scriptgen.py </h2>

This is where the magic happens. To execute it, an API key for the Deepseek R1 free model is needed, which I got from [OpenRouter](https://openrouter.ai).


