import soundfile as sf
import numpy as np
import os
import sys
import glob

REPO = os.path.expanduser('~/ambiscaper')
OUTPUT = os.path.join(REPO, 'output')

# Work out which scene folder to use
if len(sys.argv) > 1:
    scene_dir = sys.argv[1]
    if scene_dir.endswith('.wav'):          # also accept the .wav itself
        scene_dir = os.path.dirname(scene_dir)
else:
    # No argument: use the most recently generated scene
    folders = [f for f in glob.glob(os.path.join(OUTPUT, '*')) if os.path.isdir(f)]
    if not folders:
        sys.exit('No scene folders found in ' + OUTPUT)
    scene_dir = max(folders, key=os.path.getmtime)

scene_dir = os.path.abspath(scene_dir)
name = os.path.basename(scene_dir)
in_path = os.path.join(scene_dir, name + '.wav')
out_path = os.path.join(scene_dir, name + '_stereo.wav')

if not os.path.exists(in_path):
    sys.exit('Could not find ' + in_path)

# Read the Ambisonics file and make a left/right stereo preview
x, fs = sf.read(in_path)
print('scene:', name, '| channels:', x.shape[1], '| sample rate:', fs)

W, Y = x[:, 0], x[:, 1]            # ACN order: W, Y, Z, X
left  = 0.5 * (W + Y)              # virtual cardioid pointing left
right = 0.5 * (W - Y)              # virtual cardioid pointing right
stereo = np.stack([left, right], axis=1)
stereo /= max(1e-9, np.max(np.abs(stereo))) / 0.9   # normalise

sf.write(out_path, stereo, fs)
print('wrote', out_path)