# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/99_audio_classification.ipynb (unless otherwise specified).

__all__ = []

# Cell
import os
import json
import tensorflow as tf
import numpy as np

# Cell

import audioengine
from .utils.gpu import list_all_gpus, set_gpu_list_memory_limit
from .utils.schema import verify_audioengine_dataset, verify_audioengine_internal_audio_representation_schema
from .utils.misc import log_init, log_info, log_debug, log_error, pad_up_to
from .models import Simple1DConvNet
from .utils.wav_utils import get_max_samples_in_wav_from_directory