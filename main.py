#!/usr/bin/env python3
"""
InsightFace Recognition Project
A comprehensive face recognition system using InsightFace

Author: AI Assistant
Date: September 2025
"""

import sys
import os
from pathlib import Path
import argparse

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.append(str(src_dir))

from face_recognizer import InsightFaceRecognizer
from database_manager import FaceDatabaseManager
from demo import FaceRecognitionDemo

def print_banner():
    """Print project banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                 InsightFace Recognition System               ║
    ║                                                              ║
    ║  A comprehensive face recognition project using InsightFace  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """Print detailed help information."""
    help_text = """
Available Commands:

🚀 QUICK START (Interactive Mode):
   python main.py interactive                       # Interactive CLI menu

1. Demo Commands:
   python main.py demo --type full                    # Run full demo
   python main.py demo --type detection --image path/to/image.jpg
   python main.py demo --type recognition --image path/to/image.jpg
   python main.py demo --type verification --image1 path1 --image2 path2

2. Database Management:
   python main.py db list                           # List all people in database
   python main.py db add "Person Name" --directory path/to/person/images
   python main.py db add "Person Name" --images img1.jpg img2.jpg
   python main.py db remove "Person Name"
   python main.py db load path/to/structured/directory
   python main.py db export database_info.json
   python main.py db verify
   python main.py db backup backup_file.pkl

3. Real-time Recognition:
   python main.py realtime                          # Start webcam recognition
   python main.py realtime --add-person "Name"     # Add person via webcam
   python main.py realtime --threshold 0.6         # Custom threshold
   python main.py add-person "John Doe"             # Add new person via webcam
   python main.py add-person "Jane" --stats         # Add person and show stats

4. Photo Capture (100 photos with counter):
   python main.py capture-photos                    # Will ask for person name
   python main.py capture-photos --person-name "John"  # Capture 100 photos for John
   python main.py capture-photos --output-dir my_photos  # Custom base directory

5. Project Setup:
   python main.py setup                            # Setup project structure
   python main.py info                             # Show project information

Example Workflow:
1. python main.py setup                            # Initial setup
2. python main.py demo                             # Run demo to test
3. python main.py db add "John Doe" --directory john_images/
4. python main.py realtime                         # Start recognition

For detailed help on any command, add --help after the command.
    """
    print(help_text)

def setup_project():
    """Setup project directories and sample files."""
    print("Setting up project structure...")
    
    base_dir = Path.cwd()
    
    # Create directories
    directories = [
        "data/known_faces",
        "data/test_images", 
        "models",
        "results",
        "src"
    ]
    
    for dir_path in directories:
        (base_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Create sample README for data directories
    readme_content = """# Face Recognition Data Directory

## Structure:
- known_faces/: Store images of people to recognize
  - person1/: Images of person1
  - person2/: Images of person2
  - ...

- test_images/: Images for testing recognition

