Filter Step: `regex`
====================

This step filters lines.

- **type: regex**

**Parameters:**

:patterns (list, required): Set the patterns to search and replace.
:patterns[*].p (str, required): The pattern to search.
:patterns[*].r (str, required): The text to be replaced with.

..
  TODO Describe more about substitution parameter, the pattern is searched line-by-line, etc.

**YAML Example:**

.. code-block:: yaml

   steps:
     - type: ppt
       placeholder_only: false

     - type: regex
       patterns:
	     - p: '\<This\>'
	       r: That
	     - p: '\<Those\>'
	       r: These

     - type: print
