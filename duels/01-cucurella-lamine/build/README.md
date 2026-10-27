# Fabrication

Aperçu (voix témoin Kokoro) :
    python3 tts.py segments.json wav && python3 timeline_tts.py
    node render.js sfx && python3 ../../../histoires-insolites/core/audio.py timeline.json sfx.json mix.wav voix.wav 0
    OUT=../cucurella-lamine-apercu.mp4 node render.js full

Version finale (voix ElevenLabs posée dans ../voix-elevenlabs.mp3) :
    ffmpeg -y -i ../voix-elevenlabs.mp3 -ar 44100 -ac 1 voix.wav
    ffmpeg -i voix.wav -af silencedetect=n=-35dB:d=0.25 -f null - 2>&1 | grep -oE 'silence_(start|end): [0-9.]+' > sil.txt
    python3 sync.py
    node render.js sfx && python3 ../../../histoires-insolites/core/audio.py timeline.json sfx.json mix.wav voix.wav 0.4
    OUT=../cucurella-lamine.mp4 node render.js full

Images de contrôle : node render.js stills 1 10 20
