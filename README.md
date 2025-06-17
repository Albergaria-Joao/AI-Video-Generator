# AI-Powered Short Video Generator
#### Video Demo:  <URL HERE>
#### Description:

##### Introduction to the project

Hello there! My name is João Albergaria, I'm a 20-year-old Computer Engineering undergraduate from Brazil. I began this course in my vacations in December of 2024 and completed it in January, starting the development of the final project. With the beginning of the new semester, however, I did not have much free time, so I only finished it now.

As its name implies, it is an automatic short video generator which only requires that the user choose the subject, duration, size (e.g. 1920x1080) and whether they want subtitles.

My primary source of inspiration was a YouTube video by Fuji Code, in which he achieves something similar using ChatGPT and Pexels API. His project differs from mine in the fact that I used the Deepseek R1 model (free) and Google Images search. Mine also receives multiple inputs for better customization of the video, while his uses only the subject.

##### Explanation

###### app.py

Here, I used the Flask framework for the application. It is a short code, being used to tie all of the JavaScript and Python interaction (AJAX), and to execute all of the functions involving the AI model and the assembly of the video itself in scriptgen.py.
It is worth noting that there is a try/catch structure in case of exceptions, which will most likely be caused by lack of tokens for the model.

###### index.html

This is the web page itself, whose visuals were mostly made using Bootstrap — with the exception of the loading animation, which I got from <a href="https://www.w3schools.com/howto/howto_css_loader.asp" target="_blank">W3 Schools</a>.
The "logo" for the project was made using Canva, and the options for the video are a `<form>` tag which is submitted upon clicking the blue "Generate" button, activating the generateVidRequest(event) function in main.js.

###### main.js

This JavaScript file is responsible for 


