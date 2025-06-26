Output Step: `webserver`
====================

This step hosts a web server so that your browser can view the text.
The text will be updated in realtime.

- **type: webserver**

**Parameters:**

:host (string, optional): The listening host. The default is ``localhost``. Set ``0.0.0.0`` if you want to view from another computer.
:port (integer, optional): The listening port. The default is ``8080``.
:index_html (string, optional): Overwrite the HTML contents.
:script_js (string, optional): Overwrite the JavaScript contents.
:style_css (string, optional): Overwrite the style sheet contents.

**YAML Example:**

.. code-block:: yaml

   steps:
     - type: ppt

     # This step sends the text to the 'Live Text' source in OBS.
     - type: webserver
       host: 0.0.0.0
       port: 8080
       style_css: |
         body {
           font-family: sans-serif;
           font-size: 32pt;
         }

Then, open your browser and navigate to ``http://127.0.0.1/`` (or your computer's IP address).

.. note::
   * If you open the page from vMix, the background should be transparent. See `vMix User Guide`_ for details.

.. _vMix User Guide: https://www.vmix.com/help28/WebBrowser.html
