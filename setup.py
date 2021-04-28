import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

include_files = ["bns.jpg",
                 "cannon.png",
                 "d_fire.png",
                 "d_shooter.wav",
                 "dragon.png",
                 "dragon3.png",
                 "energy.png",
                 "favicon.ico",
                 "fbg.png",
                 "fire.png",
                 "fireball.png",
                 "h_score.txt",
                 "help_player.wav",
                 "hitvillain.wav",
                 "info.wav",
                 "level.txt",
                 "play.wav",
                 "tree.png",
                 "v_shooter.wav",
                 "villain.png",
                 "welcome.wav",
                 "You_Win.wav",
                 "youlose.wav"

                 ]

executables = [cx_Freeze.Executable("main.py",
                                    icon="favicon.ico",
                                    base=base,

                                    )]

cx_Freeze.setup(
    name="Dragon Fire",
    options={"build_exe": {"packages": ["pygame"], "include_files": include_files}},
    version="1.0",
    description="2D game for Desktop.",
    executables=executables

)
