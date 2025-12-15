# Tikva

Simplified robotics toolkit for CLI dataset recording and robot control.

## Features

- Auto-detection of robots via USB/CAN by PID
- Auto-configuration of cameras (OpenCV + RealSense)
- Automatic calibration by serial number
- Dataset recording in LeRobot format
- Intuitive CLI with commands + interactive REPL
- Optional minimal REST API

## Installation

```bash
pip install -e .
```

With optional dependencies:

```bash
pip install -e ".[api,realsense]"
```

## Quick Start

### List detected robots
```bash
tikva robot list
```

### Calibrate a robot
```bash
tikva robot calibrate 0
```

### List cameras
```bash
tikva camera list
```

### Start recording
```bash
tikva record start --dataset my_data --freq 30
tikva record stop
tikva record save
```

### Interactive REPL
```bash
tikva repl
```

## Configuration

Configuration file: `~/.tikva/config.yaml`

```yaml
enable_realsense: true
enable_cameras: true
max_opencv_index: 10
default_freq: 30
```

## Architecture

```
tikva/
├── core/         # Framework-agnostic logic
├── hardware/     # Robot abstraction
├── cameras/      # Camera implementations
├── models/       # Pydantic models
├── cli/          # CLI interface
└── api/          # Optional FastAPI
```


