#   Iterates through folders containing song tracks.
#   Combines songs in each folder based on requested 
#   instrumentation/vocals

#   Not finished or pythonic

#   Need to learn functions better

#   Reads INI's files for name/artist/instrumentation,
#   fixed all errors in INI's manually rather than
#   figure out how 'try' or error handling works. test

import os
from os import path
from pydub import AudioSegment
import configparser


def insert_overlay(string, string2):
    return f"{string[:1]}{string2}{string[1:]})"


insts = "NoVoxNoDrums"  # Songname - *insts* .mp3
wantBass = True    # Pick yer weapons (and noses)
wantGuitar = True
wantVocals = False
wantKeys = True
wantDrums = False

x = 0
count = 0
rootdir = 'ToConvert'  # input folder


for root, dirs, files in os.walk(rootdir):
    for folder in dirs:
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        print(os.path.join(root, folder))
        isRhythm, isGuitar, isKeys, isVocals, isDrums, drumber = "", "", "", "", "", ""
        config = ""
        if path.exists(os.path.join(root, folder, "song.ogg")):
            song = AudioSegment.from_file(os.path.join(root, folder, "song.ogg"))
            config = configparser.ConfigParser()
            config.read(os.path.join(root, folder, 'song.ini'))
            fname = config['song']['name']
            fartist = config['song']['artist']
            icon = config['song']['icon']

            name = fname.replace('/', '')
            artist = fartist.replace('/', '')
            if path.exists(f"PracOutput/{artist}/{name} - {artist} - {insts} - {icon}.mp3"):
                print("Song already completed!")
                count += 1
                print(f"{count} songs already completed")
                continue
            if path.exists(os.path.join(root, folder, "rhythm.ogg")):
                isRhythm = True
                rhythm = AudioSegment.from_file(os.path.join(root, folder, "rhythm.ogg"))
            elif path.exists(os.path.join(root, folder, "bass.ogg")):
                isRhythm = True
                rhythm = AudioSegment.from_file(os.path.join(root, folder, "bass.ogg"))
            if path.exists(os.path.join(root, folder, "guitar.ogg")):
                isGuitar = True
                guitar = AudioSegment.from_file(os.path.join(root, folder, "guitar.ogg"))
            if path.exists(os.path.join(root, folder, "vocals.ogg")):
                isVocals = True
                vocals = AudioSegment.from_file(os.path.join(root, folder, "vocals.ogg"))
            if path.exists(os.path.join(root, folder, "keys.ogg")):
                isKeys = True
                keys = AudioSegment.from_file(os.path.join(root, folder, "keys.ogg"))
            if path.exists(os.path.join(root, folder, "drums.ogg")) or path.exists(os.path.join(root, folder, "drums_1.ogg")):
                isDrums = True
                if path.exists(os.path.join(root, folder, "drums_4.ogg")):
                    drumber = 4
                    drums4 = AudioSegment.from_file(os.path.join(root, folder, "drums_4.ogg"))
                    drums3 = AudioSegment.from_file(os.path.join(root, folder, "drums_3.ogg"))
                    drums2 = AudioSegment.from_file(os.path.join(root, folder, "drums_2.ogg"))
                    drums1 = AudioSegment.from_file(os.path.join(root, folder, "drums_1.ogg"))
                elif path.exists(os.path.join(root, folder, "drums_3.ogg")):
                    drumber = 3
                    drums3 = AudioSegment.from_file(os.path.join(root, folder, "drums_3.ogg"))
                    drums2 = AudioSegment.from_file(os.path.join(root, folder, "drums_2.ogg"))
                    drums1 = AudioSegment.from_file(os.path.join(root, folder, "drums_1.ogg"))
                elif path.exists(os.path.join(root, folder, "drums_2.ogg")):
                    drumber = 2
                    drums2 = AudioSegment.from_file(os.path.join(root, folder, "drums_2.ogg"))
                    drums1 = AudioSegment.from_file(os.path.join(root, folder, "drums_1.ogg"))
                elif path.exists(os.path.join(root, folder, "drums.ogg")):
                    drumber = 1
                    drums = AudioSegment.from_file(os.path.join(root, folder, "drums.ogg"))
                print(f"Drumber = {drumber}")
            tracks = "("
            tracks = insert_overlay(tracks, "song")
            if isRhythm and wantBass:
                tracks = insert_overlay(tracks, "rhythm.overlay(")
            if isGuitar and wantGuitar:
                tracks = insert_overlay(tracks, "guitar.overlay(")
            if isVocals and wantVocals:
                tracks = insert_overlay(tracks, "vocals.overlay(")
            if isKeys and wantKeys:
                tracks = insert_overlay(tracks, "keys.overlay(")
            if isDrums and wantDrums:
                if drumber == 4:
                    tracks = insert_overlay(tracks, "drums4.overlay(")
                    tracks = insert_overlay(tracks, "drums3.overlay(")
                    tracks = insert_overlay(tracks, "drums2.overlay(")
                    tracks = insert_overlay(tracks, "drums1.overlay(")
                elif drumber == 3:
                    tracks = insert_overlay(tracks, "drums3.overlay(")
                    tracks = insert_overlay(tracks, "drums2.overlay(")
                    tracks = insert_overlay(tracks, "drums1.overlay(")
                elif drumber == 2:
                    tracks = insert_overlay(tracks, "drums2.overlay(")
                    tracks = insert_overlay(tracks, "drums1.overlay(")
                elif drumber == 1:
                    tracks = insert_overlay(tracks, "drums.overlay(")
            print(tracks)

            combined = None
            exec("combined = " + tracks)
            print(combined)
            # os.makedirs(f"PracOutput/{icon}", exist_ok=True)  # make folders with sources
            # filename = f"PracOutput/{icon}/{name} - {artist} - {insts}"
            # os.makedirs(f"PracOutput/{artist}", exist_ok=True)  # make folders with artists
            # filename = f"PracOutput/{artist}/{name} - {artist} - {insts}"
            os.makedirs(f"PracOutput/{artist}", exist_ok=True)  # make folders with sources/artists
            filename = f"PracOutput/{artist}/{name} - {artist} - {insts} - {icon}"
            combined.export(f"{filename}.mp3", format="mp3", bitrate="320k", tags={f'artist': artist, 'name': name, 'source': icon, 'type': insts})
            x += 1
            print(f"Completed {x} Songs!")

        else:
            print(f"{files} is not a song folder")
