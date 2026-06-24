import os
import torch
import pickle

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "cnn_model.pt")

def infer(image_path):
    # If a PyTorch model exists, load and run a simple inference pipeline; otherwise return a demo response
    if os.path.exists(MODEL_PATH):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        data = torch.load(MODEL_PATH, map_location=device)
        from torchvision import transforms
        from PIL import Image
        model_state = data.get('model_state_dict')
        classes = data.get('classes', [])
        # load a ResNet50 skeleton
        from torchvision import models
        import torch.nn as nn
        model = models.resnet50(pretrained=False)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, len(classes))
        model.load_state_dict(model_state)
        model.to(device)
        model.eval()
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[.485,.456,.406], std=[.229,.224,.225])
        ])
        img = Image.open(image_path).convert('RGB')
        x = preprocess(img).unsqueeze(0).to(device)
        with torch.no_grad():
            out = model(x)
            probs = torch.softmax(out, dim=1).cpu().numpy()[0]
            idx = int(probs.argmax())
            return {"disease": classes[idx] if classes else str(idx), "confidence": float(probs.max())}
    else:
        # demo fallback
        return {"disease": "healthy", "confidence": 0.5}
