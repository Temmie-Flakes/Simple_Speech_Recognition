A simple implementation and UI of Audio-to-Text models. Specifically The faster whisper models (guillaumekln/faster-whisper-large-v2)<br />
I tried to make this installer beginner friendly. I used heavily modified code from [haveyouwantto/faster-whisper-transcription](https://github.com/haveyouwantto/faster-whisper-transcription)

quick install (windows):<br />
----
1. download this repo as a zip or using Git.
2. download and install [python 3.10.6](https://www.python.org/downloads/release/python-3106/) (recommended) and add to PATH (untested on later versions including 3.11.3)
3. ~~(download [ffmpeg](https://ffmpeg.org/download.html) and add to PATH if your using anything other than .wav [here's a guide](https://www.youtube.com/watch?v=5xgegeBL0kw)~~ 
>you "probably" don't need to do this step anymore: <br />
>tinywisper uses PyAV rather then ffmpeg. gradio uses ffmpy and ffmpeg but I am avoiding the parts of gradio that need it.
4. run Install.bat
5. run either RunBaseModel.bat (recommended if you have >8 gigs of Vram) or RunSmallModel.bat.

how to use:
----
1. drag or upload video or audio files into the file box.
2. hit `Do Stuff`

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
use whichever one that works
- hitting `Stop Stuff` interrupts the transcription if it gets stuck or is spitting out the same thing infinitely 
- hitting `Restart Program` Restarts the entire program automatically. It's mostly just for devlopment. You can use the same tab after it restarts.
- translating to a different language might not be reliable, not sure if it's the model or my implementation.
- When importing files, Gradio creates 2 temp files which are identical to the original file. This can take up space and cause a lot of read/writes to happen. Why does it make 2 and not 1 temp file? heck if i know... 
- all the files get stored locally and can be used offline once ran at least one time.<br />
all necessary files \*__should__\* all get stored within the same file as the program

- To run the program on another drive: DO INITIAL INSTALL ON C: DRIVE. run the installer and run the program once to let the model download into the modelsCache. THEN move the entire repo folder into another drive. 

The built in HuggingFace model installer cannot download models onto another drive (it installs it into user/.cache then moves it and it can't move files from one drive to another) so you have to download the models in C: drive then move it. The venv should work since the batch references the python executable directly rather than the activate.bat 

- Currently supports the models @ https://huggingface.co/guillaumekln


Todo:
----
- [ ] force gradio to stop making temporary files
- [ ] add autodetection for cuda gpu's
- [ ] force huggingfaceHub to move files onto different drive.
