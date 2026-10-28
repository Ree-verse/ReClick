<h1 align="center">
    ReClick
</h1>

<p align="center">
  <b>Simple auto-clicker.</b>
</p>

<p align="center">
  <a href="https://github.com/ree-verse/ReClick"><img src="https://raw.githubusercontent.com/ree-verse/ReClick/main/assets/ReClick.svg" alt="ReClick logo" height=256></a>
</p>

ReClick lets you automate mouse clicks with a clean desktop UI, configurable intervals, repeat modes, click types, fixed/current cursor position, and global hotkeys.

## Preview

https://github.com/user-attachments/assets/2dac0445-383f-4fa8-86ff-370bc7e0de7e

## Features

- Set click interval in:
  - Hours
  - Minutes
  - Seconds
  - Milliseconds
- Choose mouse button:
  - Left
  - Right
  - Middle
- Choose click type:
  - Single
  - Double
- Repeat options:
  - Fixed number of times
  - Infinite until stopped
- Click at:
  - Current cursor position
  - Fixed X/Y position
- Built-in position picker
- Global hotkeys for start/stop/toggle

## Requirements

- Python **3.10+**
- Dependencies:
  - `customtkinter`
  - `keyboard`
  - `mouse`

## Installation

### 1. Via releases

You can download pre-built binaries directly from the GitHub Releases page:
> https://github.com/ree-verse/ReClick/releases

### 2. Manual Installation

First, run:
```bash
pip install customtkinter keyboard mouse
```

Then:
```bash
python path/to/main.py
```

Alternatively, you can simply run the following commands from the project's root directory:
```bash
make install
make build
```

## Default Hotkeys

- `F6`: Start
- `F7`: Stop
- `F8`: Toggle start/stop

You can change them in the `HOTKEYS` dictionary inside the code:

```python
HOTKEYS = {
    "start": "F6",
    "stop": "F7",
    "toggle": "F8",
}
```

## How to Use

1. Launch the app.
2. Set the click interval.
3. Choose:
   - mouse button
   - single or double click
4. Select repeat mode:
   - finite number of clicks
   - infinite
5. Select click position:
   - current cursor position
   - fixed coordinates
6. If needed, use **Pick** to capture a screen position.
7. Click **Start** or press `F6`/`F8`.

## Notes

- Global hotkeys work even when the app is not focused.
- On some Linux, `keyboard` and `mouse` may require **root permissions**.
- On Linux, the app uses dark mode by default because automatic theme detection may not work properly.
- Due to Windows system timer limitations, the absolute fastest click rate is about 60-65 clicks per second (~15.6ms delay). Setting the interval to 1ms will run at this maximum speed, not 1,000 clicks per second.
- If you accidentally type text (like "abc") into the number fields, the app won't crash. It will safely ignore the text and use a default value (like 0 or 1) in the background.

## Code note

Certain functions and variables are intentionally only used once, for readability purposes.

## Support

If you have questions, suggestions, or want to hang out with other developers, join my Discord server: [Ree-verse GitHub Support](https://discord.gg/ZZfqH9Z4uQ).

## Credits

This project was inspired by [AutoClicker](https://github.com/oriash93/AutoClicker).
Many thanks to [oriash93](https://github.com/oriash93) for the inspiration.

## License

Released under the [MIT License](https://github.com/ree-verse/ReClick/blob/main/LICENSE) © 2026 [Ree-verse](https://github.com/ree-verse).

## Star History

<a href="https://star-history.com/#Ree-verse/ReClick&Timeline">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ree-verse/ReClick&type=Timeline&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ree-verse/ReClick&type=Timeline" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ree-verse/ReClick&type=Timeline" />
  </picture>
</a>

## Disclaimer

- **Wayland is NOT supported.** This autoclicker only works on X/Xorg/X11 display servers due to Wayland's security restrictions. To check your display server, run `echo $XDG_SESSION_TYPE`. Switch to an X11 session if needed.

- **Use responsibly.** Autoclickers may violate Terms of Service for online games and websites. This tool is intended for legitimate automation, accessibility, and testing purposes only. Use at your own risk.
