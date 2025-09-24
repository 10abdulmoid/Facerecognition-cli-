#!/usr/bin/env python3
"""
Interactive CLI for Face Recognition System
A user-friendly command-line interface for face recognition operations

Author: AI Assistant
Date: September 2025
"""

import sys
import os
from pathlib import Path
import time

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.append(str(src_dir))

from face_recognizer import InsightFaceRecognizer
from photo_capture import PhotoCapture
from ultra_fast_realtime import UltraFastRealTimeFaceRecognition

class InteractiveFaceRecognitionCLI:
    """Interactive CLI for face recognition operations."""
    
    def __init__(self):
        """Initialize the interactive CLI."""
        self.database_path = "models/face_database.pkl"
        self.recognizer = None
        
    def print_banner(self):
        """Print welcome banner."""
        banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║              🤖 Interactive Face Recognition CLI             ║
    ║                                                              ║
    ║          Welcome to your personal face recognition system!   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_main_menu(self):
        """Print the main menu options."""
        menu = """
    ┌─────────────────────────────────────────────────────────────┐
    │                        MAIN MENU                            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  1. 👁️  Detect faces from existing database                 │
    │                                                             │
    │  2. 📷 Add new person to database (100 photos + detection)  │
    │                                                             │
    │  3. 📊 View database statistics                             │
    │                                                             │
    │  4. 🚪 Exit                                                 │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
        """
        print(menu)
    
    def get_user_choice(self):
        """Get user's menu choice."""
        while True:
            try:
                choice = input("\n    👉 Enter your choice (1-4): ").strip()
                if choice in ['1', '2', '3', '4']:
                    return int(choice)
                else:
                    print("    ❌ Invalid choice! Please enter 1, 2, 3, or 4.")
            except KeyboardInterrupt:
                print("\n\n    👋 Goodbye!")
                sys.exit(0)
            except Exception:
                print("    ❌ Invalid input! Please enter a number between 1-4.")
    
    def check_database_exists(self):
        """Check if database exists and show stats."""
        if os.path.exists(self.database_path):
            # Load recognizer to check database
            temp_recognizer = InsightFaceRecognizer()
            temp_recognizer.load_database(self.database_path)
            stats = temp_recognizer.get_database_stats()
            
            print(f"\n    ✅ Database found: {stats['total_people']} people, {stats['total_faces']} faces")
            for person, count in stats['people'].items():
                print(f"       • {person}: {count} face(s)")
            return True
        else:
            print(f"\n    ⚠️  No database found at {self.database_path}")
            return False
    
    def option_detect_existing(self):
        """Option 1: Detect faces from existing database."""
        print("\n" + "="*60)
        print("    🔍 DETECTING FROM EXISTING DATABASE")
        print("="*60)
        
        if not self.check_database_exists():
            print("    ❌ Cannot detect without a database. Please add people first (Option 2).")
            input("\n    Press Enter to continue...")
            return
        
        print("\n    🚀 Starting real-time face detection...")
        print("    📹 Make sure your camera is connected and working.")
        print("    💡 Press 'q' to quit the detection window.")
        
        # Give user time to prepare
        for i in range(3, 0, -1):
            print(f"    ⏰ Starting in {i}...")
            time.sleep(1)
        
        try:
            # Initialize ultra-fast recognition
            recognition_system = UltraFastRealTimeFaceRecognition(
                database_path=self.database_path,
                confidence_threshold=0.3
            )
            
            print("\n    🎥 Camera starting... Look at the camera!")
            recognition_system.run_webcam_recognition()
            
        except KeyboardInterrupt:
            print("\n    ⏹️  Detection stopped by user.")
        except Exception as e:
            print(f"\n    ❌ Error during detection: {str(e)}")
        
        print("\n    ✅ Detection session ended.")
        input("\n    Press Enter to return to main menu...")
    
    def option_add_new_person(self):
        """Option 2: Add new person to database (100 photos + detection)."""
        print("\n" + "="*60)
        print("    📷 ADD NEW PERSON TO DATABASE")
        print("="*60)
        
        # Get person name
        while True:
            person_name = input("\n    👤 Enter the person's name: ").strip()
            if person_name:
                # Clean name (remove special characters)
                clean_name = "".join(c for c in person_name if c.isalnum() or c in " _-").strip()
                if clean_name:
                    person_name = clean_name
                    break
                else:
                    print("    ❌ Please enter a valid name with letters/numbers.")
            else:
                print("    ❌ Name cannot be empty!")
        
        print(f"\n    📸 We'll now capture 100 photos of {person_name}")
        print("    💡 Tips for best results:")
        print("       • Ensure good lighting")
        print("       • Look at the camera")
        print("       • Try different angles and expressions")
        print("       • Stay within the camera frame")
        
        input(f"\n    👉 Press Enter when {person_name} is ready for photo capture...")
        
        try:
            # Step 1: Capture 100 photos
            print(f"\n    📷 Capturing 100 photos of {person_name}...")
            capture_system = PhotoCapture(person_name, output_base_dir="data/captured_photos")
            success = capture_system.start_capture_session()
            
            if capture_system.photo_count == 0:
                print("    ❌ No photos were captured.")
                input("\n    Press Enter to return to main menu...")
                return
            elif capture_system.photo_count < 100:
                print(f"    ⚠️  Only captured {capture_system.photo_count} photos (target was 100).")
                continue_prompt = input("    Continue with database addition? (y/n): ").lower()
                if continue_prompt != 'y':
                    return
            
            print(f"    ✅ Successfully captured {capture_system.photo_count} photos of {person_name}!")
            print(f"    📁 Photos saved to: {capture_system.output_dir}")
            
            # Step 2: Add to database
            print(f"\n    💾 Adding {person_name} to face database...")
            
            # Initialize recognizer if not exists
            if not self.recognizer:
                self.recognizer = InsightFaceRecognizer()
                
            # Load existing database if it exists
            if os.path.exists(self.database_path):
                self.recognizer.load_database(self.database_path)
            
            # Add photos to database from the specific person's directory
            photos_dir = capture_system.output_dir
            added_count = 0
            
            if photos_dir.exists():
                print(f"    🔄 Processing {capture_system.photo_count} photos...")
                for img_file in photos_dir.glob("*.jpg"):
                    if self.recognizer.add_face_to_database(str(img_file), person_name):
                        added_count += 1
                        print(f"       ✓ Added face from {img_file.name}")
                    else:
                        print(f"       ✗ No face detected in {img_file.name}")
                
                # Save updated database
                self.recognizer.save_database(self.database_path)
                
                print(f"    ✅ Added {added_count} face embeddings for {person_name} to database!")
                
                # Step 3: Start real-time detection
                print(f"\n    🎯 Now starting real-time detection with {person_name} included!")
                print("    📹 You should now see recognition working with the new person.")
                print("    💡 Press 'q' to quit the detection window.")
                
                # Give user time to prepare
                for i in range(3, 0, -1):
                    print(f"    ⏰ Starting detection in {i}...")
                    time.sleep(1)
                
                # Start real-time recognition
                recognition_system = UltraFastRealTimeFaceRecognition(
                    database_path=self.database_path,
                    confidence_threshold=0.3
                )
                
                print(f"\n    🎥 Camera starting... {person_name}, look at the camera to test recognition!")
                recognition_system.run_webcam_recognition()
                
            else:
                print(f"    ❌ Could not find captured photos directory for {person_name}")
                
        except KeyboardInterrupt:
            print("\n    ⏹️  Process stopped by user.")
        except Exception as e:
            print(f"\n    ❌ Error during process: {str(e)}")
        
        print(f"\n    ✅ Process completed for {person_name}!")
        input("\n    Press Enter to return to main menu...")
    
    def option_view_stats(self):
        """Option 3: View database statistics."""
        print("\n" + "="*60)
        print("    📊 DATABASE STATISTICS")
        print("="*60)
        
        if not os.path.exists(self.database_path):
            print("    ⚠️  No database found. Add some people first!")
            input("\n    Press Enter to return to main menu...")
            return
        
        try:
            # Load recognizer to get stats
            temp_recognizer = InsightFaceRecognizer()
            temp_recognizer.load_database(self.database_path)
            stats = temp_recognizer.get_database_stats()
            
            print(f"\n    📁 Database file: {self.database_path}")
            print(f"    👥 Total people: {stats['total_people']}")
            print(f"    🤖 Total face embeddings: {stats['total_faces']}")
            print(f"    💾 Approximate size: {stats['total_faces'] * 512 * 4 / 1024:.1f} KB")
            
            print("\n    👤 People in database:")
            if stats['people']:
                for person, count in stats['people'].items():
                    percentage = (count / stats['total_faces']) * 100
                    print(f"       • {person}: {count} faces ({percentage:.1f}%)")
            else:
                print("       (No people in database)")
                
        except Exception as e:
            print(f"    ❌ Error reading database: {str(e)}")
        
        input("\n    Press Enter to return to main menu...")
    
    def run(self):
        """Run the interactive CLI."""
        try:
            # Clear screen and show banner
            os.system('clear' if os.name == 'posix' else 'cls')
            self.print_banner()
            
            # Check initial database status
            print("\n    🔍 Checking system status...")
            self.check_database_exists()
            
            while True:
                self.print_main_menu()
                choice = self.get_user_choice()
                
                if choice == 1:
                    self.option_detect_existing()
                elif choice == 2:
                    self.option_add_new_person()
                elif choice == 3:
                    self.option_view_stats()
                elif choice == 4:
                    print("\n    👋 Thank you for using Face Recognition CLI!")
                    print("    💫 Goodbye!")
                    break
                
                # Clear screen for next iteration
                os.system('clear' if os.name == 'posix' else 'cls')
                self.print_banner()
                
        except KeyboardInterrupt:
            print("\n\n    👋 Goodbye!")
        except Exception as e:
            print(f"\n    ❌ Unexpected error: {str(e)}")

def main():
    """Main entry point."""
    cli = InteractiveFaceRecognitionCLI()
    cli.run()

if __name__ == "__main__":
    main()