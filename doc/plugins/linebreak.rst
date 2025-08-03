Filter Step: `linebreak`
========================

This step helps to adjust line breaks.

- **type: linebreak**

**Parameters:**

These parameters control how to concatinate shapes and lines.

:``shape_delimiter`` (string, optional): Delimiter when concatinating shapes. Default is ``\n``.
:``line_delimiter`` (string, optional): Delimiter when concatinating lines in a shape. Default is ``\n``.
:``strip`` (boolean, optional): Before concatinating lines, strip leading and trailing spaces from each line. Default is true.

For example, if you want to get multiple lines into one, set ``line_delimiter`` to ``' '`` (just a space).

These parameters control splitting a line and joining lines.
Ideal target languages are CJK (Chinese, Japanese, and Korean).

:``split_long_line`` (integer, optional): Threshold number when splitting a long line. Default is ``0``, do not split.
:``split_nowrap`` (string, optional): Characters that the split should not happen just before them. Set punctuations in your language. Default is ``.,"'``.
:``split_nowrap_allow_overflow`` (boolean, optional): When a character in ``split_nowrap`` is overflowing, the option controls the overflow is allowed or not. Default is true.
:``joined_column_max`` (integer, optional): Threshold number when joining short lines. Default is ``0``, do not join.
:``join_by`` (string, optional): Delimiter when joining short lines. Default is a space ``' '``.

These parameters controls calculation of character widths.

:``ambiguous_char_width`` (int, optional): Width for Unicode ambiguous characters. Default is ``1``.
:``custom_width.*`` (int, optional): Width for the specified character.

.. versionadded:: 0.3 The parameter ``ambiguous_char_width`` and ``custom_width``.

**Order of process:**

The texts are processed in the order described below.

1. Split long lines.
2. Join short lines.
3. Concatinate lines in each shape.
4. Concatinate shapes.

**YAML Example:**

.. code-block:: yaml

   steps:
     - type: ppt

     # Adjust line breaks
     - type: linebreak
       shape_delimiter: '\n'
       line_delimiter: ' '
       strip: true

     # This step prints the result
     - type: stdout

..
  TODO Add more examples.
