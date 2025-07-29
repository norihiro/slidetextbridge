Getting Started
===============

This section covers the basic steps to get ``slidetextbridge`` running.

Installation
------------

Download a pre-built package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is recommended for Windows users.

If you are on Windows,
the easiest way to get started is to download the latest ZIP file.

1. Download the ``slidetextbridge-X.Y.Z-windows.zip`` file from the `release page`_.
2. Extract the contents of the ZIP file.
3. Edit the configuration file ``config.yaml`` in the folder.
4. That's it! You can run ``slidetextbridge.exe`` from this folder.

.. _release page: https://github.com/norihiro/slidetextbridge/releases

Download from PyPI (Other Platforms)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may install from PyPI.

.. code-block:: bash

   # It is recommended to use a virtual environment
   # For Linux, add `--system-site-packages` to use uno module from LibreOffice.
   python -m venv --system-site-packages venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   # Install this tool
   pip install slidetextbridge

Configuration File
------------------

``slidetextbridge`` uses a YAML file (e.g., ``config.yaml``) to define a pipeline of steps.
Each step in the pipeline processes text in some way,
either by reading it from a source, transforming it, or sending it to a destination.

Here is a basic configuration to get you started.
This setup reads text from the placeholder shapes of the current slide in PowerPoint and sends it to a text source in OBS Studio.

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

     # # Step 3: Optionaly, you may use web server for vMix, etc.
     # - type: webserver
     #   host: 0.0.0.0                   # Host address the server will listen on. 0.0.0.0 for all.
     #   port: 8080                      # Host port the server will listen on.


Running the Program
-------------------

Downloaded the pre-built package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  If you have downloaded the ZIP file from the release page,

  1. Ensure ``config.yaml`` is located at the same directory of ``slidetextbridge.exe``.
  2. Double-click ``slidetextbridge.exe``.
  3. That's it, a console window will appear.

Downloaded from PyPI
^^^^^^^^^^^^^^^^^^^^

  If you have installed using ``pip``,

  .. code-block:: bash

     slidetextbridge -c config.yaml

Now, when you change slides in PowerPoint, the text from the new slide's should appear in the specified OBS text source or in your browser,
depending on your configuration.
