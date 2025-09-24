# 🤖 InsightFace Recognition System

A comprehensive, high-performance face recognition system built with InsightFace, featuring real-time detection, database management, interactive CLI, and ultra-fast webcam recognition optimized for maximum performance.

## 🚀 Key Features

### 🔍 **Advanced Face Detection & Analysis**
- **High-accuracy face detection** using InsightFace Buffalo models (L/M/S variants)
- **106-point facial landmarks** detection for detailed face analysis
- **Age and gender estimation** with confidence scores
- **Face quality scoring** and detection confidence metrics
- **Multi-face detection** in single images with bounding boxes
- **Facial landmark visualization** with multiple display styles

### 👤 **Intelligent Face Recognition**
- **Custom face database** creation and management
- **Ultra-fast real-time recognition** via webcam (60+ FPS optimized)
- **Face verification** (1:1 matching) with similarity scores
- **Face identification** (1:N matching) against database
- **Configurable similarity thresholds** for precision control
- **Background processing** with threading for smooth performance
- **Automatic photo capture** system (100 photos per person)

### 🗃️ **Comprehensive Database Management**
- **Persistent face database** with pickle serialization
- **Add/remove people** with multiple image support
- **Bulk import** from structured directories
- **Database statistics** and integrity verification
- **Export/backup** capabilities with JSON metadata
- **Smart deduplication** and face quality filtering

### 📊 **Interactive & CLI Interfaces**
- **Beautiful interactive CLI** with menu-driven interface
- **Comprehensive command-line tools** for all operations
- **Real-time performance metrics** and FPS monitoring
- **Photo capture wizard** with visual feedback
- **Progress indicators** and status displays
- **Multiple visualization styles** for facial landmarks

### ⚡ **Performance Optimizations**
- **Ultra-fast webcam processing** with frame skipping
- **Background threading** for non-blocking recognition
- **Optimized camera settings** for maximum FPS
- **Memory-efficient** face embedding storage
- **Configurable processing parameters** for speed vs accuracy

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+** (Recommended: Python 3.9-3.11)
- **pip package manager**
- **Webcam/Camera** for real-time features

### 📦 Quick Installation

1. **Navigate to project directory**
   ```bash
   cd /Users/abdulmoid/Desktop/face_recognition
   ```

