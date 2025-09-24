# Test Images Directory

Place test images here for testing face recognition.

## Purpose:
- Images to test recognition against your database
- Can contain multiple people
- Used for demonstration and validation

## Usage:
```bash
# Test recognition on a specific image
python main.py demo --type recognition --image data/test_images/your_image.jpg

# Test face detection
python main.py demo --type detection --image data/test_images/group_photo.jpg
```

## Tips:
- Include both individual photos and group photos
- Mix of people in your database and unknown people
- Various lighting and angle conditions
- Good for testing recognition accuracy