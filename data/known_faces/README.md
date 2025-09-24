# Known Faces Directory

This directory should contain subdirectories for each person you want to recognize.

## Structure:
```
known_faces/
├── person1/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── person2/
│   ├── image1.jpg
│   └── image2.jpg
└── another_person/
    ├── pic1.png
    ├── pic2.png
    └── pic3.png
```

## Guidelines:

### Image Quality:
- Use clear, front-facing photos
- Good lighting (avoid shadows on face)
- Face should be clearly visible
- Minimum face size: 112x112 pixels
- Avoid blurry or low-resolution images

### Number of Images:
- **Minimum**: 1 image per person
- **Recommended**: 3-5 images per person
- **Optimal**: 5-10 images with variations

### Image Variations:
Include photos with:
- Different lighting conditions
- Slight angle variations
- Different expressions
- With/without glasses (if applicable)
- Different backgrounds

### Supported Formats:
- .jpg / .jpeg
- .png
- .bmp

## Usage:
After adding images, run:
```bash
python main.py db load data/known_faces
```

This will automatically create a face database from all the images in the subdirectories.