A simple implementation and UI of Audio-to-Text models. Specifically The faster whisper models (guillaumekln/faster-whisper-large-v2)<br />
I tried to make this installer beginner friendly. I used heavily modified code from [haveyouwantto/faster-whisper-transcription](https://github.com/haveyouwantto/faster-whisper-transcription)

quick install (windows):<br />
----
1. download this repo as a zip or using Git.
2. download and install [python 3.10.6](https://www.python.org/downloads/release/python-3106/) (recommended) and add to PATH (untested on later versions including 3.11.3)
3. download [ffmpeg](https://ffmpeg.org/download.html) and add to PATH if your using anything other then .wav [here's a guide](https://www.youtube.com/watch?v=5xgegeBL0kw)
4. run Install.bat
5. run either RunBaseModel.bat (recommended if you have >8 gigs of Vram) or RunSmallModel.bat.

how to use:
----
1. drag or upload video or audio files into the file box.
2. hit "Do Stuff"

you have the option to automatically output a .txt file with the transcribed text. <br />

you have a choice putting a newline at the end of sentences (adds newline after .!?), between the computed segments (between the sliced audio that is fed into the AI), or none (one really long string of text)
<br />

you can translate the audio to many different languages 

you can edit the `--repo-id [hugging face repo name]` line in the batch file. look at `RunSmallModel.bat` for example.<br />

Notes:<br />
----
- If you don't have a cuda enabled GPU, edit RunBaseModel.bat and change:<br />
`venv\Scripts\python.exe Open_WebUI.py --cache_dir "modelsCache"` <br />
to:<br />
`venv\Scripts\python.exe Open_WebUI.py --cache_dir "modelsCache" --device "cpu"`<br />
or <br />
`venv\Scripts\python.exe Open_WebUI.py --cache_dir "modelsCache" --device "cpu" --compute_type "float32"` <br />
whichever one that works
- when translating to a different language that has non utf-8(ascii) characters (Korean, Chinese, Arabic, etc... ) TURN OFF WRITING TO TEXT FILE. this is due to python automatically assuming text to UTF-8 when writing to a file
- When importing files, Gradio creates 2 temp files which are identical to the origional file. This can take up space and cause alot of read/writes to happen. Why does it make 2 and not 1 temp file? heck if i know... 
- all the files get stored locally and can be used offline once ran atleast one time.<br />
all nessarry files \*__should__\* all get stored within the same file as the program

- To run the program on another drive: DO INITIAL INSTALL ON C: DRIVE. run the installer and run the program once to let the model download into the modelsCache. THEN move the entire repo folder into another drive. 

The built in HuggingFace model installer cannot download models onto another drive (it installs it into user/.cache then moves it and it cant move files from one drive to another) so you have to download the models in C: drive then move it. The venv should work since the batch refrences the python executible directly rather then the activate.bat 

- Currently supports the models @ https://huggingface.co/guillaumekln


Todo:
----
- [ ] Fix UTF-8 formatting when outputting to file
- [ ] force gradio to stop making temporary files
- [ ] add autodetection for cuda gpu's
- [ ] force huggingfaceHub to move files onto different drive.
