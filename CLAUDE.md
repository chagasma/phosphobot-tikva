# Phosphobot Repository Structure

## Overview

Phosphobot is a CLI toolkit for robot teleoperation, dataset recording, and action model training. It provides a web dashboard, hardware abstraction layer, physics simulation, and ML model integration.

Technology stack: Python FastAPI backend, React frontend, PyBullet simulation, WebSocket/HTTP APIs.

## Directory Structure

### /phosphobot/ - Core Python Package

Main application package containing all core functionality.

#### /phosphobot/hardware/ - Robot Hardware Layer

Hardware abstraction and robot drivers.

Key files:
- base.py (1500+ lines) - Abstract base classes: BaseRobot, BaseManipulator, BaseMobileRobot
- sim.py (661 lines) - PyBullet simulation wrapper with GUI/headless modes
- Robot implementations:
  - so100.py - 6-DOF arm with Feetech servos
  - koch11.py - Custom manipulator
  - piper.py - Agilex Piper (CAN-based)
  - wx250s.py - Interbotix arm
  - go2.py (18,860 lines) - Unitree Go2 quadruped
  - lekiwi.py - Custom mobile platform
  - urdfloader.py - Generic URDF loader
- /motors/ - Motor control SDKs (Dynamixel, Feetech)

Robot interface methods:
- connect(), disconnect()
- read_position(), write_position()
- read_torque(), write_torque()
- enable_torque(), disable_torque()
- get_end_effector_pose()
- Calibration sequences

#### /phosphobot/am/ - Action Models

ML model integration for robot control.

Files:
- base.py - Abstract ActionModel interface
- lerobot.py - LeRobot framework integration
- act.py - Action Chunking Transformer
- pi05.py - Pi0.5 VLA model
- gr00t.py - NVIDIA Groot model
- smolvla.py - SmolVLA model

#### /phosphobot/endpoints/ - FastAPI REST API

HTTP endpoints for web dashboard.

Key endpoints:
- control.py (1399 lines) - Robot control, teleoperation, AI inference
- recording.py - Dataset recording management
- training.py - Model training jobs
- camera.py - Camera management
- pages.py - Dashboard page serving
- auth.py - Authentication
- networking.py - Network configuration
- chat.py - Chat interface integration

#### /phosphobot/models/ - Data Models

Pydantic schemas for validation.

Files:
- __init__.py (40,218 lines) - Core data models and schemas
- dataset.py - Dataset structures
- lerobot_dataset.py (160,080 lines) - LeRobot format
- robot.py - Robot configuration models
- camera.py - Camera models

#### /phosphobot/chat/ - Terminal Chat Interface

Textual TUI application.

Files:
- app.py - Textual TUI app
- agent.py - AI agent logic
- utils.py - Chat utilities

#### Other Core Files

- main.py - CLI entry point (typer commands)
- app.py - FastAPI application and server startup
- robot.py - RobotConnectionManager (auto-detection, lifecycle)
- configs.py - Configuration class with YAML support
- camera.py - Camera detection and management
- utils.py - Utility functions

### /resources/ - Static Resources

- /urdf/ - Robot URDF files for PyBullet simulation
- /calibration/ - Robot-specific calibration JSON files
- /default/ - Default robot configurations
- /swagger-ui/ - API documentation UI assets
- /dist/ - Built React frontend (served as static files)
- tokens.toml - Authentication tokens

### /tests/ - Test Suite

- /api/ - API integration tests
- /phosphobot/ - Unit tests for robot classes
- /realsense/ - RealSense camera tests
- udp_client.py - UDP teleoperation testing
- test_identify_cameras.html - Camera identification tool

### /hooks/ - Git hooks for development

## Entry Points

### CLI Commands

Entry point: phosphobot/main.py

Commands:
- phosphobot run - Start server with web dashboard
- phosphobot run --chat - Launch chat TUI mode
- phosphobot info - Show hardware/camera information
- phosphobot update - Display update instructions

Flags:
- --simulation=headless - Headless PyBullet simulation
- --simulation=gui - PyBullet GUI in separate window
- --only-simulation - Force simulation mode
- --port=PORT - Set server port

### Server Startup

File: phosphobot/app.py

