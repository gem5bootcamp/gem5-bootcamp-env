#!/usr/bin/env python3

import torch
print("GPU available!") if torch.cuda.is_available() else print("No GPU available.")
x = torch.rand(5, 3)
print(x)
