# Media guide

Use only our own media. Label CAD as "render". No stock photos, no other companies' vehicles, no AI-generated images presented as our hardware.

| Kind | Format | Limit |
|---|---|---|
| Hero loop | WebM (VP9) and MP4 (H.264), muted, 5 to 10 s, 1280 px wide | 10 MB, with `media/hero-still.jpg` fallback |
| Longer footage | Upload to YouTube or Vimeo and embed | None in repo |
| Photos | JPEG or WebP, 2400 px wide at most | 500 KB each where possible |
| Plots and diagrams | SVG preferred, otherwise PNG | 300 KB |
| Portraits | Square JPEG, 400 to 800 px | 300 KB |

Every image needs alt text (what it shows) and a caption when it carries information. No file over 50 MB, ever: `scripts/check_site.py` fails the build.

Compress video: `ffmpeg -i in.mp4 -an -vf scale=1280:-2 -c:v libx264 -crf 28 -movflags +faststart hero.mp4`

The current shot list is kept by the lab leads.
