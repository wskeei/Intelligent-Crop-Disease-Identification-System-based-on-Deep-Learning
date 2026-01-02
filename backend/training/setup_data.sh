#!/bin/bash

# Setup Data Directory
mkdir -p data
cd data

echo "Downloading PlantVillage Dataset..."
if command -v wget >/dev/null 2>&1; then
    wget -q https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip -O plantvillage.zip
else
    echo "wget not found, using curl..."
    curl -L https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip -o plantvillage.zip
fi

echo "Unzipping..."
unzip -q plantvillage.zip

echo "Organizing..."
# Move the color images to the root of ./data
# Structure in zip: PlantVillage-Dataset-master/raw/color/[classes]
mv PlantVillage-Dataset-master/raw/color/* .

# Cleanup
rm -rf PlantVillage-Dataset-master plantvillage.zip

echo "Data setup complete! Dataset is in backend/training/data"
