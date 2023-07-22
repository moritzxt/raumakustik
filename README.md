# Raumakustik App

This streamlit application delivers an estimation of the reverberation time in octave bands and an evaluation of the speech intelligibility for a room given by user inputs.

Users can enter the volume of the room and areas of surfaces and subsurfaces. Materials for these surfaces can be choosen from a database. Custom materials can be added to that database. Additionally a number of persons can be added to the rooms equivalent absorption surface. Speech intelligibilty can be evaluated for different use cases like ‘music’ or ‘education/communication’ as described in DIN 18041.

The calculations are based on statistical acoustics and implement the standards DIN EN 12354-6 and DIN 18041.

[[_TOC_]]

## Documentation & User Guide
A Documentation generated with [Sphinx](https://www.sphinx-doc.org/) can be found [here](https://mcht67.github.io/raumakustik2ndUpload/index.html). 
For details on usage and implementation of the norms view the [User Guide](pages/user_guide.pdf).

## Setup
Use git to clone this repository into your computer.
```
git clone https://github.com/moritzxt/raumakustik
```

Setup of the virtual environment:

```
python3 -m venv venv
source venv/bin/activate        # Activation for Linux / MacOS
venv\Scripts\Activate.ps1       # Activation for Windows (PowerShell)
venv\Scripts\Activate.bat       # Activation for Windows (CommandLine)
pip install -r requirements.txt
```

## Run Application
Open a console and navigate to the raumakustik directory:
```
streamlit run Nachhallzeitenanalyse.py
```

For more information see the [Documentation](https://moritzxt.github.io/raumakustik/index.html)
and the [User Guide](pages/user_guide.pdf).
