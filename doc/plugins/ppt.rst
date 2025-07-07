Input Step: `ppt`
=================

This step reads text from a Microsoft PowerPoint presentation.
It is designed to be an input source, meaning it's usually the first step in the pipeline.

- **type: ppt**

**Parameters:**

:``placeholder_only`` (boolean, optional): Select only placeholder shapes. True by default.
:``poll_wait_time`` (float, optional): Set the wait time for each polling in seconds. 0.1 seconds by default.

What is placeholder?
  Placeholders mean the shapes that comes from the slide master,
  or the shapes existing when a new slide page is created.
  It is recommended to put every text on the placeholders.

  However, if you want to get all other texts, set ``placeholder_only`` to ``false``.
  By this, all shapes will be processed.

**YAML Example:**

.. code-block:: yaml

   steps:
     # This step reads from PowerPoint. The text is then passed to the next step.
     - type: ppt
       placeholder_only: true
       poll_wait_time: 0.1
