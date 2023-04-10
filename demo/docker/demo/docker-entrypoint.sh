#!/bin/bash
conda run --no-capture-output -n sliderule_env voila --theme=dark --no-browser --Voila.ip=0.0.0.0 --MappingKernelManager.cull_interval=60 --MappingKernelManager.cull_idle_timeout=120 /voila_demo.ipynb
