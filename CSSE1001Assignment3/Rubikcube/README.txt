BBCUBER'S CUBE
Copyright (c) 2008, Josh Hicks
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 
Neither the name of Josh Hicks nor the names of his contributors may be used to endorse or promote products derived from this software without specific prior written permission. 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

==============================================================
HOW TO INSTALL
==============================================================

To run unzip all the python documents, the piecemeth folder,
the replays folder,t1 and the icon to the same folder. Then
run the controller file. The rest should compile from there.

You should also have python 2.5.2 downloaded to run this
prorgram. If you don't have it you can download it from
http://www.python.org/download/.
	
No non-standard libraries are needed.

This program was deveolped under windows xp

I have usually run this program through IDLE, so I
know that it works there.

The program does not require a particular directory to run
The program does not require certain parameters to run


==============================================================
FILES IN FOLDER
==============================================================
Controller.py	main file
highscore.py	
Model.py	
ModelPointer.p	
piecesolve.py	
Visual.py	
Visualreplay.py
icon.ico
t1.txt
piecemeth/
 includes step1-18
replays/
 includes some of highrec0-9
Design Document.pdf
Reflections.pdf

==============================================================
SUMMARY
==============================================================
BBCUBER'S CUBE is a rubik's cube simulator and solver program.
By using the keyboard, users can solve a virtual cube. Replays
and highscores are stored when the program is quit. The
program will also solve a scrambled cube. Cubes cannot be
entered except indirectly though .txt files.

==============================================================
PLAYING THE GAME
==============================================================
If you are new to this program, I recommend opening the controls,
and having them on the right hand screen until you learn them. You
can open these from help>help on the menu. Then scramble the cube
and go. If it doesn't work, check that Caps Lock is off. Also, there
should be a black border around the cube on the left. if not press
tab. You can also change the control options from the menu. As these
are fairly different I suggest that you try them all and see which
suits you best. And even if jump gets you better times, its still
not as cool.

However, if you are new to the rubik's cube. Then I strongly suggest
that you look up some of the links under the Help menu. Personally,
I suggest the Lars Petrus site, and secondly the Heise before you
begin to learn algorithms at Fredrich although most people go
directly to learning a few algorithms without real understanding.

If the see through cube is a little hard for you to think about at
the moment, then go to the name entry box in the bottom left. Type
100000 or some other suitiably large number and hit ctrl-z. While
you're here if you haven't typed in you name yet you may as well.
Finishing that click enter to return you to your not so see through
cube.

You can also edit the visual options with the colour menu. It's
fairly self explanitory. The only one that isn't is the solve menu
and to my shame only the piece solve actually works. However, it's
fairly interesting. So once you're solving away and just give up
you can click on Solve from the Solve menu. This will open up a
window on the right. Left and Right will move backwards and
forwards through the solve. To get back just click tab until the 
black border once again appears.

Once you do manage to solve the cube, you'll notice that your
highscore will have been updated (if in top 10, sorry for those
who didn't make it). If you click on it the window on the right
will load up a replay. Just click play to see you go. The only
bug (intentionally i must admit) is that if you completed it off
a saved file only the moves done after you opened it will show up.
This means you could have a very very boring 5 mins if you reopened
your file then.