Function: start_server()
- Initializes FastAPI app
- Auto-selects port (80, then 8020-8039)
- Launches Uvicorn ASGI server
- Serves React dashboard from /resources/dist/

Default URL: http://localhost:80

## Configuration

### Configuration File

Location: ~/.phosphobot/config.yaml

Managed by: phosphobot/configs.py (Configuration class)

Key settings:
- SIM_MODE - Simulation mode (headless/gui)
- ONLY_SIMULATION - Force simulation
- ENABLE_REALSENSE - Toggle RealSense cameras
- ENABLE_CAN - Toggle CAN device scanning
- MAX_OPENCV_INDEX - Camera scan limit
- Recording defaults (frequency, codec, format)

### Project Config

File: pyproject.toml

Current version: 0.3.134
Python requirement: >=3.9
Package manager: uv

## Robot Integration

### Connection Manager

File: phosphobot/robot.py

Class: RobotConnectionManager

Detection flow:
1. Scan USB serial ports (list_ports.comports())
2. Scan CAN interfaces (can0, can1)
3. Try each robot class's from_port() method
4. Connect and validate
5. Add to active robots list

Supported connection types:
- USB serial (Feetech, Dynamixel servos)
- CAN bus (Agilex Piper)
- Network (Unitree Go2)
- Simulation (always available)

### Adding a New Robot

Steps:
1. Create URDF file in /resources/urdf/
2. Create driver class in /phosphobot/hardware/my_robot.py
3. Inherit from BaseRobot or BaseManipulator
4. Implement abstract methods
5. Add detection logic to RobotConnectionManager
6. Test in simulation with --simulation=gui
7. Test on real hardware

## Build Process

### Frontend Build

Location: /dashboard/ (separate from this repo)

Commands:
```bash
cd ./dashboard
npm i && npm run build
cp -r ./dist/* ../phosphobot/resources/dist/
```

### Backend Build

Commands:
```bash
cd phosphobot
uv sync
uv run phosphobot run --simulation=headless
```

### Complete Build

Makefile shortcut:
```bash
make
```

Equivalent to:
1. Build frontend dashboard
2. Copy dist to resources
3. Install Python dependencies via uv
4. Run phosphobot

## Key Dependencies

### Robotics
- pybullet >=3.2.7 - Physics simulation
- dynamixel-sdk >=3.7.31 - Dynamixel motor control
- feetech-servo-sdk >=1.0.0 - Feetech servo control
- piper-sdk >=0.4.2 - Agilex Piper SDK
- go2-webrtc-connect >=0.2.1 - Unitree Go2 connection

### Web Framework
- fastapi[standard] >=0.115.5 - REST API framework
- uvicorn >=0.32.1 - ASGI server
- websockets >=14.1 - WebSocket support

### Computer Vision
- opencv-python-headless >=4.0 - Image processing
- pyrealsense2 - Intel RealSense cameras (platform-specific)

### ML/Data
- numpy >=1.26.4 - Numerical computing
- scipy >=1.13.0 - Scientific computing
- pandas >=2.2 - Data manipulation
- datasets >=3.2.0 - Dataset management
- huggingface-hub >=0.28.0 - Model hub integration

### Utilities
- typer >=0.16.0 - CLI framework
- loguru >=0.7.2 - Logging
- pydantic >=2.10.2 - Data validation
- textual >=6.1.0 - TUI framework

## Control Modes

The system supports multiple teleoperation modes:

1. Keyboard - Direct keyboard control via web dashboard
2. VR Control - Meta Quest integration
3. Leader-Follower - Teaching mode with leader arm
4. AI Inference - Action model inference (VLA models)

Control flow:
- User input (keyboard/VR/leader) OR AI model output
- FastAPI endpoint receives control command
- RobotConnectionManager routes to active robot(s)
- Robot driver translates to motor commands
- Simulation mirror updates in PyBullet

## Dataset Recording

Format: LeRobot dataset format (Parquet files)

Recording flow:
1. Start recording via /api/recording/start endpoint
2. Capture frames at configured frequency
3. Record: robot positions, camera images, actions
4. Save to Parquet files in episodes/
5. Upload to Hugging Face Hub (optional)

Recommended: 40+ episodes for training

