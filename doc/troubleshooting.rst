Troubleshooting
===============

This page lists common problems you might encounter while using the PowerPoint to OBS Text Bridge and how to resolve them.

No text appears in OBS
----------------------

**Possible causes:**

- The OBS Text Source name in `config.yaml` does not match exactly.
- The OBS WebSocket connection is not active.
- PowerPoint is not running or not in slideshow mode.

**Solutions:**

- Double-check the `source_name` field in your configuration file.
- Open OBS and ensure the text source is visible in the active scene.
- Make sure PowerPoint is open and running the slideshow (not just editing mode).
- Verify that OBS WebSocket is enabled (see `Tools` / `WebSocket Server Settings`).

OBS connection failed
---------------------

**Possible causes:**

- Incorrect host, port, or password in `config.yaml`.
- OBS is not running.
- OBS WebSocket server is not enabled.
- Firewall prevents connection.

**Solutions:**

- Ensure OBS is open and the WebSocket server is enabled in OBS.
- Confirm the password and port match what is configured in OBS.
- Default port is usually `4455` for OBS 28 and later.
- Check OS's firewall settings.

PowerPoint not detected
-----------------------

**Possible causes:**

- PowerPoint is not the desktop version.
- Slideshow is not started.
- PowerPoint is running with administrator privileges and the tool is not (or vice versa).

**Solutions:**

- Use Microsoft PowerPoint (desktop version), not PowerPoint Online or mobile.
- Click **Slide Show** / **From Beginning** or **From Current Slide** to start the slideshow.
- If needed, run both PowerPoint and this tool with the same permission level (e.g., either both as administrator or both as regular user).

Text does not update when slides change
---------------------------------------

**Possible causes:**

- The text content hasn't changed between slides.
- PowerPoint is not focused, or slide transitions are animated with delays.

**Solutions:**

- Check that slides actually contain different text content.
- Wait until the transition finishes if using animations.
- Add `stdout` step to verify whether the slide is detected correctly.

Program window doesn't appear
-----------------------------

**Possible cause:**

- This tool runs as a background process by design.

**Solutions:**

- Check the system tray or Task Manager to confirm it is running.
- To stop the program, use Task Manager or provide a system tray icon (if implemented).

Text contains strange characters or formatting
----------------------------------------------

**Possible causes:**

- PowerPoint slide includes special characters, smart quotes, or formatting tags.
- Unicode not properly rendered in OBS text source.

**Solutions:**

- Use ``regex`` filter to replace the characters.
- Ensure the OBS text source uses a font that supports the required characters (e.g., for emoji or non-Latin scripts).

Still stuck?
------------

If none of these solutions help:

- Check the program's output on the console window.
- File an issue on the project's GitHub page with your configuration and a description of the problem.
