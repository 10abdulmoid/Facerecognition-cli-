# Photo Capture Guide

This guide explains how to use the webcam photo capture tool to take and organize photos.

## Quick Start

### Method 1: Using Main Script (Recommended)
```bash
# Capture photos to default directory (captured_photos/)
python main.py capture-photos

# Capture photos for a specific person (creates subdirectory)
python main.py capture-photos --person-name "John Doe"

# Capture photos to custom directory
python main.py capture-photos --output-dir "my_photos"

# Use different camera (if you have multiple cameras)
python main.py capture-photos --camera 1
```

### Method 2: Using Direct Script
```bash
cd src/
python photo_capture.py --person-name "Person Name"
```

## Features

✅ **High-quality capture** - 1280x720 resolution by default  
✅ **Visual guidelines** - Rule of thirds grid and corner markers  
✅ **Real-time feedback** - Photo counter and status display  
✅ **Organized storage** - Automatic directory creation with timestamps  
✅ **Multiple camera support** - Choose which camera to use  
✅ **Fullscreen mode** - Toggle fullscreen for better framing  
✅ **Instant capture feedback** - Visual confirmation when photo is taken  

## Controls During Capture

| Key | Action |
|-----|--------|
| `SPACE` or `c` | Capture photo |
| `q` or `ESC` | Quit capture session |
| `r` | Toggle guidelines on/off |
| `f` | Toggle fullscreen mode |

## Visual Aids

### Guidelines (Press 'r' to toggle)
- **Rule of thirds grid**: Helps with photo composition
- **Center point**: For centered shots
- **Corner markers**: Frame boundaries
- **Grid lines**: Professional composition guide

### Status Display
- **Photo counter**: Shows how many photos you've captured
- **Controls reminder**: Key combinations displayed
- **Ready indicator**: Shows camera is ready
- **Capture feedback**: "CAPTURED!" confirmation

## File Organization

### Default Structure
```
captured_photos/
├── photo_20250924_143022_001.jpg
├── photo_20250924_143025_002.jpg
└── photo_20250924_143028_003.jpg
```

### With Person Name
```bash
python main.py capture-photos --person-name "Alice Cooper"
```
Creates:
```
captured_photos/
└── Alice_Cooper/
    ├── photo_20250924_143022_001.jpg
    ├── photo_20250924_143025_002.jpg
    └── photo_20250924_143028_003.jpg
```

### Custom Directory
```bash
python main.py capture-photos --output-dir "family_photos" --person-name "Dad"
```
Creates:
```
family_photos/
└── Dad/
    ├── photo_20250924_143022_001.jpg
    ├── photo_20250924_143025_002.jpg
    └── photo_20250924_143028_003.jpg
```

## Example Session

```bash
$ python main.py capture-photos --person-name "Alice"

=== Webcam Photo Capture ===
Output directory: captured_photos/Alice
Camera: 0
Creating photos for: Alice
Photos will be saved to: /Users/username/face_recognition/captured_photos/Alice

=== Photo Capture Session Started ===
Instructions:
- Press 'SPACE' or 'c' to capture a photo
- Press 'q' or 'ESC' to quit
- Press 'r' to show/hide guidelines
- Press 'f' to toggle fullscreen

Ready to capture photos!

✓ Captured: photo_20250924_143022_001.jpg
✓ Captured: photo_20250924_143025_002.jpg
✓ Captured: photo_20250924_143028_003.jpg
Guidelines: OFF
✓ Captured: photo_20250924_143032_004.jpg
Ending capture session...

=== Session Complete ===
Total photos captured: 4
Photos saved in: /Users/username/face_recognition/captured_photos/Alice

🎉 Successfully captured 4 photos!
📁 Location: /Users/username/face_recognition/captured_photos/Alice

📸 Captured files:
  - photo_20250924_143022_001.jpg
  - photo_20250924_143025_002.jpg
  - photo_20250924_143028_003.jpg
  - photo_20250924_143032_004.jpg
```

## Tips for Best Photos

### Lighting
- **Natural light** is best - sit near a window
- **Avoid backlighting** - don't sit with light behind you
- **Even lighting** - avoid harsh shadows on face
- **Soft light** - diffused lighting works better than direct

### Positioning
- **Eye level** - camera should be at your eye level
- **Arm's length** - sit about arm's length from camera
- **Centered** - use the center point guide
- **Rule of thirds** - for more artistic shots, use grid lines

### Technical
- **Hold still** - stay steady when capturing
- **Multiple angles** - capture from different angles
- **Good background** - clean, uncluttered background
- **Camera stability** - ensure your camera/laptop is stable

## Use Cases

### 1. Personal Photo Collection
```bash
python main.py capture-photos --output-dir "my_photos"
```

### 2. Family Album
```bash
python main.py capture-photos --person-name "Mom" --output-dir "family"
python main.py capture-photos --person-name "Dad" --output-dir "family"
python main.py capture-photos --person-name "Sister" --output-dir "family"
```

### 3. Profile Pictures
```bash
python main.py capture-photos --person-name "ProfilePics" --output-dir "social_media"
```

### 4. Document Photos
```bash
python main.py capture-photos --output-dir "documents"
# Good for capturing documents, whiteboards, etc.
```

## Integration with Face Recognition

After capturing photos, you can use them with the face recognition system:

### 1. Manual Database Addition
```bash
# Copy photos to known_faces directory
cp captured_photos/Alice/* data/known_faces/Alice/

# Rebuild database
python main.py db add "Alice" --directory data/known_faces/Alice/
```

### 2. Direct Addition (Alternative workflow)
```bash
# Capture photos first
python main.py capture-photos --person-name "Alice"

# Then manually move best photos to face recognition directory
# Select 3-5 best, clear photos and copy them
```

## Troubleshooting

### Camera Issues
- **"Could not open camera"**: Try different camera index (`--camera 1`)
- **Poor quality**: Check camera resolution settings
- **Lag**: Close other applications using the camera

### File Issues
- **Permission denied**: Check write permissions for output directory
- **Disk space**: Ensure enough space for photos (each ~200KB-2MB)

### Display Issues
- **Window too small**: Press 'f' for fullscreen
- **Guidelines not visible**: Press 'r' to toggle
- **Blurry preview**: Check camera focus and lighting

## Advanced Usage

### Batch Capture for Multiple People
```bash
#!/bin/bash
# Script to capture photos for multiple people

people=("Alice" "Bob" "Charlie" "Diana")

for person in "${people[@]}"; do
    echo "Capturing photos for $person"
    python main.py capture-photos --person-name "$person"
    echo "Press Enter when ready for next person..."
    read
done
```

### Custom Resolution (Modify script)
Edit `photo_capture.py` line 32-33:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)   # 1080p
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
```

The photo capture tool is now ready to use! 📸