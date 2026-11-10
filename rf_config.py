"""
Load config.yaml with portable paths (2026-11-10).

A path value in the config may be
  - relative  : resolved against the report_framework root (the directory of this file), not against the config
                file, so config copies that the GPU scripts write into output folders resolve the same way
                (e.g. `../WorldMM` = the WorldMM checkout next to report_framework/);
  - ${VAR}    : replaced by that environment variable (an unset variable is an error), e.g. `${WORLDMM_DIR}`;
  - absolute  : used as is.
load_config() returns the parsed config with every key in PATH_KEYS turned into an absolute path; all other
values are returned exactly as yaml.safe_load parses them.
"""
import os
import re
from typing import Any, Dict

import yaml

RF_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(RF_ROOT, "config.yaml")

# Config keys that hold file system paths.
PATH_KEYS = {
    "paths": ("worldmm_root", "hf_home", "caption_dir", "metadata_dir", "episodic_cache_root", "log_dir"),
    "service": ("frames_dir",),
    "report": ("outputs_dir", "deep_reporter_log_dir"),
}
_ENV_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def resolve_path(value: str) -> str:
    def env(match):
        name = match.group(1)
        if name not in os.environ:
            raise ValueError(f"config path {value!r}: environment variable {name} is not set")
        return os.environ[name]

    path = _ENV_RE.sub(env, value)
    return path if os.path.isabs(path) else os.path.normpath(os.path.join(RF_ROOT, path))


def load_config(path: str = DEFAULT_CONFIG) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for section, keys in PATH_KEYS.items():
        for key in keys:
            if cfg.get(section, {}).get(key) is not None:
                cfg[section][key] = resolve_path(str(cfg[section][key]))
    return cfg
