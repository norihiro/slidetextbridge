Input Step: `openlp`
====================

This step reads text from `OpenLP`_ an open source church presentation and lyrics projection application.

.. _OpenLP: https://openlp.org/

- **type: openlp**

**Parameters:**

:``host`` (string, optional): Set the host name communicate with. Default is ``localhost``.
:``port`` (integer, optional): Set the port number that OpenLP is listening on. Default is ``4316``.
:``port_ws`` (integer, optional): Set the port number that OpenLP is listening on for websocket. Default is ``port_ws`` + 1, ie. ``4317``.

**YAML Example:**

.. code-block:: yaml

   steps:
     # This step reads from OpenLP
     - type: openlp
       host: localhost
       port: 4316

Usage
-----

At first, you need to enable remote-control feature on OpenLP.
Go to `Settings` / `Configure OpenLP` and open `Remote Interface` tab.

Check `Port number` and `Remote URL`.

Description
-----------

OpenLP has several types for service item.
We will take the text from **Songs**, **Bibles**, **Custom Slides**.
Other types such as **Presentations** and **Images** will be ignored.

.. tip::

  You may retrieve the title or the HTML by using :doc:`/plugins/jmespath`.

  **Example to retrieve the title:**

  .. code-block:: yaml
     :emphasize-lines: 3,4

      - type: openlp

      - type: jmespath
        filter: shapes[*].title

  **Example to retrieve HTML:**

  .. code-block:: yaml
     :emphasize-lines: 3,4

      - type: openlp

      - type: jmespath
        filter: shapes[*].html

  The HTML will be accepted by `Pthread Text plugin`_ on OBS Studio.

  .. _Pthread Text plugin: https://github.com/norihiro/obs-text-pthread
