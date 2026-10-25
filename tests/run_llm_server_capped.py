"""Start report_framework/local_llm_server.py with a hard per-process GPU memory cap (run with CUDA_VISIBLE_DEVICES=<gpu>)."""
import sys
import torch
torch.cuda.set_per_process_memory_fraction(19000 / (torch.cuda.get_device_properties(0).total_memory / 2**20))
sys.path.insert(0, "/data1/jyheo/workspace/VideoRAG/report_framework")
import local_llm_server
sys.argv = ["local_llm_server.py", "--config", "/data1/jyheo/workspace/VideoRAG/report_framework/config.yaml", "--port", sys.argv[1]]
local_llm_server.main()
