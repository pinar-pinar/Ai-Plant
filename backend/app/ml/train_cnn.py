import torch
from torchvision import transforms, datasets, models
from torch import nn, optim
from torch.utils.data import DataLoader
import argparse
import os

def train(data_dir, epochs=10, batch_size=32, lr=1e-4, out_path="models/cnn_model.pt", device="cuda"):
    # Préparation dataset
    train_transforms = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[.485,.456,.406], std=[.229,.224,.225])
    ])
    train_ds = datasets.ImageFolder(os.path.join(data_dir, "train"), transform=train_transforms)
    val_ds = datasets.ImageFolder(os.path.join(data_dir, "val"), transform=train_transforms)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    # Model transfer learning
    model = models.resnet50(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(train_ds.classes))

    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # boucle d'entraînement (simplifiée)
    for epoch in range(epochs):
        model.train()
        for imgs, labels in train_loader:
            imgs = imgs.to(device); labels = labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        # validation ici...
    torch.save({'model_state_dict': model.state_dict(), 'classes': train_ds.classes}, out_path)
    print("Model saved to", out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--out", default="models/cnn_model.pt")
    args = parser.parse_args()
    train(args.data_dir, epochs=args.epochs, out_path=args.out)