2. **Create virtual environment** (Recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup project structure**
   ```bash
   python main.py setup
   ```

5. **Verify installation**
   ```bash
   python main.py info
   ```

## 🚀 Quick Start Guide

### 🎯 **Interactive Mode (Recommended for Beginners)**
```bash
# Launch the beautiful interactive CLI
python main.py interactive
# OR simply run:
python interactive_cli.py
```

The interactive CLI provides:
- **Menu-driven interface** with clear options
- **Real-time face detection** from existing database
- **Guided photo capture** (100 photos per person)
- **Database statistics** and management
- **Visual feedback** and progress indicators

### 1. **Run Demos & Tests**
```bash
# Run comprehensive demonstration
python main.py demo --type full

# Test face detection on specific image
python main.py demo --type detection --image data/test_images/test_trump.jpg

# Test face recognition against database
python main.py demo --type recognition --image path/to/image.jpg --database models/face_database.pkl

# Test face verification (compare two faces)
python main.py demo --type verification --image1 face1.jpg --image2 face2.jpg
```

### 2. **Build Your Face Database**
```bash
# Add person from directory of images
python main.py db add "John Doe" --directory path/to/john_images/

# Add person from specific image files
python main.py db add "Jane Smith" --images img1.jpg img2.jpg img3.jpg

# Load from structured directory (person_name/images...)
python main.py db load data/known_faces/

python main.py db list

# Remove person from database
python main.py db remove "Person Name"

# Database management
python main.py db verify      # Verify database integrity
python main.py db export      # Export database info
python main.py db backup     # Create backup
```

### 3. **Photo Capture System**
```bash
# Capture 100 photos for a new person (guided process)
python main.py capture-photos

# Capture photos for specific person
python main.py capture-photos --person-name "John Doe"

# Use custom output directory
python main.py capture-photos --output-dir my_photos/
```

### 4. **Real-time Recognition**
```bash
# Start ultra-fast webcam recognition
python main.py realtime

# Add new person via webcam (interactive)
python main.py add-person "New Person"

# Use custom recognition threshold
python main.py realtime --threshold 0.6

# Add person and show database stats
python main.py add-person "Jane" --stats
```

## 📁 Project Structure

```
face_recognition/
├── 📄 main.py                    # Main CLI entry point
├── 📄 interactive_cli.py         # Interactive menu-driven CLI
├── 📄 requirements.txt           # Python dependencies
├── 📁 src/                       # Source code modules
│   ├── 🧠 face_recognizer.py     # Core InsightFace recognition engine
│   ├── ⚡ ultra_fast_realtime.py # Ultra-optimized real-time recognition
│   ├── 📷 photo_capture.py       # 100-photo capture system
│   ├── 🗃️ database_manager.py    # Database operations & management
│   ├── 🎯 demo.py                # Demonstration scripts
│   └── 📁 add_person.py          # Person addition utilities
├── 📁 data/                      # Data storage
│   ├── 📁 known_faces/           # Training images (person_name/images)
│   ├── 📁 test_images/           # Test images for demos
│   └── 📁 captured_photos/       # Auto-captured photos
├── 📁 models/                    # Trained models & databases
│   └── 💾 face_database.pkl      # Serialized face database
├── 📁 results/                   # Output results & visualizations
└── 📚 Documentation Files
    ├── 📖 README.md              # This comprehensive guide
    ├── 📘 USAGE_GUIDE.md         # Detailed usage examples
    ├── 🔧 ADD_PERSON_GUIDE.md    # Person addition guide
    └── 📸 PHOTO_CAPTURE_GUIDE.md # Photo capture instructions
```

## 💡 Core Components Explained

### 🧠 **InsightFaceRecognizer** (`face_recognizer.py`)
- **Primary recognition engine** using InsightFace Buffalo models
- **Face detection** with 106-point landmarks
- **Embedding extraction** (512-dimensional vectors)
- **Database management** with pickle serialization
- **Age/gender estimation** and quality scoring
- **Similarity calculation** using cosine similarity

### ⚡ **UltraFastRealTimeFaceRecognition** (`ultra_fast_realtime.py`)
- **60+ FPS optimization** with threading and frame skipping
- **Background processing** for non-blocking recognition
- **Optimized camera settings** (MJPEG, reduced resolution)
- **Smart result caching** with confidence filtering
- **Performance monitoring** with FPS display

### 📷 **PhotoCapture** (`photo_capture.py`)
- **Automated 100-photo capture** with visual feedback
- **Person-specific directories** with clean naming
- **Real-time capture counter** and progress display
- **Quality feedback** during capture process
- **Integration with database** for seamless workflow

### 🗃️ **Database Manager** (`database_manager.py`)
- **Persistent storage** with pickle serialization
- **CRUD operations** (Create, Read, Update, Delete)
- **Bulk operations** and directory imports
- **Database integrity** verification and repair
- **Export/backup** functionality with metadata

## 🚀 Advanced Usage Examples

### 📊 **Database Operations**
```bash
# Comprehensive database management
python main.py db list                    # Show all people and face counts
python main.py db verify                  # Check database integrity
python main.py db export db_info.json    # Export metadata to JSON
python main.py db backup backup.pkl      # Create database backup

# Bulk operations
python main.py db load data/known_faces/  # Load from directory structure
python main.py db add "Team" --directory team_photos/ --recursive
```

### 🎯 **Recognition & Detection**
```bash
# Different recognition modes
python main.py demo --type recognition --image test.jpg --threshold 0.7
python main.py demo --type detection --save-results        # Save annotated images
python main.py demo --type verification --image1 a.jpg --image2 b.jpg

# Batch processing
python main.py batch-recognize --input-dir photos/ --output-dir results/
```

### ⚡ **Real-time Performance Tuning**
```bash
# Ultra-fast mode (optimized for speed)
python main.py realtime --fast-mode --threshold 0.3

# High-accuracy mode (optimized for precision) 
python main.py realtime --precision-mode --threshold 0.8

# Custom camera settings
python main.py realtime --camera 1 --resolution 640x480 --fps 30
```

### 📷 **Advanced Photo Capture**
```bash
# Batch photo capture for multiple people
python main.py capture-batch --people "John,Jane,Bob" --photos-per-person 100

# Quality-controlled capture
python main.py capture-photos --quality-check --min-confidence 0.8

# Custom capture settings
python main.py capture-photos --person-name "Alice" --resolution 1920x1080
```

## ⚙️ Configuration & Settings

### 🎛️ **Model Configuration**
The system supports different InsightFace models for various performance needs:

- **`buffalo_l`** (Default): Best accuracy, slower processing
- **`buffalo_m`**: Balanced accuracy/speed
- **`buffalo_s`**: Fastest processing, good accuracy

### 🎯 **Recognition Thresholds**
- **`0.3-0.4`**: Very permissive (good for difficult lighting)
- **`0.5-0.6`**: Balanced (recommended for most cases)
- **`0.7-0.8`**: Strict (high precision, may miss some matches)
- **`0.8+`**: Very strict (only very confident matches)

### 📊 **Performance Optimization**
```python
# In your code, you can customize:
recognizer = InsightFaceRecognizer(
    model_name='buffalo_l',     # Model selection
    ctx_id=0,                   # 0=CPU, >0=GPU
    det_size=(640, 640)         # Detection resolution
)
```

## 🔧 Troubleshooting

### 🚨 **Common Issues & Solutions**

#### **Camera not detected**
```bash
# Test different camera indices
python main.py realtime --camera 0  # Default
python main.py realtime --camera 1  # External camera
```

#### **Low recognition accuracy**
```bash
# Try lower threshold
python main.py realtime --threshold 0.3

# Add more training images
python main.py db add "Person" --directory more_photos/
```

#### **Slow performance**
```bash
# Use smaller model
python main.py realtime --model buffalo_s

# Enable fast mode
python main.py realtime --fast-mode
```

#### **Memory issues**
```bash
# Clear database and rebuild
python main.py db backup current_backup.pkl
python main.py db clear
python main.py db load data/known_faces/
```

### 🔍 **Debug Mode**
```bash
# Enable verbose logging
python main.py --debug realtime
python main.py --verbose db list
```

## 📋 Dependencies & Requirements

### 🐍 **Python Packages**
```
numpy==1.26.4           # Numerical computing
opencv-python==4.10.0.84 # Computer vision
onnxruntime==1.22.1     # ONNX model runtime
insightface==0.7.3      # Face recognition models
Pillow==10.4.0          # Image processing
matplotlib==3.9.2       # Plotting and visualization
scikit-learn==1.5.2     # Machine learning utilities
mxnet==1.9.1           # Deep learning framework
albumentations==1.4.16  # Image augmentation
tqdm==4.66.5           # Progress bars
```

### 💻 **System Requirements**
- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for models and databases
- **Camera**: USB webcam or built-in camera
- **OS**: Windows 10+, macOS 10.15+, Linux Ubuntu 18.04+

## 🤝 Contributing & Development

### 🛠️ **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd face_recognition

# Create development environment
python -m venv dev_env
source dev_env/bin/activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt  # If available
```

### 🧪 **Testing**
```bash
# Run basic functionality tests
python main.py demo --type full

# Test all components
python src/face_recognizer.py    # Test core recognition
python src/photo_capture.py      # Test photo capture
python interactive_cli.py        # Test interactive CLI
```

## 📜 License & Credits

### 🏆 **Built With**
- **[InsightFace](https://github.com/deepinsight/insightface)**: State-of-the-art face recognition
- **[OpenCV](https://opencv.org/)**: Computer vision library  
- **[NumPy](https://numpy.org/)**: Numerical computing
- **[scikit-learn](https://scikit-learn.org/)**: Machine learning utilities

### 👨‍💻 **Author**
**AI Assistant** - *September 2025*

### 🙏 **Acknowledgments**
- InsightFace team for the excellent face recognition models
- OpenCV community for computer vision tools
- Python community for the amazing ecosystem

## 📞 Support & Contact

### 🆘 **Getting Help**
1. **Check documentation**: Review this README and guide files
2. **Run diagnostics**: Use `python main.py info` and `python main.py --debug`
3. **Check examples**: Look at `USAGE_GUIDE.md` for detailed examples
4. **Test components**: Run individual modules to isolate issues

### 🐛 **Reporting Issues**
When reporting issues, please include:
- Python version (`python --version`)
- Operating system and version
- Complete error message or unexpected behavior
- Steps to reproduce the issue
- Camera/hardware information (for webcam issues)

---

**🎉 Happy Face Recognition!** 

*This system is designed to be powerful yet user-friendly. Whether you're a beginner using the interactive CLI or an advanced user leveraging the full API, you have everything needed for professional-grade face recognition applications.*

### Face Detection
```python
from src.face_recognizer import InsightFaceRecognizer

recognizer = InsightFaceRecognizer()
image = cv2.imread('path/to/image.jpg')

# Detect all faces in image
faces = recognizer.detect_faces(image)
for face in faces:
    print(f"Face detected with confidence: {face['score']:.3f}")
    print(f"Age: {face.get('age', 'Unknown')}")
    print(f"Gender: {'Male' if face.get('gender') == 1 else 'Female'}")
```

### Face Recognition
```python
# Add faces to database
recognizer.add_face_to_database('john1.jpg', 'John Doe')
recognizer.add_face_to_database('john2.jpg', 'John Doe')

# Recognize faces in new image
results = recognizer.recognize_face(test_image, threshold=0.5)
for result in results:
    print(f"Recognized: {result['name']} (confidence: {result['confidence']:.3f})")
```

### Face Verification
```python
# Verify if two images contain same person
result = recognizer.verify_faces(image1, image2)
print(f"Same person: {result['verified']}")
print(f"Similarity: {result['similarity']:.4f}")
```

## Command Line Interface

### Demo Commands
```bash
# Full demo with all features
python main.py demo --type full

# Face detection demo
python main.py demo --type detection --image test.jpg

# Face recognition demo  
python main.py demo --type recognition --image test.jpg

# Face verification demo
python main.py demo --type verification --image1 person1.jpg --image2 person2.jpg
```

### Database Management
```bash
# Add person from directory
python main.py db add "Person Name" --directory /path/to/images/

# Add person from specific images
python main.py db add "Person Name" --images img1.jpg img2.jpg

# Remove person from database
python main.py db remove "Person Name"

# List all people
python main.py db list

# Load from structured directory
python main.py db load /path/to/structured/directory/

# Export database information
python main.py db export database_info.json

# Verify database integrity
python main.py db verify

# Backup database
python main.py db backup backup.pkl
```

### Real-time Recognition
```bash
# Start real-time recognition
python main.py realtime

# Add person via webcam
python main.py realtime --add-person "New Person"

# Custom settings
python main.py realtime --threshold 0.6 --camera 1 --database custom_db.pkl
```

## Advanced Configuration

### Model Selection
```python
# Different InsightFace models
recognizer = InsightFaceRecognizer(model_name='buffalo_l')  # High accuracy
recognizer = InsightFaceRecognizer(model_name='buffalo_m')  # Balanced
recognizer = InsightFaceRecognizer(model_name='buffalo_s')  # Fast
```

### GPU Acceleration
```python
# Use GPU if available
recognizer = InsightFaceRecognizer(ctx_id=0)  # GPU 0
recognizer = InsightFaceRecognizer(ctx_id=-1) # CPU only
```

### Custom Detection Size
```python
# Larger detection size for better accuracy
recognizer = InsightFaceRecognizer(det_size=(640, 640))
```

## Performance Tips

### Image Quality
- Use clear, front-facing photos
- Good lighting conditions
- Minimal blur or motion
- Face should be at least 112x112 pixels

### Database Optimization
- Add multiple images per person (3-5 recommended)
- Include variations in lighting and angles
- Remove poor quality images
- Regular database verification

### Recognition Accuracy
- Adjust threshold based on your use case:
  - High security: threshold = 0.7+
  - Balanced: threshold = 0.5-0.6
  - High recall: threshold = 0.3-0.4

## Troubleshooting

### Common Issues

1. **Import errors**
   ```bash
   # Make sure you're in the project directory
   cd /path/to/face_recognition
   
   # Install requirements
   pip install -r requirements.txt
   ```

2. **No faces detected**
   - Check image quality and lighting
   - Ensure face is clearly visible
   - Try different detection sizes

3. **Poor recognition accuracy**
   - Add more training images per person
   - Improve image quality
   - Adjust recognition threshold
   - Verify database integrity

4. **Camera not working**
   ```bash
   # Try different camera index
   python main.py realtime --camera 1
   ```

### Error Messages

- `"No face detected"`: Image quality issue or no faces in image
- `"Database file not found"`: Run database setup first
- `"Could not open camera"`: Check camera permissions and availability

## Dependencies

- **insightface**: Core face recognition library
- **opencv-python**: Image processing and webcam access
- **numpy**: Numerical computations
- **scikit-learn**: Similarity calculations
- **matplotlib**: Visualization
- **Pillow**: Additional image support

## Model Information

This project uses InsightFace models which are:
- Pre-trained on large-scale face datasets
- Optimized for accuracy and speed
- Support various face analysis tasks
- Available in different sizes (buffalo_s/m/l)

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## License

This project is for educational and research purposes. Please respect InsightFace licensing terms.

## Support

For issues and questions:
1. Check this README and troubleshooting section
2. Verify your installation and setup
3. Test with provided demo images first
4. Check InsightFace documentation for model-specific issues

---

**Happy Face Recognition! 🎯**