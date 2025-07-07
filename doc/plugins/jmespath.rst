Filter Step: `jmespath`
=======================

This step filters shapes by attributes.
The filter engine is powered by JMESPath.

- **type: jmespath**

**Parameters:**

:``filter`` (string, required): Set the filter in JMESPath format

**YAML Example:**

.. code-block:: yaml

   steps:
     - type: ppt
       placeholder_only: false

     # This is useful to see the structure of the shape data
     - type: print
       json: true

     # This step selects texts whose size is 28 or bigger
     - type: jmespath
       filter: shapes[?text_frame.text_range.font.size>=`28`]

     - type: print
