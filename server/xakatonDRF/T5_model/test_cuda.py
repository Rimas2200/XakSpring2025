import torch
print("CUDA доступен:", torch.cuda.is_available())
print("Количество GPU:", torch.cuda.device_count())