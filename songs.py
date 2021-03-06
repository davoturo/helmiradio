#!/usr/bin/env
# -*- coding: utf-8 -*-

from datetime import datetime
import time
import requests
import csv
import openpyxl


# saves the song info to a easier to edit format
class SongInfo:
	songCount = 0 # song counter

	def __init__(self, timestamp, artist, song):
		self.timestamp = timestamp  # timestamp in milliseconds
		self.artist = artist # artist name
		self.song = song #  song name
		SongInfo.songCount += 1  # increase song counter

		# keeps track of amount of songs
	def displaySongCount(self):
		print "Total songs: %d" % SongInfo.songCount


#  downloads the json file from helmiradio.fi and more
def get_songs():
	url = "http://www.helmiradio.fi/api/programdata/getlatest?_=" #  url to api 
	r = requests.get(url) #  using requests to get the json file
	songs = r.json()  # parsing to json

	length = len(songs['result'])  # total of songs in json file (max 978)	

	s_list = [] # list for all songs
	i = 0

	# this puts all songs (timestamp, artist, song-name) to s_list
	while i != length:
		current_song = songs['result'][i] # current song
	 	song_time = convert_time(current_song['timestamp']) # songs timestamp
		song_artist = current_song['artist'] # artist
		song_name = current_song['song'] # song name

		#  adds to s_list
		s_list.append(SongInfo(song_time, song_artist, song_name))

		i += 1
	
	"""
	# used to save song info to a xlsx file
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "Helmiradio song list"
	"""
	for s in s_list:

		#  save_to_csv_file(s.timestamp, s.artist.encode("utf-8"), s.song.encode("utf-8")) #  uncomment to save as csv file
		
		#  ws.append([s.timestamp, s.artist, s.song])

		print "%s; \'%s - %s\'" % (s.timestamp, s.artist, s.song)

	# wb.save("song-list.xlsx")

#  save songs to a csv file
def save_to_csv_file(time, artist, song):
	outputFile = open("song.csv", 'a')
	outputWriter = csv.writer(outputFile, delimiter=",")

	outputWriter.writerow([time, artist, song])

	outputFile.close()

# necessary for songs with special characters
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

#  converts the time from unix time
def convert_time(time_in_milliseconds):
	song_time = time_in_milliseconds / 1000 # changes time to seconds 
	song_time = time.strftime("%d/%m/%Y %H:%M", time.localtime(song_time)) # formats time

	return song_time # return formatted time

#  main
def main():
	#  calls get_songs()
	get_songs()


#  calls main
main()