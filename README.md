# Duck-Jump-3 

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Sigmanificient/Duck-Jump-2.0/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Sigmanificient/Duck-Jump-2.0/?branch=master)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Sigmanificient/duck-jump-2.0)
![GitHub repo size](https://img.shields.io/github/repo-size/Sigmanificient/duck-jump-2.0)
![Lines of code](https://img.shields.io/tokei/lines/github/Sigmanificient/duck-jump-2.0)
![GitHub last commit](https://img.shields.io/github/last-commit/Sigmanificient/duck-jump-2.0)

## A rewrite
Duck Jump is a game originally thought by a group of 4 persons.
The Game contains collisions issue, as most of the code uses the same mechanics
from the lost original one.


| :exclamation: | The Duck Jump 2.exe is generated with PyInstaller. |
| ------------- | :------------------------------------------------- |

*Since the executable isn't signed, your antivirus can delete the executable.*
Feel free to check yourself the source code whether your not confidant or a curious guy.

However, if you still can't trust the executable, you will have to install python to run the .py file.

```bash
python -m pip install requirements.txt
python -m main.py
```


## More Informations

***Why the game run 90-100fps ?***

> This is due of two main raisons :
> - First, making a game that run same speed in any fps condition under pygame is way harder.
So we decide to limit the fps to something easily reachable by a lot of computer today.
> 
> With a fixed fps, the game should run about always the same speed.
> - Moreover, having the maximal amount of fps is not the most useful thing since it will ask more processor resources,
and most monitors does have an 60Hz refresh rate limit.
  
***Pydroid compatible ?***
> **No**, unfortunately, there is function that make the pygame program 
incompatible with pydroid.
> Even it's would be, you'll need a very powerful phone to run it well.

***"Failed to execute script" strange message showing up ?***
> This message can be if the executable is not compatible with your computer.
> 
> It have been made for windows 10 and could failed on windows 7 or 8.
