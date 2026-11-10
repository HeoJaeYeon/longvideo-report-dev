"""Start videorag_retriever_service.py with a hard per-process GPU memory cap.
Run with CUDA_VISIBLE_DEVICES=<gpu>. Usage: python run_service_capped.py <config.yaml> [--preload VID]
Cap: env GPU_MEM_CAP_MIB (default 19000)."""
import os
import sys
import torch
cap_mib = int(os.environ.get("GPU_MEM_CAP_MIB", "19000"))
torch.cuda.set_per_process_memory_fraction(cap_mib / (torch.cuda.get_device_properties(0).total_memory / 2**20))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import videorag_retriever_service
sys.argv = ["videorag_retriever_service.py", "--config", sys.argv[1]] + sys.argv[2:]
videorag_retriever_service.main()
