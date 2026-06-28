# Download CC0 puppy vocal samples + variant pools for Demo. See assets/dog/sfx/CREDITS.md
$ErrorActionPreference = 'Stop'
$demo = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $demo
$sfx = Join-Path $root 'assets\dog\sfx'
New-Item -ItemType Directory -Force -Path $sfx | Out-Null

$previews = @{
  '_chihuahua.mp3' = 'https://cdn.freesound.org/previews/350/350593_6433555-hq.mp3'
  '_puppy8.mp3'    = 'https://cdn.freesound.org/previews/728/728029_24119-hq.mp3'
}

foreach ($name in $previews.Keys) {
  Write-Host "Downloading $name ..."
  Invoke-WebRequest -Uri $previews[$name] -OutFile (Join-Path $sfx $name) -TimeoutSec 60
}

$babyZip = Join-Path $env:TEMP 'baby-animals.zip'
$babyDir = Join-Path $env:TEMP 'baby-animals'
if (-not (Test-Path (Join-Path $babyDir 'Bark.ogg'))) {
  Invoke-WebRequest -Uri 'https://opengameart.org/sites/default/files/baby-animals.zip' -OutFile $babyZip -TimeoutSec 90
  Expand-Archive -Force -Path $babyZip -DestinationPath $babyDir
}
Copy-Item (Join-Path $babyDir 'Bark.ogg') (Join-Path $sfx 'puppy-yip.ogg') -Force
Copy-Item (Join-Path $babyDir 'Bark.ogg') (Join-Path $sfx '_bark.ogg') -Force

$py = @'
import librosa, soundfile as sf, numpy as np, os, glob

sfx = os.environ['DOG_SFX']

def to_mono(y):
    return librosa.to_mono(y) if getattr(y, 'ndim', 1) > 1 else y

def norm(y, peak=0.92):
    y = to_mono(y)
    m = np.max(np.abs(y)) or 1
    return y / m * peak

def extract_peak(y, sr, max_dur=1.0, offset_sec=0.0, frame_sec=0.25):
    y = to_mono(y)
    if offset_sec > 0:
        y = y[int(sr * offset_sec):]
    frame = int(sr * frame_sec)
    best_i, best_e = 0, 0
    step = max(1, frame // 4)
    for i in range(0, max(1, len(y) - frame), step):
        e = np.sum(y[i:i + frame] ** 2)
        if e > best_e:
            best_e, best_i = e, i
    start = max(0, best_i - int(sr * 0.05))
    end = min(len(y), start + int(sr * max_dur))
    return y[start:end]

def fade(y, sr, attack=0.02, release=0.06):
    n = len(y)
    a = min(n // 4, int(sr * attack))
    r = min(n // 4, int(sr * release))
    out = y.copy()
    if a > 0:
        out[:a] *= np.linspace(0, 1, a)
    if r > 0:
        out[-r:] *= np.linspace(1, 0, r)
    return out

def write_wav(name, y, sr, peak=0.88):
    sf.write(os.path.join(sfx, name), norm(fade(y, sr), peak), sr, subtype='PCM_16')

chi, sr = librosa.load(os.path.join(sfx, '_chihuahua.mp3'), sr=44100, mono=True)
p8, sr2 = librosa.load(os.path.join(sfx, '_puppy8.mp3'), sr=44100, mono=True)
yip_path = os.path.join(sfx, 'puppy-yip.ogg')
yip, sr3 = librosa.load(yip_path, sr=44100, mono=True)

wh_a = extract_peak(chi, sr, 1.05, 0.0)
wh_b = extract_peak(chi, sr, 0.85, 0.35)
write_wav('puppy-whimper-a.wav', wh_a, sr, 0.90)
write_wav('puppy-whimper-b.wav', wh_b, sr, 0.84)
write_wav('puppy-whimper.wav', wh_a, sr, 0.90)

soft_a = extract_peak(p8, sr2, 0.95, 0.0)
soft_b = extract_peak(p8, sr2, 0.75, 0.55)
write_wav('puppy-soft-a.wav', soft_a, sr2, 0.76)
write_wav('puppy-soft-b.wav', soft_b, sr2, 0.70)
write_wav('puppy-soft-whimper.wav', soft_a, sr2, 0.76)

sigh_a = extract_peak(p8, sr2, 0.55, 0.15) * 0.85
sigh_b = extract_peak(p8, sr2, 0.45, 0.85) * 0.80
write_wav('puppy-sigh-a.wav', sigh_a, sr2, 0.68)
write_wav('puppy-sigh-b.wav', sigh_b, sr2, 0.62)

yip_a = extract_peak(yip, sr3, 0.35, 0.0)
yip_b = extract_peak(yip, sr3, 0.28, 0.12)
write_wav('puppy-yip-b.wav', yip_b, sr3, 0.82)
import shutil
shutil.copy2(yip_path, os.path.join(sfx, 'puppy-yip-a.ogg'))

bark_path = os.path.join(sfx, '_bark.ogg')
bark, sr4 = librosa.load(bark_path, sr=44100, mono=True)
write_wav('puppy-bark-a.wav', extract_peak(bark, sr4, 0.38, 0.0), sr4, 0.86)
write_wav('puppy-bark-b.wav', extract_peak(bark, sr4, 0.32, 0.10), sr4, 0.80)
write_wav('puppy-excited-a.wav', extract_peak(bark, sr4, 0.26, 0.0), sr4, 0.90)
write_wav('puppy-excited-b.wav', extract_peak(bark, sr4, 0.22, 0.14), sr4, 0.86)

mur_a = extract_peak(p8, sr2, 1.15, 0.05) * 0.72
mur_b = extract_peak(chi, sr, 1.25, 0.25) * 0.68
write_wav('puppy-murmur-a.wav', mur_a, sr2, 0.52)
write_wav('puppy-murmur-b.wav', mur_b, sr, 0.48)

for p in glob.glob(os.path.join(sfx, '_*.mp3')) + [bark_path]:
    if os.path.isfile(p):
        os.remove(p)
print('puppy sample pools ready')
'@

$env:DOG_SFX = $sfx
python -c $py
Write-Host 'Done. See assets/dog/sfx/CREDITS.md'
