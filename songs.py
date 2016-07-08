#!/usr/bin/env
# -*- coding: utf-8 -*-

from datetime import datetime
import time
import requests
import csv
import openpyxl

class SongInfo:
	songCount = 0

	def __init__(self, timestamp, artist, song):
		self.timestamp = timestamp
		self.artist = artist
		self.song = song
		SongInfo.songCount += 1

	def displaySongCount(self):
		print "Total songs: %d" % SongInfo.songCount

	def displaySongInfo(self):
		print self.timestamp, ";", self.artist, "-", self.song


def get_songs():
	url = "http://www.helmiradio.fi/api/programdata/getlatest?_="
	r = requests.get(url)
	songs = r.json()

	length = len(songs['result'])
	current_song = songs['result'][0]
	
 	song_time = convert_time(current_song['timestamp'])
	song_artist = current_song['artist']
	song_name = current_song['song']
	# print song_time # + ": " + current_song['artist'] + " - " + current_song['song']

	s1 = SongInfo(song_time, song_artist, song_name)

	s_list = []

	i = 0

	while i != length:
		current_song = songs['result'][i]
	 	song_time = convert_time(current_song['timestamp'])
		song_artist = current_song['artist']
		song_name = current_song['song']

		s_list.append(SongInfo(song_time, song_artist, song_name))

		i += 1
		
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "Helmiradio song list"

	for s in s_list:
		#  save_to_csv_file(s.timestamp, s.artist.encode("utf-8"), s.song.encode("utf-8"))
		
		ws.append([s.timestamp, s.artist, s.song])

		print "%s; \'%s - %s\'" % (s.timestamp, s.artist, s.song)

	wb.save("song-list.xlsx")

def save_to_csv_file(time, artist, song):
	outputFile = open("song.csv", 'a')
	outputWriter = csv.writer(outputFile, delimiter=",")

	outputWriter.writerow([time, artist, song])

	outputFile.close()

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def convert_time(time_in_milliseconds):
	song_time = time_in_milliseconds / 1000
	song_time = time.strftime("%d/%m/%Y %H:%M", time.localtime(song_time))

	return song_time


def main():

	get_songs()


main()
