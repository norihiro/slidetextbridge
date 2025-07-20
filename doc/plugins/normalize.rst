Filter Step: `normalize`
========================

This step normalizes Unicode text by `unicodedata.normalize`_.

.. _unicodedata.normalize: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize

- **type: normalize**

**Parameters:**

:``form`` (str, optional): Set the form. Available choices are ``NFC``, ``NFKC``, ``NFD``, and ``NFKD``. Default is ``NFKC``.

**Description:**

In Japanese,
there are various kana representations such as half-width and full-width, composition and decomposition for voiced and semi-voiced marks.

.. list-table:: Japanese normalization
   :header-rows: 1

   * -
     - ``NFC``
     - ``NFD``
     - ``NFKC``
     - ``NFKD``
   * - Full-width voiced and semi-voiced kana
     - Composition
     - Decomposition
     - Composition
     - Decomposition
   * - Full-width Kana
     - Full-width
     - Full-width
     - Full-width
     - Full-width
   * - Half-width Katakana
     - Half-width
     - Half-width
     - Full-width
     - Full-width
   * - Half-width digits and latin letters
     - Half-width
     - Half-width
     - Half-width
     - Half-width
   * - Full-width digits and latin letters
     - Full-width
     - Full-width
     - Half-width
     - Half-width


**YAML Example:**

.. code-block:: yaml

   steps:
     - type: ppt

     - type: normalize

     - type: print
