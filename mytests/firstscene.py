from ambiscaper import *
import numpy as np
import os

# AmbiScaper settings
soundscape_duration = 5.0
ambisonics_order = 1
foreground_folder = os.path.abspath('./samples/Acoustics_Book')

### Create an ambiscaper instance
ambiscaper = AmbiScaper(duration=soundscape_duration,
                        ambisonics_order=ambisonics_order,
                        fg_path=foreground_folder)
### Add an event
ambiscaper.add_event(source_file=('choose', ['adult_female_speech.flac','bagpipe_music.flac']),
                     source_time=('const', 0),
                     event_time=('const', 0),
                     event_duration=('const', soundscape_duration),
                     event_azimuth=('uniform', 0, 2*np.pi),
                     event_elevation=('uniform', -np.pi/2, np.pi/2),
                     event_spread=('const', 0),
                     snr=('const', 0),
                     pitch_shift=('const', 1),
                     time_stretch=('const', 1)
                     )
### Genereate the audio and the annotation
outfolder = '/home/olanf/ambiscaper/output'
 # watch out! outfolder must exist
destination_path = os.path.join(outfolder,"my_first_ambisonics_soundscape")

ambiscaper.generate(destination_path=destination_path,
                    generate_txt=True)
