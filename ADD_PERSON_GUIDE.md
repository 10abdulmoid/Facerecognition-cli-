# Add Person to Face Recognition Database

This guide explains how to add new people to your face recognition database using the webcam.

## Quick Start

### Method 1: Using Main Script (Recommended)
```bash
# Add a new person named "John Doe"
python main.py add-person "John Doe"

# Add person with custom database location
python main.py add-person "Jane Smith" --database models/face_database.pkl

# Add person and show database statistics afterward
python main.py add-person "Mike Johnson" --stats

# Use a different camera (if you have multiple cameras)
python main.py add-person "Sarah Wilson" --camera 1
```

### Method 2: Using Direct Script
```bash
cd src/
python add_person.py "Person Name"
```

## How It Works

1. **Start the script** with the person's name as a command-line argument
2. **Position your face** clearly in the webcam frame
3. **Capture multiple photos** by pressing 'c' when your face is detected
4. **Save to database** by pressing 's' when you're done capturing
5. **The system automatically**:
   - Creates a directory for the person in `data/known_faces/`
   - Saves captured images with timestamps
   - Extracts face embeddings and adds them to the database
   - Shows success confirmation

## Controls During Capture

| Key | Action |
|-----|--------|
| `c` | Capture current frame (only when face is detected) |
| `s` | Save all captured photos to database and finish |
| `q` | Quit without saving anything |

## Visual Feedback

- **Green box**: Face detected and ready to capture
- **Red text**: No face detected - position yourself better
- **"CAPTURED!" message**: Photo successfully captured
- **Counter**: Shows how many photos you've captured

## Tips for Best Results

1. **Good Lighting**: Ensure your face is well-lit
2. **Multiple Angles**: Capture 3-5 photos from slightly different angles
3. **Clear Face**: Make sure your face is clearly visible and unobstructed
4. **Stable Position**: Keep your face steady when capturing
5. **Direct Gaze**: Look directly at the camera for at least one photo

## Example Session

```bash
$ python main.py add-person "Alice Cooper"

=== Face Recognition Database - Add Person ===
Person to add: Alice Cooper
Database path: models/face_database.pkl
Camera index: 0

Loaded existing database with 1 faces

=== Database Statistics ===
Total people: 1
Total faces: 144

Faces per person:
  Trump: 144 samples

=== Adding Alice Cooper to database ===
Instructions:
- Position your face clearly in the frame
- Press 'c' to capture a photo
- Press 'q' to quit without saving
- You can capture multiple photos for better recognition
- Press 's' when you're done capturing photos

Press any key to start the webcam feed...

✓ Captured photo 1: Alice Cooper_20250924_143022_1.jpg
✓ Captured photo 2: Alice Cooper_20250924_143025_2.jpg
✓ Captured photo 3: Alice Cooper_20250924_143028_3.jpg

=== Processing 3 captured images ===
✓ Added Alice Cooper_20250924_143022_1.jpg to database
✓ Added Alice Cooper_20250924_143025_2.jpg to database
✓ Added Alice Cooper_20250924_143028_3.jpg to database

✓ Database saved to models/face_database.pkl
✓ Successfully added Alice Cooper with 3 face samples!

🎉 Successfully added Alice Cooper to the database!

You can now test recognition with:
python main.py realtime --database models/face_database.pkl
```

## After Adding a Person

Once you've successfully added someone to the database, you can:

1. **Test recognition** with any of the real-time modes:
   ```bash
   python main.py realtime --database models/face_database.pkl
   python main.py fastrealtime --database models/face_database.pkl
   python main.py ultrafast --database models/face_database.pkl
   ```

2. **Check database statistics**:
   ```bash
   python main.py db list
   ```

3. **Test with a static image**:
   ```bash
   python main.py demo --type recognition --image path/to/test/image.jpg --database models/face_database.pkl
   ```

## Troubleshooting

### "No face detected"
- Ensure good lighting
- Move closer to the camera
- Make sure your face is clearly visible
- Check if the camera is working properly

### "Failed to add to database"
- Make sure the models directory exists
- Check that you have write permissions
- Ensure the face was properly detected in the captured images

### Camera not opening
- Try a different camera index: `--camera 1`
- Make sure no other application is using the camera
- Check camera permissions on your system

### Low quality recognition
- Add more photos of the person (3-5 recommended)
- Ensure photos are clear and well-lit
- Try different angles and expressions
- Consider adjusting the recognition threshold when testing

## File Structure

After adding a person, you'll see:

```
face_recognition/
├── data/
│   └── known_faces/
│       └── Alice Cooper/
│           ├── Alice Cooper_20250924_143022_1.jpg
│           ├── Alice Cooper_20250924_143025_2.jpg
│           └── Alice Cooper_20250924_143028_3.jpg
└── models/
    └── face_database.pkl  # Updated with new person
```