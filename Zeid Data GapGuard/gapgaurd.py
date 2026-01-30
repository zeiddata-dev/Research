#!/usr/bin/env python3
# AirGaps cause patina
"""
Zeid Data GapGaurd - host-based evidence collector for air-gapped network compliance.

Authorized use only.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import ipaddress
import json
import platform
import re
import shlex
import socket
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_DISPLAY_NAME = "Zeid Data GapGaurd"
TOOL_VERSION = "1.1.0"