## Tips:
1. Use clear, front-facing photos for best results
2. Multiple images per person improve accuracy
3. Good lighting and image quality are important
4. Supported formats: .jpg, .jpeg, .png, .bmp
"""
    
    with open(base_dir / "data" / "README.md", "w") as f:
        f.write(readme_content)
    
    print("Project structure created successfully!")
    print("\nNext steps:")
    print("1. Add face images to data/known_faces/person_name/")
    print("2. Add test images to data/test_images/")
    print("3. Run: python main.py demo")

def show_project_info():
    """Show project information and status."""
    print_banner()
    
    print("Project Status:")
    print("=" * 40)
    
    # Check dependencies
    try:
        import insightface
        print(f"✓ InsightFace: {insightface.__version__}")
    except ImportError:
        print("✗ InsightFace: Not installed")
    
    try:
        import cv2
        print(f"✓ OpenCV: {cv2.__version__}")
    except ImportError:
        print("✗ OpenCV: Not installed")
    
    # Check project structure
    base_dir = Path.cwd()
    required_dirs = ["data", "models", "results", "src"]
    
    print("\nProject Structure:")
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        status = "✓" if dir_path.exists() else "✗"
        print(f"{status} {dir_name}/")
    
    # Check database
    db_path = base_dir / "models" / "face_database.pkl"
    if db_path.exists():
        try:
            manager = FaceDatabaseManager(str(db_path))
            stats = manager.recognizer.get_database_stats()
            print(f"\nDatabase Status:")
            print(f"✓ Database exists with {stats['total_people']} people")
        except Exception as e:
            print(f"✗ Database exists but has issues: {e}")
    else:
        print(f"\n✗ No face database found")
    
    print(f"\nFor help, run: python main.py --help")

def main():
    """Main entry point for the face recognition project."""
    parser = argparse.ArgumentParser(
        description='InsightFace Recognition System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    demo_parser.add_argument('--type', choices=['full', 'detection', 'recognition', 'verification'],
                            default='full', help='Type of demo')
    demo_parser.add_argument('--image', help='Test image path')
    demo_parser.add_argument('--image1', help='First image for verification')
    demo_parser.add_argument('--image2', help='Second image for verification')
    demo_parser.add_argument('--database', help='Database file path')
    
    # Database command
    db_parser = subparsers.add_parser('db', help='Database management')
    db_subparsers = db_parser.add_subparsers(dest='db_action')
    
    # Database subcommands
    list_parser = db_subparsers.add_parser('list', help='List people in database')
    
    add_parser = db_subparsers.add_parser('add', help='Add person to database')
    add_parser.add_argument('name', help='Person name')
    add_parser.add_argument('--directory', help='Directory with person images')
    add_parser.add_argument('--images', nargs='+', help='Image file paths')
    
    remove_parser = db_subparsers.add_parser('remove', help='Remove person')
    remove_parser.add_argument('name', help='Person name')
    
    load_parser = db_subparsers.add_parser('load', help='Load from directory structure')
    load_parser.add_argument('directory', help='Root directory')
    
    export_parser = db_subparsers.add_parser('export', help='Export database info')
    export_parser.add_argument('output', help='Output JSON file')
    
    verify_parser = db_subparsers.add_parser('verify', help='Verify database integrity')
    
    backup_parser = db_subparsers.add_parser('backup', help='Backup database')
    backup_parser.add_argument('backup_path', help='Backup file path')
    
    # Real-time command
    rt_parser = subparsers.add_parser('realtime', help='Real-time recognition')
    rt_parser.add_argument('--add-person', help='Add person via webcam')
    rt_parser.add_argument('--threshold', type=float, default=0.5, help='Recognition threshold')
    rt_parser.add_argument('--camera', type=int, default=0, help='Camera index')
    rt_parser.add_argument('--database', help='Database file path')
    
    # Fast real-time command
    fast_rt_parser = subparsers.add_parser('fastrealtime', help='High-performance real-time recognition')
    fast_rt_parser.add_argument('--threshold', type=float, default=0.25, help='Recognition threshold')
    fast_rt_parser.add_argument('--camera', type=int, default=0, help='Camera index')
    fast_rt_parser.add_argument('--database', help='Database file path')
    
    # Ultra-fast real-time command
    ultra_fast_rt_parser = subparsers.add_parser('ultrafast', help='Ultra high-performance real-time recognition')
    ultra_fast_rt_parser.add_argument('--threshold', type=float, default=0.2, help='Recognition threshold')
    ultra_fast_rt_parser.add_argument('--camera', type=int, default=0, help='Camera index')
    ultra_fast_rt_parser.add_argument('--database', help='Database file path')
    
    # Add person command
    add_person_parser = subparsers.add_parser('add-person', help='Add new person to database via webcam')
    add_person_parser.add_argument('person_name', help='Name of the person to add')
    add_person_parser.add_argument('--database', default='models/face_database.pkl', help='Database file path')
    add_person_parser.add_argument('--camera', type=int, default=0, help='Camera index')
    add_person_parser.add_argument('--stats', action='store_true', help='Show database statistics after adding')
    
    # Photo capture command
    photo_parser = subparsers.add_parser('capture-photos', help='Capture photos from webcam')
    photo_parser.add_argument('--output-dir', default='captured_photos', help='Directory to save photos')
    photo_parser.add_argument('--camera', type=int, default=0, help='Camera index')
    photo_parser.add_argument('--person-name', help='Person name (creates subdirectory)')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Setup project structure')
    
    # Info command  
    info_parser = subparsers.add_parser('info', help='Show project information')
    
    # Interactive CLI command
    interactive_parser = subparsers.add_parser('interactive', help='Launch interactive CLI menu')
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        print_help()
        return
    
    # Execute commands
    try:
        if args.command == 'demo':
            demo = FaceRecognitionDemo(args.database)
            
            if args.type == 'full':
                demo.run_full_demo(args.image)
            elif args.type == 'detection':
                if args.image:
                    demo.demo_face_detection(args.image)
                else:
                    print("Please provide --image for detection demo")
            elif args.type == 'recognition':
                if args.image:
                    demo.demo_face_recognition(args.image)
                else:
                    print("Please provide --image for recognition demo")
            elif args.type == 'verification':
                if args.image1 and args.image2:
                    demo.demo_face_verification(args.image1, args.image2)
                else:
                    print("Please provide --image1 and --image2 for verification demo")
        
        elif args.command == 'db':
            database_path = "models/face_database.pkl"
            manager = FaceDatabaseManager(database_path)
            
            if args.db_action == 'list':
                manager.list_people()
            elif args.db_action == 'add':
                if args.directory:
                    added = manager.add_person_from_directory(args.name, args.directory)
                elif args.images:
                    added = manager.add_person_from_images(args.name, args.images)
                else:
                    print("Please specify --directory or --images")
                    return
                print(f"Added {added} faces for {args.name}")
                manager.save_database()
            elif args.db_action == 'remove':
                if manager.remove_person(args.name):
                    manager.save_database()
            elif args.db_action == 'load':
                loaded = manager.load_from_structured_directory(args.directory)
                print(f"Loaded {loaded} faces")
                manager.save_database()
            elif args.db_action == 'export':
                manager.export_database_info(args.output)
            elif args.db_action == 'verify':
                manager.verify_database_integrity()
            elif args.db_action == 'backup':
                if os.path.exists(manager.database_path):
                    manager.backup_database(args.backup_path)
                else:
                    print("No database file found")
        
        elif args.command == 'realtime':
            # Import here to avoid issues if opencv not available
            sys.path.append(str(Path(__file__).parent / 'src'))
            from realtime_recognition import RealTimeFaceRecognition
            
            rt_system = RealTimeFaceRecognition(args.database, args.threshold)
            
            if args.add_person:
                rt_system.add_person_interactively(args.add_person)
                database_path = args.database or "models/face_database.pkl"
                rt_system.recognizer.save_database(database_path)
            else:
                rt_system.run_webcam_recognition(args.camera)
        
        elif args.command == 'fastrealtime':
            # Import here to avoid issues if opencv not available
            sys.path.append(str(Path(__file__).parent / 'src'))
            from fast_realtime_recognition import FastRealTimeFaceRecognition
            
            fast_rt_system = FastRealTimeFaceRecognition(args.database, args.threshold)
            fast_rt_system.run_webcam_recognition(args.camera)
        
        elif args.command == 'ultrafast':
            # Import here to avoid issues if opencv not available
            sys.path.append(str(Path(__file__).parent / 'src'))
            from ultra_fast_realtime import UltraFastRealTimeFaceRecognition
            
            ultra_fast_rt_system = UltraFastRealTimeFaceRecognition(args.database, args.threshold)
            ultra_fast_rt_system.run_webcam_recognition(args.camera)
        
        elif args.command == 'add-person':
            # Import here to avoid issues if opencv not available
            sys.path.append(str(Path(__file__).parent / 'src'))
            from add_person import PersonAdder
            
            adder = PersonAdder(args.database)
            success = adder.add_person_to_database(args.person_name, args.camera)
            
            if success:
                print(f"\n🎉 Successfully added {args.person_name} to the database!")
                if args.stats:
                    adder.show_database_stats()
                print(f"\nYou can now test recognition with:")
                print(f"python main.py realtime --database {args.database}")
            else:
                print(f"\n❌ Failed to add {args.person_name} to database")
        
        elif args.command == 'capture-photos':
            # Import here to avoid issues if opencv not available
            sys.path.append(str(Path(__file__).parent / 'src'))
            from photo_capture import PhotoCapture
            
            # Get person name if not provided
            person_name = args.person_name
            if not person_name:
                print("=== Photo Capture Setup ===")
                person_name = input("Enter the person's name: ").strip()
                
                if not person_name:
                    print("Error: Person name cannot be empty")
                    return
            
            print(f"\n=== Starting Photo Capture Session ===")
            print(f"Person: {person_name}")
            print(f"Target: 100 photos")
            
            capturer = PhotoCapture(person_name, args.output_dir, args.camera)
            success = capturer.start_capture_session()
            
            if success and capturer.photo_count > 0:
                completion_rate = (capturer.photo_count / capturer.target_photos) * 100
                print(f"\n🎉 Session completed!")
                print(f"📊 Captured: {capturer.photo_count}/{capturer.target_photos} photos ({completion_rate:.1f}%)")
                print(f"📁 Location: {capturer.output_dir.absolute()}")
                
                if capturer.photo_count >= capturer.target_photos:
                    print(f"\n✅ SUCCESS: All {capturer.target_photos} photos captured!")
                else:
                    print(f"\n⚠️  PARTIAL: {capturer.photo_count} photos captured (stopped early)")
            else:
                print("\n❌ No photos were captured")
        
        elif args.command == 'setup':
            setup_project()
        
        elif args.command == 'info':
            show_project_info()
        
        elif args.command == 'interactive':
            # Import and run interactive CLI
            import subprocess
            import sys
            subprocess.run([sys.executable, 'interactive_cli.py'])
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")
        print("For help, run: python main.py --help")

if __name__ == "__main__":
    main()