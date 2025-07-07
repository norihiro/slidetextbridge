Input Step: `impress`
=====================

This step reads text from a LibreOffice Impress presentation.
It is designed to be an input source, meaning it's usually the first step in the pipeline.

- **type: impress**

**Parameters:**

:``host`` (string, optional): Set the host name communicate with. Default is ``localhost``.
:``port`` (integer, optional): Set the port number that LibreOffice is listening on. Default is ``2002``.
:``pipe_name`` (string, optional): Set the pipe name that LibreOffice is waiting. Default is unset.
:``poll_wait_time`` (float, optional): Set the wait time for each polling in seconds. 0.1 seconds by default.

Connecting with socket
  Usually, you don't need to specify any parameters in the configuration file.
  However, you may change the host or port so that you can connect to the remote host.

  .. code-block:: yaml

     steps:
       - type: impress
         host: localhost
         port: 2002
         poll_wait_time: 0.1

  To use the socket, start libreoffice like below.

  .. code-block:: bash

     libreoffice '--accept=socket,host=localhost,port=2002;urp;'


Connecting with pipe
  If ``pipe_name`` is specified, the connection to LibreOffice is made through the named pipe.
  Below is the example of step.

  .. code-block:: yaml

     steps:
       - type: impress
         pipe_name: slidetextbridge_pipe
         poll_wait_time: 0.1

  To use the pipe, start libreoffice like below.

  .. code-block:: bash

     libreoffice '--accept=pipe,name=slidetextbridge_pipe;urp;'
