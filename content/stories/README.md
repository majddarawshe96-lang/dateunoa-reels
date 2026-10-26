Story reels, planned and ready to render with the dateunoa-story-reel skill.
Each folder: episode.md (logline, cast, shot prompts, DM reply, captions), episode.json (build spec), shots/ (put the generated shots here as s1.mp4, s2.mp4, ...).
Build: python3 <skill>/scripts/build_episode.py episode.json --sheet sheet.png
Finished reels go to reels/stories/epNN.mp4.
