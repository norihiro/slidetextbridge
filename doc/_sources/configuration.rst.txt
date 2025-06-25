Configuration File Reference
============================

The configuration file is a YAML document that defines the ``steps`` of the text-processing pipeline.

Top-Level Structure
-------------------

The root of the configuration must be a ``steps`` key, which holds a list of step objects.

.. code-block:: yaml

   steps:
     - ... # Step 1
     - ... # Step 2
     - ... # and so on

Step Types
----------

Each step is an object with a ``type`` key.
Additional keys may be required depending on the type.

See :doc:`plugins/index` for the complete list of available types.
