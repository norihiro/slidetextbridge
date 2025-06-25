Getting Started
===============

This section covers the basic steps to get ``slidetextbridge`` running.

For Windows Users (Recommended)
-------------------------------

If you are on Windows,
the easiest way to get started is to download the latest ZIP file.
This does not require you to install Python or manage packages with pip.

1. Download the ``slidetextbridge-X.Y.Z-windows.zip`` file from the project's `release page`_.
2. Extract the contents of the ZIP file to a folder on your computer.
3. Edit the configuration file ``config.yaml`` in the folder.
4. That's it! You can run the program directly from this folder.

.. _release page: https://github.com/norihiro/slidetextbridge/releases

From PyPI (Other Platforms)
---------------------------

You may install from PyPI.
(Though I have not released on PyPI yet, hopefully, it's available when you are reading this document.)

.. code-block:: bash

   # It is recommended to use a virtual environment
   # For Linux, add `--system-site-packages` to use uno module from LibreOffice.
   python -m venv --system-site-packages venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   # Install this tool
   pip install slidetextbridge

From Source (For Developers)
----------------------------

If you want to install from source, modify the code, you can download the source code from GitHub.

.. code-block:: bash

   # Clone from GitHub
   git clone https://github.com/norihiro/slidetextbridge.git
   cd slidetextbridge

   # It is recommended to use a virtual environment
   python -m venv --system-site-packages venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   # Install this tool
   pip install -e .


Configuration
-------------

``slidetextbridge`` uses a YAML file (e.g., ``config.yaml``) to define a pipeline of steps.
Each step in the pipeline processes text in some way,
either by reading it from a source, transforming it, or sending it to a destination.

Here is a basic configuration to get you started.
This setup reads text from the notes section of the current slide in PowerPoint and sends it to a text source in OBS Studio.

**config.yaml:**

.. code-block:: yaml

   # Configuration file for slidetextbridge

   # The 'steps' key defines a sequence of operations.
   # The text output from one step becomes the input for the next.
   steps:
     # Step 1: Retrieves text from the notes of the active slide in Microsoft PowerPoint.
     - type: ppt

     # Step 2: Prints the retrieved text to the console. This is useful for troubleshooting.
     - type: stdout

     # Step 3: Sends the text to a specific source in OBS Studio via the WebSocket plugin.
     - type: obsws
       url: 'ws://localhost:4455/'     # URL of the OBS WebSocket server.
       password: 'your_password_here'  # Password for the OBS WebSocket server (leave blank if none).
       source_name: 'Live Text'        # The name of the Text (GDI+) or (Freetype 2) source in OBS Studio.


Running the Program
-------------------

Once your ``config.yaml`` is ready, you can run the program. The command will differ based on your installation method.

Donwloadede from the release page

  If you have downloaded the ZIP file from the release page,
  1. Ensure ``config.yaml`` is located at the same directory of ``slidetextbridge.exe``.
  2. Double-click ``slidetextbridge.exe``.
  3. That's it, a console window will appear.

.. code-block:: bash

   # If running from source
   slidetextbridge -c config.yaml

Now, when you change slides in PowerPoint, the text from the new slide's should appear in the specified OBS text source.
