# Tracking #

```
~/Desktop/check_audio.desktop
	~/AIY-projects-python/checkpoints/check_audio.py
		~/AIY-projects-python/src/aiy/audio.py
			aiy._drivers._player
			aiy._drivers._recorder
			aiy._drivers._tts
```

## aiy._drivers._player ##

AIY-projects-python/src/aiy/_drivers/_player.py

```
$ arecord --version
arecord: version 1.1.3 by Jaroslav Kysela <perex@perex.cz>
```

## aiy._drivers._recorder ##

AIY-projects-python/src/aiy/_drivers/_recorder.py

```
$ aplay --version
aplay: version 1.1.3 by Jaroslav Kysela <perex@perex.cz>
```

## aiy._drivers._tts ##

AIY-projects-python/src/aiy/_drivers/_tts.py

```
$ pico2wave --usage
Usage: pico2wave [-?] [-w|--wave=filename.wav] [-l|--lang=lang] [-?|--help] [--usage] <words>
```

# Library #

```
$ PYTHONPATH=$PYTHONPATH:/home/pi/AIY-projects-python/src python3 your_code.py
```

# Resouce #

## Speech to text - SpeechRecognition ##

```
$ sudo pip3 install speechrecognition
```

### Usage ###

```
import speech_recognition as sr

r = sr.Recognizer()
r.energy_threshold = 4000

with sr.WavFile(input_wav_file_path) as source:
	audio = r.record(source)
	wav_to_text = r.recognize_google(audio, language='zh_TW')
	if wav_to_text == "天氣":
		pass
```

## Text to Speech - gtts ##

```
$ sudo pip3 install gtts
```

### Usage ###

```
from gtts import gTTS
from tempfile import NamedTemporaryFile

mp3_path = NamedTemporaryFile(delete=True)
tts = gTTS(text = text , lang='zh-tw')
tts.save(mp3_path.name)
```

## MP3 to Wav - pydub (via ffmpeg) ##

```
$ sudo pip3 install pydub
```

### Usage ###

```
from pydub import AudioSegment
sound = AudioSegment.from_mp3(mp3_path.name)
sound.export(wav_path, format="wav")
```

# Service #

## Weather - https://wttr.in ##

```
$ curl -s 'http://wttr.in/Taipei?0&lang=zh'
天氣預報： Taipei, Taiwan

    \  /       局部多云
  _ /"".-.     10-11 °C
    \_(   ).   ↖ 9 km/h
    /(___(__)  10 km
               0.0 mm

$ loc=`curl -s ipinfo.io/city` && curl -s "http://wttr.in/$loc?0&lang=zh"
天氣預報： Taipei, Taiwan

    \  /       局部多云
  _ /"".-.     10-11 °C
    \_(   ).   ↖ 9 km/h
    /(___(__)  10 km
               0.0 mm
```

## Weather - https://works.ioa.tw/weather ##

```
$ curl -s https://works.ioa.tw/weather/api/weathers/1.json | jq '.specials[0]'
{
  "title": "低溫特報",
  "status": "低溫",
  "at": "2018-03-09 21:10:00",
  "desc": "強烈大陸冷氣團及輻射冷卻影響，氣溫明顯偏低，預計今（９）日至明（１０日）晨臺灣中部以北、東北部沿海空曠地區及馬祖、 金門夜晚至清晨易出現攝氏１０度左右低溫，農漁養殖業及山坡地作物請嚴防寒害，民眾亦請注意保暖，使用瓦斯熱水器具應注意室內通風，以免一氧化碳中毒。",
  "img": "Hypothermia.png"
}
```
