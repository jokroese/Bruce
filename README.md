# 🦑 Bruce (Local Dev Setup)

This is a fork of the Bruce firmware for ESP32-based offensive security tools. This version is currently focused on development for the lilygo-t-embed-cc1101 board only.

## 🚀 Getting Started (Local Dev)

Prerequisites:

- uv (Python environment & package manager)
- platformio installed in your uv environment:

```
uv pip install platformio
```

1. Clone the Repo

```
git clone https://github.com/YOUR_FORK/Bruce.git
cd Bruce
```

2. Set Up Environment (using uv)

```
uv venv
uv pip install platformio
```

You can now run all PlatformIO commands inside the uv sandbox. 3. Build the Firmware

```
uv run pio run -e lilygo-t-embed-cc1101
```

4. Upload the Firmware
   Plug in your board, then run:

```
uv run pio run -e lilygo-t-embed-cc1101 -t upload
```

## 🧠 Notes

- No need for a global PlatformIO install — everything is isolated via uv.
- To avoid flashing errors, make sure you know the correct port and have the required USB permissions.
- You can edit platformio.ini to set or change defaults as needed.

## 🛠️ Roadmap (Fork)

This fork will evolve to include:

- 🔍 Intent-based menu redesign
- 🐙 New mascot & name
- 🧠 Default payloads and scripts
- 🐍 MicroPython support for user scripting
- 🦀 Rust integration for performance-critical parts

## 📖 More Info

- Official project: [github.com/pr3y/Bruce](https://github.com/pr3y/Bruce)
- Docs & features overview: [Bruce Wiki](https://github.com/pr3y/Bruce/wiki)
