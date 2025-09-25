# Known Faces Directory - Trump Dataset

This directory contains a comprehensive dataset for face recognition demonstration purposes.

## Current Dataset:
```
known_faces/
└── trump/
    ├── trump1.jpg - trump50.jpg          # Original Trump photos (50 images)
    ├── donald trump51.jpg - trump100.jpg  # Extended Trump dataset (50 images)  
    └── donald trump speech101.jpg - speech150.jpg  # Speech/presentation photos (46 images)
```

**Total: ~146 high-quality Trump face images** for robust face recognition training and testing.

## Dataset Features:

## Guidelines:

### High-Quality Image Collection:
- ✅ Clear, front-facing photos with excellent lighting
- ✅ Various angles and expressions for robust training
- ✅ Multiple lighting conditions (indoor/outdoor/studio)
- ✅ Different backgrounds and contexts
- ✅ Speech/presentation scenarios for real-world testing

### Dataset Statistics:
- **Images**: ~146 high-resolution photos
- **Variations**: Multiple expressions, angles, and lighting
- **Quality**: Professional and semi-professional photography
- **Formats**: JPG optimized for fast loading
- **Face Size**: All images contain clearly visible faces (>112x112px)

### Recognition Performance:
This comprehensive dataset enables:
- 🎯 **High accuracy** face recognition (>95% confidence)
- ⚡ **Fast training** with diverse examples
- 🔄 **Robust testing** across different scenarios
- 📊 **Reliable benchmarking** for face recognition systems

## Quick Start:
Build the face database from this dataset:
```bash
# Load Trump dataset into database
python main.py db load data/known_faces

# Test recognition on sample image
python main.py demo --type recognition --image data/test_images/test_trump.jpg

# Start real-time recognition
python main.py realtime
```

## Adding Your Own Data:
To add new people, create folders like:
```bash
mkdir data/known_faces/person_name
# Add 5-10 clear photos of the person
python main.py db load data/known_faces
```