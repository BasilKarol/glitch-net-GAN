import torch

for name in ['art', 'hard', 'light', 'medium']:
    params = torch.load(f"model/GlitchNet_{name}_params.pth", map_location=torch.device('cpu'))['gx']
    torch.save(params, f"model/Generator_{name}_params.pth")