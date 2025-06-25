Output Step: `obsws`
====================

This step sends the received text to an OBS Studio text source using the ``obs-websocket`` plugin.

Make sure OBS Studio version 28.0.0 or later so that obs-websocket is pre-installed.

- **type: obsws**

**Parameters:**

:url (string, required): The WebSocket URL for your OBS instance. The default is typically ``ws://localhost:4455/``.
:password (string, optional): The password you have set in your OBS WebSocket Server Settings. If you have not set a password, you can leave this blank or omit it.
:source_name (string, required): The exact name of the Text source in OBS that you want to update. For example, ``Text (GDI+)``, ``Live Subtitles``, etc.

**YAML Example:**

.. code-block:: yaml

   steps:
     - type: ppt

     # This step sends the text to the 'Live Text' source in OBS.
     - type: obsws
       url: 'ws://localhost:4555/'
       password: 'your_secret_password'
       source_name: 'Text (GDI+)'
