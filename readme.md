# WitchFire
A Halloween enhanced version of the SkyFire shooter game, which was written and presented by Phil Gilmore at Utah Kids Code Camp 2017 (github.com/nunug/kcc_2017).

## How to Run
_Note! 
The program is not tested on Mac or Linux.  You may need to change file path references to use different slashes._

You will need Python installed. I believe it was originally written for Python 2.7, but these new enhancements were made in Python 3.10.  Open a command prompt.  Navigate to the root directory where you cloned or downloaded the WitchFire repository.  Issue these commands to start the game.

On Windows (CMD or PowerShell):
```
cd source
python .\witchfire.py
```

On Mac (Terminal):
```
cd source
python3 ./witchfire.py
```

On Linux, Ubuntu, Raspberry Pi:
```
cd source
python ./witchfire.py
```


Press `ESC` at any time to quit the game.  You can also click the [X] on the toolbar at the top of the window.

The game engine renders to a 640 x 480 screen which fits on kids' crappy uncle's laptops when they come to see us at KCC events.  But it's a little hard to see.  For developers with nice hardware, I have added a double-buffer where the rendering buffer will be scaled up to a larger window before flipping.  That way you can specify the resolution without having to modify all the aspects of the code that deal with coordinates and sizes and scales.

To set the size of the game's display window, edit these settings in `witchfire.py`:

```
screen_width = 1920
screen_height = 1080
```

## How to Play
Tina Templeton's intern has fumbled her Jolly Jack-o-Lantern enchantment and accidentally brought the entire pumpkin patch to life.  It is up to Tina to put them down.  Blow up the Jolly Jack-o-Lanterns before they knock you out of the sky.

Fly your witchy using the `up` and `down` arrow keys (either the navigation keys or the numeric keypad with the NumLock off, which is how proper computer users do it).  Fire at the Jolly Jack-o-Lanterns with the `space bar`.

You start with 3 lives.  After killing enough Jolly Jack-o-Lanterns, you will earn an extra life.  This achievement is indicated by a buh-ding sound.  Every time you are touched by a Jolly Jack-o-Lantern, you lose a life.  When (not if) you lose all your lives, the game is over.

As you destroy the Jolly Jack-o-Lanterns, they will haunt you more aggressively.  They will start to sway confrontationally and will speed up as they charge you.  They will also increase in number.   There is no end to the game, so I'm afraid tonight is the night you will die.  

## How to Cheat
The game has a good balance of challenge and fairness.  You can play for a while but you will die.  No amount of skill can keep you alive forever.  Hower, the Konami code can.  If you fancy this cheat, the witch can cast the spell to imbue herself with 30 extra lives using this incantation:

`up`
`up`
`down`
`down`
`left`
`right`
`left`
`right`
`space bar`

You will know that the spell is cast when your lives increase by 30 and you hear the delightful Konami chime.
