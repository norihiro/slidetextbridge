Filter Step: `stdout`
=====================

This step just prints the text on console.

- **type: stdout**

**Parameters:**

:``json`` (boolean, optional): Print in JSON format. The default is false.
:``page_delimiter`` (string, optional): The delimiter between the slide pages. Default is ``\n\n`` (ie., one empty line).

**YAML Example:**

.. code-block:: yaml

   steps:
     - type: ppt

     # This step prints all shapes with their properties.
     - type: stdout
       page_delimiter: '\n\n'
       json: true
