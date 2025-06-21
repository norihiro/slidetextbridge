# Text Feed from Microsoft PowerPoint

This tool retrieves text from the current presentation on Microsoft PowerPoint,
modifies the text, and send it to OBS Studio.

This tool bridges Microsoft PowerPoint and OBS Studio during live event.
While a PowerPoint slideshow is being displayed in-person,
this tool retrieves the current slide's text,
optionally applies small modifications,
and sends it to OBS Studio to be shown in a *Text Source*
-- typically as a lower-third overlay during a livestream.

## Features

- Captures live slideshow text on PowerPoint
  - Periodically checks which slide is currently being shown in PowerPoint slideshow.
  - Shapes can be filtered by placeholder, size, etc. powered by [JMESPath](https://jmespath.org/).
- Filter texts
  - Adjusts line breaks.
- Sends OBS Studio
  - Sends the text to a specific text source in OBS Studio via [obs-websocket](https://github.com/obsproject/obs-websocket).

## Use Case

This tool is ideal for:
- Church services, seminars, or other events where PowerPoint is used for the in-person audience.
- Situations where OBS Studio overlays need to match slide content automatically without manual edits.

## Requirements

- Microsoft Windows
- Microsoft PowerPoint (desktop version)
  (Uses COM interface to access the slideshow.)
- OBS Studio 30 or later

## Configuration

Edit `ppttextfeed.yaml` to set these information.
- Shape selection rule
- Text format rules
- OBS websocket URL and password
- Target text source name

Note: If PowerPoint and OBS Studio run in different computers,
run this program on the computer running PowerPoint.

## Usage

- Start your PowerPoint slideshow as usual.
- Run `ppttextfeed.exe`
  The program will show up a console window. You can minimize it.
- Also run OBS Studio.

Footnote: You may start this tool first.

<!-- TODO: put an example
## Example
-->
