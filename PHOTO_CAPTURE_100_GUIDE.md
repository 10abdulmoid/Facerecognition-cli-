# Photo Capture Script - 100 Photos with Counter

This script captures exactly 100 photos of a person from your webcam, with real-time counter display and organized file naming.

## ✨ Features

🎯 **Exactly 100 Photos** - Automatically stops after capturing 100 photos  
📊 **Real-time Counter** - Large, prominent counter showing progress (X/100)  
👤 **Person-based Organization** - Creates directories and filenames based on person's name  
🎮 **Simple Controls** - Only press 'c' to capture, 'q' to quit  
📱 **Progress Display** - Shows percentage complete and photos remaining  
📁 **Smart File Naming** - Files named as `PersonName_001.jpg` to `PersonName_100.jpg`  

## 🚀 Quick Start

### Method 1: Interactive (Recommended)
```bash
# Script will ask for person's name
python main.py capture-photos
```

### Method 2: Pre-specify Name
```bash
# Provide name directly
python main.py capture-photos --person-name "John Doe"
```

### Method 3: Direct Script
```bash
cd src/
python photo_capture.py --person-name "Alice Smith"
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `c` | **Capture photo** (only way to take photos) |
| `q` or `ESC` | **Quit early** (before reaching 100 photos) |

## 📊 On-Screen Display

The webcam feed shows:

### Status Panel (Top Left)
- **Person**: Name being captured
- **Photos**: Current count (e.g., "Photos: 47/100")  
- **Progress**: Percentage complete (e.g., "Progress: 47.0%")
- **Instructions**: Reminder to press 'C'

### Large Counter (Top Right)
- **Big numbers**: "47/100" in large, green text
- **Status indicator**: "READY" or "COMPLETE!" when done

### Capture Feedback
- **"CAPTURED!"** message when photo is taken
- **"X more to go!"** showing remaining photos
- **"COMPLETE!"** when all 100 photos are captured

## 📁 File Organization

### Directory Structure
```
captured_photos/
└── Person_Name/
    ├── Person_Name_001.jpg
    ├── Person_Name_002.jpg
    ├── Person_Name_003.jpg
    ├── ...
    ├── Person_Name_099.jpg
    └── Person_Name_100.jpg
```

### Name Cleaning
- Spaces become underscores: "John Doe" → "John_Doe"
- Special characters removed: "Mary-Jane!" → "Mary-Jane"
- Numbers preserved: "User123" → "User123"

## 📸 Example Session

```bash
$ python main.py capture-photos

=== Photo Capture Setup ===
Enter the person's name: Alice Cooper

=== Starting Photo Capture Session ===
Person: Alice Cooper
Target: 100 photos

Photos will be saved to: /path/to/captured_photos/Alice_Cooper
Target: 100 photos for Alice Cooper

=== Photo Capture Session Started for Alice Cooper ===
Instructions:
- Press 'c' to capture a photo
- Press 'q' or 'ESC' to quit early
- Target: 100 photos

Ready to capture photos!

✓ Captured 1/100: Alice_Cooper_001.jpg
  → 99 more photos needed
✓ Captured 2/100: Alice_Cooper_002.jpg
  → 98 more photos needed
...
✓ Captured 99/100: Alice_Cooper_099.jpg
  → 1 more photos needed
✓ Captured 100/100: Alice_Cooper_100.jpg
  → 🎉 ALL 100 PHOTOS COMPLETE!

🎉 TARGET REACHED! Captured all 100 photos!

=== Session Complete ===
Photos captured: 100/100
Photos saved in: /path/to/captured_photos/Alice_Cooper

🎉 Session completed!
📊 Captured: 100/100 photos (100.0%)
📁 Location: /path/to/captured_photos/Alice_Cooper

✅ SUCCESS: All 100 photos captured!
```

## 🎯 Usage Scenarios

### 1. Building Face Recognition Dataset
```bash
python main.py capture-photos --person-name "Training Subject"
# Creates 100 photos for machine learning training
```

### 2. Family Photo Collection
```bash
python main.py capture-photos --person-name "Mom"
python main.py capture-photos --person-name "Dad"  
python main.py capture-photos --person-name "Sister"
# Organized family photo collection
```

### 3. Profile Picture Session  
```bash
python main.py capture-photos --person-name "Professional_Headshots"
# 100 shots to choose the best profile picture
```

### 4. Documentation/ID Photos
```bash
python main.py capture-photos --person-name "ID_Photos_2024"
# Systematic photo documentation
```

## 💡 Tips for Best Results

### 📷 Camera Positioning
- **Eye level**: Position camera at your eye level
- **Arm's length**: Sit about 2-3 feet from camera
- **Stable setup**: Ensure camera doesn't move during session

### 💡 Lighting  
- **Natural light**: Best results near a window
- **Even lighting**: Avoid harsh shadows
- **No backlighting**: Don't sit with light behind you

### 🎭 Variety for Best Dataset
- **Different angles**: Slight head turns left/right
- **Different expressions**: Smile, neutral, serious
- **Different distances**: Lean slightly closer/farther
- **Eye direction**: Look at camera, slightly left/right

### ⏰ Session Management
- **Take breaks**: Pause every 25-30 photos to avoid fatigue
- **Stay consistent**: Try to maintain similar posture
- **Good pace**: Don't rush - quality over speed

## 🔧 Technical Details

### File Specifications
- **Format**: JPEG (.jpg)
- **Resolution**: 1280x720 (HD)
- **Size**: ~150-200KB per photo
- **Total size**: ~15-20MB for 100 photos

### Naming Convention
- **Pattern**: `{PersonName}_{Number:003}.jpg`
- **Example**: `John_Doe_001.jpg`, `John_Doe_002.jpg`, etc.
- **Zero-padded**: Numbers always 3 digits (001, 002, ..., 100)

## 🚨 Troubleshooting

### Camera Issues
- **"Could not open camera"**: Try `--camera 1` for different camera
- **Poor quality**: Check lighting and camera focus
- **Lag**: Close other applications using camera

### File Issues  
- **"Permission denied"**: Check write permissions for directory
- **"Disk full"**: Need ~20MB free space for 100 photos
- **Name conflicts**: Script creates unique directories per person

### Session Issues
- **Stopped early**: Check terminal output for error messages
- **Counter not updating**: Ensure 'c' key is being pressed (not spacebar)
- **Photos blurry**: Improve lighting and hold steady when pressing 'c'

## 🔄 Integration with Face Recognition

After capturing 100 photos, you can:

### 1. Select Best Photos
```bash
# Review the 100 photos and select 5-10 best ones
# Copy selected photos to face recognition directory
cp captured_photos/Alice_Cooper/Alice_Cooper_042.jpg data/known_faces/Alice/
cp captured_photos/Alice_Cooper/Alice_Cooper_067.jpg data/known_faces/Alice/
# ... select more
```

### 2. Add to Face Recognition Database
```bash
python main.py db add "Alice" --directory data/known_faces/Alice/
```

### 3. Test Recognition
```bash
python main.py realtime --database models/face_database.pkl
```

## 📋 Command Reference

```bash
# Interactive mode (asks for name)
python main.py capture-photos

# Specify person name
python main.py capture-photos --person-name "Person Name"

# Custom output directory
python main.py capture-photos --output-dir "my_photos" --person-name "John"

# Different camera
python main.py capture-photos --camera 1 --person-name "User"

# Direct script usage
cd src/
python photo_capture.py --person-name "Direct User"
```

Your photo capture system is ready to systematically collect 100 high-quality photos! 📸✨