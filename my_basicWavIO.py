import pyaudio
import wave
import sys
import os

"""
Written by BxDx92 / Durzo, 2018
    -Basic IO functions for WAV Files
        -playSelection plays a section from start for start+length 
        -cut selection writes a new wav file from start to start+length
"""


def playSelection(filename,startInSec = 7, lengthInSec = 4):
    '''Plays a .WAV File from startInSec for lengthInSec'''
    if os.path.isfile(filename):
        # open wave file
        try:
            wave_stream = wave.open(filename, 'rb')
        except IOError:
            print "Could not read file:", filename

        # initialize audio
        py_audio = pyaudio.PyAudio()
        stream = py_audio.open(format=py_audio.get_format_from_width(wave_stream.getsampwidth()),
                               channels=wave_stream.getnchannels(),
                               rate=wave_stream.getframerate(),
                               output=True)

        # skip unwanted frames
        n_frames = int(startInSec * wave_stream.getframerate())
        wave_stream.setpos(n_frames)

        # write desired frames to audio buffer
        n_frames = int(lengthInSec * wave_stream.getframerate())
        frames = wave_stream.readframes(n_frames)
        stream.write(frames)

        # close and terminate everything properly
        wave_stream.close()
        stream.close()
        py_audio.terminate()
    else:
        raise IOError("Couldnt Find File: \"%s\"" % filename)

def cutSelection(filename, outFilename="", startInSec = 7, lengthInSec = 4):
    '''Cuts out a part of .WAV File from startInSec for lengthInSec,
    and saves it und outFilename.WAV'''
    if os.path.isfile(filename):
        # open wave file
        try:
            waveInStream = wave.open(filename, 'rb')
        except IOError:
            print "Could not read file:", filename

        # Default Output file
        if str(outFilename) == "":
            endInSec = startInSec + lengthInSec
            outFilename = filename + "_start_" + str(startInSec) + "_end_" + str(endInSec)
        elif str(outFilename)[-4:].upper() != ".WAV":
            outFilename = outFilename + ".wav"

        # initialize audio
        py_audio = pyaudio.PyAudio()
        stream = py_audio.open(format=py_audio.get_format_from_width(waveInStream.getsampwidth()),
                               channels=waveInStream.getnchannels(),
                               rate=waveInStream.getframerate(),
                               output=True)

        # skip unwanted frames
        n_frames = int(startInSec * waveInStream.getframerate())
        waveInStream.setpos(n_frames)

        # write desired frames to audio buffer
        n_frames = int(lengthInSec * waveInStream.getframerate())
        frames = waveInStream.readframes(n_frames)
        # created Output File and write it
        waveOutStream = wave.open(outFilename, 'wb')
        waveOutStream.setnchannels(waveInStream.getnchannels())
        waveOutStream.setsampwidth(waveInStream.getsampwidth())
        waveOutStream.setframerate(waveInStream.getframerate())
        waveOutStream.writeframes(b''.join(frames))
        print outFilename
        print "File SHould be Created"
        # close and terminate everything properly
        waveInStream.close()
        waveOutStream.close()
        stream.close()
        py_audio.terminate()
    else:
        raise IOError("Couldnt Find File: \"%s\"" % filename)


if __name__ == "__main__":
    pass
    # playSelection('/home/durzo/Schreibtisch/Scripts/TestAudioFiles/tesst.txt')
    # cutSelection('/home/durzo/Schreibtisch/Scripts/TestAudioFiles/diarizationExample2.wav','/home/durzo/Schreibtisch/Scripts/TestAudioFiles/diarz_01.wav',0,2)