## Model Training

Supported frameworks:
- LeRobot (Hugging Face)
- Action Chunking Transformer (ACT)
- Vision-Language-Action models (VLAs)

Training flow:
1. Record dataset
2. Configure training job via /api/training/ endpoint
3. Launch training (local or cloud)
4. Deploy trained model
5. Use for AI inference control

## Code Statistics

Approximate line counts:
- phosphobot/models/__init__.py - 40,218 lines
- phosphobot/models/lerobot_dataset.py - 160,080 lines
- phosphobot/hardware/go2.py - 18,860 lines
- phosphobot/hardware/base.py - 1,500+ lines
- phosphobot/endpoints/control.py - 1,399 lines
- phosphobot/hardware/sim.py - 661 lines

Total: ~16,000+ lines across main modules (excluding generated model files)

## Development Workflow

Typical development cycle:
1. Clone repo with git lfs
2. Install uv package manager
3. Run make to build frontend + backend
4. Start server with phosphobot run --simulation=gui
5. Test robot integration in simulation
6. Deploy to real hardware
7. Record datasets
8. Train action models
9. Deploy for AI control

## Testing

Test framework: pytest

Test categories:
- Unit tests - /tests/phosphobot/
- API tests - /tests/api/
- Integration tests - /tests/realsense/, UDP tests

Run tests:
```bash
pytest tests/
```

## Platform Support

Supported platforms:
- Linux - Primary development platform
- macOS - Supported (requires PyBullet workaround on Silicon)
- Windows - Supported (requires Visual C++ Build Tools)

## Common Issues

MacOS Silicon PyBullet compilation:
- Use forked pybullet from git submodules
- Build from source with modified zutil.h
- Edit pyproject.toml to use local build

Windows PyBullet compilation:
- Install Visual Studio
- Install Microsoft C++ v14 Build Tools

## API Structure

Base URL: http://localhost:80/api/

Main routes:
- /api/control/* - Robot control endpoints
- /api/recording/* - Dataset recording
- /api/training/* - Model training
- /api/camera/* - Camera management
- /api/auth/* - Authentication
- /api/networking/* - Network config

WebSocket endpoint: ws://localhost:80/ws

## Simulation Details

Simulation backend: PyBullet

Modes:
- Headless - No GUI, faster
- GUI - Separate process with 3D visualization

Features:
- URDF-based robot models
- Physics simulation
- Shared memory IPC
- Multi-robot support
- Automatic stepping thread

GUI controls:
- Mouse to rotate camera
- WASD to move camera
- Q/E to zoom

## File Formats

- .urdf - Robot definition (XML)
- .yaml - Configuration files
- .parquet - Dataset storage (LeRobot format)
- .json - Calibration data
- .toml - Tokens and project config

## Authentication

Default tokens location: /resources/tokens.toml

Authentication backends:
- Supabase integration
- Local token validation

## Logging

Logger: Loguru

Log levels:
- DEBUG - Development details
- INFO - Standard operations
- WARNING - Non-critical issues
- ERROR - Critical failures

Monitoring integrations:
- Sentry - Error tracking
- PostHog - Analytics

## Network Communication

Protocols:
- HTTP/REST - Primary API
- WebSocket - Real-time updates
- UDP - Low-latency teleoperation
- ZMQ - Camera streaming
- CAN - Motor bus communication

## Camera System

File: phosphobot/camera.py

Supported cameras:
- OpenCV cameras (USB webcams)
- Intel RealSense D405, D435, D435i
- Network cameras (RTSP)

Detection:
- Auto-scan OpenCV indices (0 to MAX_OPENCV_INDEX)
- RealSense SDK enumeration
- Manual camera addition

Streaming:
- ZMQ for low-latency
- HTTP MJPEG fallback
- WebRTC for VR

## Extension Points

The codebase is designed for extension:

1. New robots - Inherit from BaseRobot, add to RobotConnectionManager
2. New action models - Inherit from ActionModel in /am/base.py
3. New endpoints - Add router to /endpoints/, register in app.py
4. New cameras - Extend camera detection in camera.py
5. Custom URDFs - Add to /resources/urdf/

## License

MIT License

Made by the Phospho community.
