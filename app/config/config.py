import os
import shutil
import socket
from dotenv import load_dotenv
import toml
from loguru import logger

load_dotenv()

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
config_file = f"{root_dir}/config.toml"


def load_config():
    # fix: IsADirectoryError: [Errno 21] Is a directory: '/MoneyPrinterTurbo/config.toml'
    if os.path.isdir(config_file):
        shutil.rmtree(config_file)

    if not os.path.isfile(config_file):
        example_file = f"{root_dir}/config.example.toml"
        if os.path.isfile(example_file):
            shutil.copyfile(example_file, config_file)
            logger.info("copy config.example.toml to config.toml")

    logger.info(f"load config from file: {config_file}")

    try:
        _config_ = toml.load(config_file)
    except Exception as e:
        logger.warning(f"load config failed: {str(e)}, try to load as utf-8-sig")
        with open(config_file, mode="r", encoding="utf-8-sig") as fp:
            _cfg_content = fp.read()
            _config_ = toml.loads(_cfg_content)
    return _config_


def save_config():
    with open(config_file, "w", encoding="utf-8") as f:
        _cfg["app"] = app
        _cfg["azure"] = azure
        _cfg["siliconflow"] = siliconflow
        _cfg["ui"] = ui
        # _cfg["ui"]["hide_config"] = False
        f.write(toml.dumps(_cfg))


pexels_api_keys = os.getenv("PEXELS_API_KEYS")
if not pexels_api_keys:
    raise RuntimeError("PEXELS_API_KEYS environment variable is not defined.")
pexels_api_keys = list(
    filter(
        lambda x: x.strip().strip("'").strip('"') != "",
        pexels_api_keys.split("|"),
    )
)

pixabay_api_keys = os.getenv("PIXABAY_API_KEYS")
if not pixabay_api_keys:
    raise RuntimeError("PIXABAY_API_KEYS environment variable is not defined.")
pixabay_api_keys = list(
    filter(
        lambda x: x.strip().strip("'").strip('"') != "",
        pixabay_api_keys.split("|"),
    )
)

logger.info(f"pixabay API keys: {len(pixabay_api_keys)} keys")
logger.info(f"pexels API keys: {len(pexels_api_keys)} keys")


_cfg = load_config()
app = _cfg.get("app", {})
# update app config with pixabay and pexels API keys
_cfg["app"]["pixabay_api_keys"] = pixabay_api_keys
_cfg["app"]["pexels_api_keys"] = pexels_api_keys

# load openai_key api_base and model from environment variables
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not defined.")
openai_api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
if not openai_api_base:
    raise RuntimeError("OPENAI_API_BASE environment variable is not defined.")
openai_model = os.getenv("OPENAI_API_MODEL", "gpt-4o-mini")
if not openai_model:
    raise RuntimeError("OPENAI_API_MODEL environment variable is not defined.")
hide_settings_panel = os.getenv("HIDE_SETTINGS_PANEL_FOR_ALL_USERS", "false").strip().lower() == "true"
hide_all_logs = os.getenv("HIDE_LOG_FOR_ALL_USERS", "false").strip().lower() == "true"

_cfg["app"]["hide_config"] = hide_settings_panel
_cfg["app"]["openai_api_key"] = openai_key
_cfg["app"]["openai_base_url"] = openai_api_base
_cfg["app"]["openai_model_name"] = openai_model
_cfg["ui"]["hide_log"] = hide_all_logs

whisper = _cfg.get("whisper", {})
proxy = _cfg.get("proxy", {})
azure = _cfg.get("azure", {})
siliconflow = _cfg.get("siliconflow", {})
ui = _cfg.get(
    "ui",
    {
        "hide_log": hide_all_logs,
    },
)

hostname = socket.gethostname()

log_level = _cfg.get("log_level", "DEBUG")
listen_host = _cfg.get("listen_host", "0.0.0.0")
listen_port = _cfg.get("listen_port", 8080)
project_name = _cfg.get("project_name", "MoneyPrinterTurbo")
logger.info(f"project name: {project_name}")
logger.info(f"listen host: {listen_host}")
logger.info(f"listen port: {listen_port}")
project_description = _cfg.get(
    "project_description",
    "<a href='https://github.com/harry0703/MoneyPrinterTurbo'>https://github.com/harry0703/MoneyPrinterTurbo</a>",
)
project_version = _cfg.get("project_version", "1.2.6")
reload_debug = False

imagemagick_path = app.get("imagemagick_path", "")
if imagemagick_path and os.path.isfile(imagemagick_path):
    os.environ["IMAGEMAGICK_BINARY"] = imagemagick_path

ffmpeg_path = app.get("ffmpeg_path", "")
if ffmpeg_path and os.path.isfile(ffmpeg_path):
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

logger.info(f"{project_name} v{project_version}")
