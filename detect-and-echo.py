#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess

import speech_recognition as sr
from gtts import gTTS

import aiy.audio  # noqa
from aiy._drivers._hat import get_aiy_device_name

AIY_PROJECTS_DIR = '/home/pi/AIY-projects-python'
RECORD_DURATION_SECONDS = 3

def enable_audio_driver():
	print("Enabling audio driver for VoiceKit.")
	configure_driver = os.path.join(AIY_PROJECTS_DIR, 'scripts', 'configure-driver.sh')
	subprocess.check_call(['sudo', configure_driver])

def get_weather_event():
	ans = subprocess.check_output(['/bin/sh', '-c', "curl -s https://works.ioa.tw/weather/api/weathers/1.json | jq '.specials[0].desc'"]).decode("utf-8");
	return str(ans).strip("\n")

def get_weather_temperature():
	ans = subprocess.check_output(['/bin/sh', '-c', "curl -s https://works.ioa.tw/weather/api/weathers/1.json | jq '.temperature'"]).decode("utf-8")
	return str(ans).strip("\n")

def get_weather():
	ans = subprocess.check_output(['/bin/sh', '-c', "curl -s https://works.ioa.tw/weather/api/weathers/1.json | jq '.desc'"]).decode("utf-8")
	return str(ans).strip("\n")

def tts_wrap(text,wav_path,volumn=50):
	from tempfile import NamedTemporaryFile
	f = NamedTemporaryFile(delete=True)
	tts = gTTS(text = text , lang='zh-tw')
	tts.save(f.name)

	from pydub import AudioSegment
	sound = AudioSegment.from_mp3(f.name)
	sound = sound - (100 - volumn) # 小聲一點
	sound.export(wav_path, format="wav")

if __name__ == '__main__':
	enable_audio_driver()

	tts_temp_file, tts_temp_path = tempfile.mkstemp(suffix='.wav')
	os.close(tts_temp_file)

	temp_file, temp_path = tempfile.mkstemp(suffix='.wav')
	os.close(temp_file)

	r = sr.Recognizer()
	r.energy_threshold = 4000

	try:
		tts_wrap("嗨，您好，目前支援天氣指令有：特報, 溫度", tts_temp_path, 60)
		aiy.audio.play_wave(tts_temp_path)

		print('收音中..')
		aiy.audio.record_to_wave(temp_path, RECORD_DURATION_SECONDS)
        
		#print('播放錄製的聲音')
		#aiy.audio.play_wave(temp_path)

		print('分析中')
        
		with sr.WavFile(temp_path) as source:
           		audio = r.record(source)
            	
		try:
			wav_to_text = r.recognize_google(audio, language='zh_TW')
			print("指令：["+wav_to_text+"]")
			if wav_to_text.find('特報') != -1 :
				print("使用'特報'指令")
				text_report = get_weather_event()
				print("result:["+text_report+"]")
				if text_report == "null":
					text_report = "今天沒有天氣特報"
				print("echo:["+text_report+"]")
				tts_wrap(text_report, tts_temp_path, 65)
				import time
				time.sleep(3)	# wait
				aiy.audio.play_wave(tts_temp_path)
			elif wav_to_text.find('溫度') != -1 :
				print("使用'溫度'指令")
				text_report = get_weather_temperature()
				print("result:["+text_report+"]")
				text_report = "今天平均溫度"+text_report+"度C"
				print("echo:["+text_report+"]")
				tts_wrap(text_report, tts_temp_path, 65)
				import time
				time.sleep(3)	# wait
				aiy.audio.play_wave(tts_temp_path)
			else:
				print("無指令配對成功")
				text_report = get_weather()
				print("result:["+text_report+"]")
				text_report = "今天天氣"+text_report
				print("echo:["+text_report+"]")
				tts_wrap(text_report, tts_temp_path, 65)
				import time
				time.sleep(3)	# wait
				aiy.audio.play_wave(tts_temp_path)
			print("解析完畢")
		except Exception as e:
			print(e)
	finally:
		try:
			os.unlink(tts_temp_path)
		except FileNotFoundError:
			pass
		try:
			os.unlink(temp_path)
		except FileNotFoundError:
			pass
