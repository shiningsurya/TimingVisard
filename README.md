# TimingVisard
_To be read as Timing Wizard_

Who is a wizard? Not just someone who conjures up a spirit, but someone who can understand the effects of what infinitesimal change in parameters brings forth in residuals. And, by understand, I mean, someone who can visualize the change. _(hence the pun above)_

_The definition of wizard here is very bad. Haha._

## For installation,
check out the `INSTALL.md` file. 

You will also find the list of requirements and dependencies



## ResVisard

It is a GUI application which has residual plot in one side and in other side sliders for each of the parameters that can be fitted. 
You move the slider in any way, the GUI changes the value correspondingly in the `par file`. And, then, you hit `FIT` and **visualize** the structures that come in the residuals.


The pic that comes when you run ResVisard is album art of **Joy Division | Unknown Pleasures**. This is the [link](https://kottke.org/plus/misc/images/joy-division-unknown-pleasures.jpg). 

_Sidenote disclaimer: I haven't checked out the album yet. I put it because it is a pop-culture reference._

#### LOGIC

_ResVisard_ is supposed to be a tool to visualize the effect of random (hence those sliders) flucuations in the parameters. 
It is not made to be exact. Slider value tells us how away from the initial value is our current parameter value. Mathematically, 

$p_i = p_{i-1} + \lambda \cdot s \cdot \mu_{p,i-1}$

$p_i$ is parameter value at step $i$. $\lambda$ is a constant. $s$ is the slider value. $\mu_{p,i}$ is the uncertainity in $p_i$.

## PyLK
_Inspired by plk and has Python, hence_


`plk`-like plugin made completely in Python and along with bunch of added functionalities to easen the timing. 
