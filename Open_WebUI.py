import argparse
import torch
parser = argparse.ArgumentParser()
parser.add_argument('--repo-id','-m', default='guillaumekln/faster-whisper-large-v2', help='Path to model repo (default: guillaumekln/faster-whisper-large-v2)')
parser.add_argument('--device','-d', default='cuda', help='Device to use for inference (default: cuda)')
parser.add_argument('--compute-type', default='float16', help='Compute type for inference (default: float16)')
parser.add_argument('--no-translate', action='store_true', help='Disable automatic translation')
# parser.add_argument('--trans-word-ts', action='store_true', help='If set, the program will generate word-level timestamps for translations. It may be unreliable.')
parser.add_argument('--force-overwrite','-f', action='store_true', help='If set, the program will overwrite any existing output files. If not set (default behavior), the program will skip writing to an output file that already exists.')
parser.add_argument('--translate-lang','-t', default=None, help='Translate to another language other than English. This is not an official behavior.')
parser.add_argument('--live', action='store_true', help='Enable live update of the output text')
parser.add_argument('--cache-dir', default=None, help='Directory of the folder to download models. Ex: "models" will make/use a folder named models in the same directory as this program (~\\models\\). The default directory is C:\\Users\\[username]\\.cache\\huggingface\\hub\\')
args = parser.parse_args()
print(args)
import glob
import os

if args.cache_dir:
    cache_dir = (args.cache_dir+"/"+args.repo_id.split("/")[-1])
else:
    cache_dir = args.repo_id

#os.environ['TRANSFORMERS_CACHE'] = cache_dir
#os.environ['PYTORCH_TRANSFORMERS_CACHE'] = '~/.cache/huggingfaces/'
#print(os.getenv('TRANSFORMERS_CACHE'))

#print(os.path.isdir(cache_dir))

if os.path.isdir(cache_dir):
    model_path = cache_dir
else:
    import huggingface_hub
    print("Downloading model...")
    kwargs = {}
    if cache_dir is not None:
        kwargs["local_dir"] = cache_dir
        kwargs["cache_dir"] = cache_dir
        # kwargs["local_dir"] = "C:/AI/MyThings/nimple Speech Recognition/ssd"
        # kwargs["cache_dir"] = "C:/AI/MyThings/nimple Speech Recognition/sfw"
        kwargs["local_dir_use_symlinks"] = False
    allow_patterns = ["config.json","model.bin","tokenizer.json","vocabulary.txt",]
    model_path=huggingface_hub.snapshot_download(args.repo_id,allow_patterns=allow_patterns,**kwargs)#tqdm_class=disabled_tqdm,,
    
print("Loading model...")         
from faster_whisper import WhisperModel

model = WhisperModel(model_path, device=args.device, compute_type=args.compute_type)
print("Model loaded.")  
supported_languages = [
    "",
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese",
    "Azerbaijani", "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian",
    "Breton", "Bulgarian", "Burmese", "Castilian", "Catalan", "Chinese",
    "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Faroese",
    "Finnish", "Flemish", "French", "Galician", "Georgian", "German", "Greek",
    "Gujarati", "Haitian", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew",
    "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese",
    "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Lao", "Latin",
    "Latvian", "Letzeburgesch", "Lingala", "Lithuanian", "Luxembourgish",
    "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori",
    "Marathi", "Moldavian", "Moldovan", "Mongolian", "Myanmar", "Nepali",
    "Norwegian", "Nynorsk", "Occitan", "Panjabi", "Pashto", "Persian",
    "Polish", "Portuguese", "Punjabi", "Pushto", "Romanian", "Russian",
    "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Sinhalese", "Slovak",
    "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish",
    "Tagalog", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tibetan",
    "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uzbek", "Valencian",
    "Vietnamese", "Welsh", "Yiddish", "Yoruba"
]            
language_codes = {
    "": "",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Azerbaijani": "az",
    "Bashkir": "ba",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Breton": "br",
    "Bulgarian": "bg",
    "Burmese": "my",
    "Castilian": "es",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Faroese": "fo",
    "Finnish": "fi",
    "Flemish": "nl",
    "French": "fr",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian": "ht",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Letzeburgesch": "lb",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Moldavian": "mo",
    "Moldovan": "mo",
    "Mongolian": "mn",
    "Myanmar": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nynorsk": "nn",
    "Occitan": "oc",
    "Panjabi": "pa",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Pushto": "ps",
    "Romanian": "ro",
    "Russian": "ru",
    "Sanskrit": "sa",
    "Serbian": "sr",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Sinhalese": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tibetan": "bo",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Valencian": "ca",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Yiddish": "yi",
    "Yoruba": "yo"
}
#from assgen import gen_subtitles

# Iterate through each audio file provided in the command line arguments
"""
for entry in audio_files:
    for audio_file in glob.glob(entry):
        # Extract the name of the file without its extension
        name = '.'.join(audio_file.split('.')[:-1])
        print('Transcribing '+name)

        if args.language is None:
            # Transcribe the audio using the provided model
            segments, info = model.transcribe(audio_file, beam_size=5, word_timestamps=True)
            
            # Print the detected language and its probability
            print(f"Detected language '{info.language}' with probability {info.language_probability}")
        
            language = info.language
        else:
            segments, info = model.transcribe(audio_file, beam_size=5, word_timestamps=True, language=args.language)
            language = args.language
        
        # Generate subtitles file with the same name as the original audio file and the detected language as the extension
        output_file = f"{name}.{language}.ass"

        if args.force_overwrite or not os.path.exists(output_file):
            
            gen_subtitles(segments, output_file)

            # If the detected language is not English, transcribe the audio using translation
            if not args.no_translate and (
                (args.translate_lang is None and language != 'en') or
                (args.translate_lang is not None and language != args.translate_lang)
                ):
                if args.translate_lang is not None:
                    segments, info = model.transcribe(audio_file, beam_size=5, language=args.translate_lang, word_timestamps=True) #args.trans_word_ts)
                else:
                    segments, info = model.transcribe(audio_file, beam_size=5, task='translate', word_timestamps=True)

                # output_file = f"{name}.en.translated"

                # Append English translation
                gen_subtitles(segments, output_file, append=True)
            
            # Print the name of the output subtitle file
            print(f"Subtitles saved to {output_file}")

        else:
            print(f"Skipping {output_file} (file already exists). Pass -f to overwrite existing files.")"""
