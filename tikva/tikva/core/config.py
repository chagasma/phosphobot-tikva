"""
Store constants and configurations for the app in this file.
"""

from pathlib import Path
from typing import List, Literal, Optional, Union

import yaml
from loguru import logger
from pydantic import BaseModel, Field

from tikva.core.utils import get_home_app_path
from tikva.types import VideoCodecs

YAML_CONFIG_PATH = str(get_home_app_path() / "config.yaml")


def rename_keys_for_config(config_dict: dict) -> dict:
    """
    Rename the keys to correspond to the fields in the Configuration class.
    We write the keys in uppercase and add DEFAULT_ in front of them.
    """
    return {
        f"DEFAULT_{key.upper()}" if not key.startswith("DEFAULT_") else key: value
        for key, value in config_dict.items()
    }


def remove_default_prefix(config_dict: dict) -> dict:
    """
    Remove the DEFAULT_ prefix from the keys.
    """
    return {
        key.replace("DEFAULT_", "").lower(): value for key, value in config_dict.items()
    }


class Configuration(BaseModel):
    # Camera settings
    ENABLE_REALSENSE: bool = True
    ENABLE_CAMERAS: bool = True
    MAX_OPENCV_INDEX: int = 10
    MAIN_CAMERA_ID: Optional[int] = None

    # Robot settings
    ENABLE_CAN: bool = False
    MAX_CAN_INTERFACES: int = 4

    # Recording defaults
    DEFAULT_DATASET_NAME: str = "example_dataset"
    DEFAULT_FREQ: int = 30
    DEFAULT_EPISODE_FORMAT: Literal["lerobot_v2.1", "lerobot_v2", "json"] = (
        "lerobot_v2.1"
    )
    DEFAULT_VIDEO_CODEC: VideoCodecs = Field(default_factory=lambda: "avc1")
    DEFAULT_VIDEO_SIZE: List[int] = [320, 240]
    DEFAULT_TASK_INSTRUCTION: str = "None"
    DEFAULT_CAMERAS_TO_DISABLE: Optional[List[int]] = None
    DEFAULT_CAMERAS_TO_RECORD: Optional[List[int]] = None

    class Config:
        extra = "ignore"

    @classmethod
    def from_yaml(
        cls, config_path: Optional[Union[str, Path]] = None
    ) -> "Configuration":
        """
        Load configuration from a YAML file.
        Args:
            config_path (str): Path to the YAML configuration file.
        Returns:
            dict: Dictionary containing configuration values.
        """
        if config_path is None:
            config_path = YAML_CONFIG_PATH

        # Ensure the file exists. If not, create it.
        if not Path(config_path).exists():
            with open(config_path, "w") as file:
                file.write("")
            return cls()

        with open(config_path, "r") as file:
            try:
                config = yaml.safe_load(file)
            except yaml.YAMLError as e:
                logger.error(
                    f"Error loading configuration file: {e}.\nUsing default config. Please shut down the program and edit the config file."
                )
                config = None

        if config is None or not isinstance(config, dict):
            config = {}
        config = rename_keys_for_config(config)

        return cls(**config)

    def save_user_settings(self, user_settings: dict) -> None:
        """
        Save user settings to a YAML file.
        Args:
            user_settings (dict): Dictionary containing user settings.
        """

        try:
            user_settings = rename_keys_for_config(user_settings)
            new_config = Configuration.model_validate(user_settings)
        except Exception as e:
            logger.error(f"Error saving user settings: {e}")
            return

        # If the user_settings are valid, save them to the YAML file
        with open(YAML_CONFIG_PATH, "w") as file:
            yaml.dump(user_settings, file)

        # Then, replace inplace the fields of the current instance with the new instance
        for field in Configuration.model_fields.keys():
            setattr(self, field, getattr(new_config, field))


config = Configuration.from_yaml()
