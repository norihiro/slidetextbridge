# Live Text Bridge from Presentation

This tool retrieves text from the current presentation on Microsoft PowerPoint or LibreOffice Impress,
modifies the text, and send it to OBS Studio.

This tool bridges from presentation texts to streaming lower-thirds during live event.
While a presentation slideshow is being displayed in-person,
this tool retrieves the current slide's text,
optionally applies small modifications,
and sends it to OBS Studio to be shown in a *Text Source*
-- typically as a lower-third overlay during a livestream.

## Features

- Captures live slideshow from these tools
  - Microsoft PowerPoint
  - LibreOffice Impress
- Filters
  - Selects shapes by placeholder, size, etc. powered by [JMESPath](https://jmespath.org/).
  - Line break adjustment.
  - Text replacement with regular expression.
- Sends to OBS Studio
  - Sends the text to a specific text source in OBS Studio via [obs-websocket](https://github.com/obsproject/obs-websocket).

## Use Case

This tool is ideal for:
- Church services, seminars, or other events where PowerPoint is used for the in-person audience.
- Situations where OBS Studio overlays need to match slide content automatically without manual edits.

## Requirements

- Host running presentation tool
  - Microsoft Windows + PowerPoint (desktop version)
    (Uses COM interface to access the slideshow.)
  - Linux + LibreOffice Impress
- Host running the streaming
  - OBS Studio 30 or later

(In future, we might support more tools.)

## Configuration

Edit `config.yaml` to set these information.
- Shape selection rule
- Text format rules
- OBS websocket URL and password
- Target text source name

Note: If presentation and streaming run on the different computers,
run this program on the computer running PowerPoint or Impress.

## Usage

- Start your presentation slideshow as usual.
- Run `slidetextbridge.exe`
  The program will show up a console window. You can minimize it.
- Also run OBS Studio.

Footnote: You may start this tool either earlier or later than starting the presentation tool.

<!-- TODO: put an example
## Example
-->
