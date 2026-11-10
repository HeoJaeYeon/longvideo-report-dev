"""Start report_framework/local_llm_server.py with a hard per-process GPU memory cap (run with CUDA_VISIBLE_DEVICES=<gpu>)."""
import os
import sys
import torch
torch.cuda.set_per_process_memory_fraction(19000 / (torch.cuda.get_device_properties(0).total_memory / 2**20))
RF = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, RF)
import local_llm_server
sys.argv = ["local_llm_server.py", "--config", os.path.join(RF, "config.yaml"), "--port", sys.argv[1]]
local_llm_server.main()
