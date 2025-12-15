import subprocess
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
from loguru import logger


def euler_from_quaternion(quaternion: np.ndarray, degrees: bool) -> np.ndarray:
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    """
    from scipy.spatial.transform import Rotation as R

    try:
        return R.from_quat(quaternion).as_euler("xyz", degrees=degrees)
    except ValueError as e:
        logger.error(
            f"Error converting quaternion to Euler angles. Returning zeros. {e}"
        )
        return np.zeros(3)


def get_quaternion_from_euler(euler_angles: np.ndarray, degrees: bool) -> np.ndarray:
    """
    Convert an Euler angle to a quaternion.
    """
    from scipy.spatial.transform import Rotation as R

    return R.from_euler("xyz", angles=euler_angles, degrees=degrees).as_quat()


def cartesian_to_polar(
    x: np.ndarray, y: np.ndarray, z: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert cartesian coordinates to polar coordinates
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta, z


def polar_to_cartesian(
    r: np.ndarray, theta: np.ndarray, z: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert polar coordinates to cartesian coordinates
    """
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, z


def get_base_path() -> Path:
    """
    Return the base path of the app.
    This is used to load bundled resources.

    tikva/    <-- base path
        tikva/
            main.py
            ...
        resources/
        ...
    """
    return Path(__file__).parent.parent.parent


def get_resources_path() -> Path:
    """
    Return the path of the resources directory.
    This is used to load bundled resources.

    tikva/
        tikva/
            main.py
            ...
        resources/    <-- resources path
        ...
    """
    return get_base_path() / "resources"


def get_home_app_path() -> Path:
    """
    Return the path to the app's folder in the user's home directory.
    This is used to store user-specific data.

    It's platform dependent.

    user_home/
        .tikva/
            calibration/
            recordings/
            ...
    """
    home_path = Path.home() / ".tikva"
    home_path.mkdir(parents=True, exist_ok=True)
    (home_path / "calibration").mkdir(parents=True, exist_ok=True)
    (home_path / "recordings").mkdir(parents=True, exist_ok=True)
    return home_path


def is_can_plugged(interface: str = "can0") -> bool:
    """
    Checks if a specified CAN interface exists.
    """
    try:
        if sys.platform == "linux":
            result = subprocess.run(
                ["ip", "link", "show", interface],
                capture_output=True,
                text=True,
                check=True,
                timeout=3,
            )
            return "does not exist" not in result.stdout.lower()
        elif sys.platform == "darwin":
            result = subprocess.run(
                ["ifconfig", interface],
                capture_output=True,
                text=True,
                check=True,
                timeout=3,
            )
            return "does not exist" not in result.stdout.lower()
        elif sys.platform == "win32":
            result = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True,
                check=True,
                timeout=3,
                errors="replace",
            )
            if result.stdout is None:
                return False
            return interface in result.stdout.lower()
        else:
            raise OSError(f"Unsupported platform: {sys.platform}")
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return False
        logger.warning(f"Failed to check CAN interface status: {str(e)}")
        return False
    except FileNotFoundError as e:
        logger.warning(f"OSError: Required system command not found: {str(e)}")
        return False
    except Exception as e:
        logger.warning(f"Unexpected error checking CAN interface: {str(e)}")
        return False
