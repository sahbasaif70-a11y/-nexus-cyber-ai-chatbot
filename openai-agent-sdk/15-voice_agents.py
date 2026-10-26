import asyncio

import numpy as np
import sounddevice as sd
from dotenv import load_dotenv

from agents import Agent

from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    TTSModelSettings,
    VoicePipeline,
    VoicePipelineConfig,
)

load_dotenv()

SAMPLE_RATE = 24_000

