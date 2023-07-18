.. image:: _images/vergleichMitSoll.jpg
   :width: 400
   :align: right


Raumakustik App
===============

This streamlit application delivers an estimation of the reverberation time in octave bands and an evaluation of the speech intelligibility for a room given by user inputs.

Users can enter the volume of the room and areas of surfaces and subsurfaces. Materials for these surfaces can be choosen from a database. Custom materials can be added to that database. 
Additionally a number of persons can be added to the rooms equivalent absorption surface. Speech intelligibilty can be evaluated for different use cases like 'music' or 'education/communication' as described in DIN 18041. 

The calculations are based on statistical acoustics and calculation are based on the standards DIN EN 12354-6 and DIN 18041.

Content
========

.. toctree::
   :maxdepth: 1
   :caption: Main

   self

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   setup
   usage

.. toctree::
   :maxdepth: 4
   :caption: Module

   room_calc
   utils
   session_utils
   pdf_protocol
   Datenbank
   

.. toctree::
   :maxdepth: 1
   :caption: User Guide (German)
   
   user_guide
   