ohNoButton=False

def iterate_segments(segments,output_txtFile,useNewLines,outputFileName):
    #for i, segment in enumerate(segments):
    wholeText_n=""
    prevNewline=True
    for segment in (segments):
        if ohNoButton:
            break
        if useNewLines==0:
            segmentText=segment.text.replace(". ",".\n").replace("! ","!\n").replace("? ","?\n")
            if segment.text[0]==" " and prevNewline==True:
                segmentText=segmentText.replace(" ","",1)  
                prevNewline=False
            if segment.text[-1]=="." or segment.text[-1]=="!" or segment.text[-1]=="?":
                segmentText=segmentText+"\n"
                prevNewline=True

        elif useNewLines==1:
            segmentText=(segment.text+"\n")
            if segment.text[0]==" ":
                segmentText=segmentText.replace(" ","",1)
        else:
            segmentText=segment.text
            
        if (output_txtFile):
            with open(outputFileName,'a') as f:
                f.write(segmentText)
                
                
        print(segmentText)
        wholeText_n=f"{wholeText_n}{segmentText}"
        yield wholeText_n
    print("__________DONE__________")
    return wholeText_n
        
       

                
                                
def generate_subtitles(audio_files, translate_lang='', language='', output_txtFile=True, useNewLines=2 , translate=True,  beam_size=5): #word_ts=True, attach=False,
    #clear txt files
    global ohNoButton
    if ohNoButton:
        ohNoButton=False
    #print(audio_files.orig_name)
    #print(audio_files.name)
    if output_txtFile:
        outputFileName = (audio_files.name.split('.')[-2].split('\\')[-1])
        open(f'{outputFileName}_transcript.txt','w').close()
        open(f'{outputFileName}_translate.txt','w').close()
    else:
        outputFileName=None
    #outputFileName=audio_files.split
    
    audio_files_path=audio_files.name.replace("\\","/")
    
    wholeText=""
    #print(audio_files)
    

    for audio_file in glob.glob(audio_files_path):
        name = '.'.join(audio_file.split('.')[:-1])
        print('Transcribing '+name)    
        if language == '':
            # Transcribe the audio using the provided model
            segments, info = model.transcribe(audio_file, beam_size=beam_size, word_timestamps=True)
            
            # Print the detected language and its probability
            print(f"Detected language '{info.language}' with probability {info.language_probability}")
        
            language = info.language
        else:
            segments, info = model.transcribe(audio_file, beam_size=beam_size, word_timestamps=True, language=language_codes[language])
            language = language
        for wholeText_n in iterate_segments(segments,output_txtFile,useNewLines,outputFileName=f'{outputFileName}_transcript.txt'):
            yield wholeText_n
        if translate and (
        (translate_lang == '' and language != 'en') or
        (translate_lang != '' and language != translate_lang)):
            if translate_lang != '':
                print("______________BEGINNING TRANSLATION______________")
                segments, info = model.transcribe(audio_file, beam_size=beam_size, language=language_codes[translate_lang], word_timestamps=True) #args.trans_word_ts)
            else:
                segments, info = model.transcribe(audio_file, beam_size=beam_size, task='translate', word_timestamps=True)
            for wholeText_n in iterate_segments(segments,output_txtFile,useNewLines,outputFileName=f'{outputFileName}_translate.txt'):
                yield wholeText_n
    ohNoButton=False      
    return wholeText
#generate_subtitles(args.audio_files, args.translate_lang)

def ohNo():
    global ohNoButton
    ohNoButton = True
    print("Stopping stuff")

import gradio as gr
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            audio_files = gr.File(label="Audio or video files to transcribe",type="file")#,file_types=['audio', 'video', '.flv'])
            translate_lang = gr.Dropdown(choices=supported_languages,label="Translate to language",allow_custom_value=True,value='')
            language = gr.Dropdown(choices=supported_languages, label="Force language",allow_custom_value=True,value='')
            output_txtFile = gr.Checkbox(label="Write output to text file", value=True)
            useNewLines = gr.Radio(["Per sentence", "Per computed segment", "Don\'t put Newlines"], label="Where to put new lines", info="Applies to both .txt file output (if enabled) and text box output", type="index", value="Don\'t put Newlines")
            translate = gr.Checkbox(label="Automatic translation", value=True)
            #word_ts = gr.Checkbox(label="Word-level timestamps", value=True)
            #attach = gr.Checkbox(label="Produce a video with embedded subtitles")
            beam_size = gr.Number(label="Beam size", value=5, precision=0)
            button = gr.Button("Do Stuff")
            stopButton = gr.Button("Stop Stuff",variant="stop")
            
        with gr.Column():
            output_text = gr.Textbox(label='Output subtitle files',max_lines=30,interactive=True)
    button.click(generate_subtitles, 
    inputs=[
    audio_files, 
    translate_lang, 
    language, 
    output_txtFile, 
    useNewLines,
    translate,
    #word_ts, 
    #attach,
    beam_size
    ], outputs=output_text)
    stopButton.click(ohNo, None, None, queue=False)
demo.queue(max_size=30)
demo.launch(inbrowser=True, show_error=True, share=False)       

