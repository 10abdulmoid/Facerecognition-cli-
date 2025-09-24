#!/usr/bin/env python3
"""
Add Person Script - Interactive face addition to the database
"""

import cv2
import numpy as np
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.append(str(Path(__file__).parent))
from face_recognizer import InsightFaceRecognizer

class PersonAdder:
    """Interactive person addition system using webcam."""
    
    def __init__(self, database_path: str = None):
        """
        Initialize person adder.
        
        Args:
            database_path: Path to saved face database
        """
        self.recognizer = InsightFaceRecognizer()
        self.database_path = database_path
        
        # Load existing database if provided
        if database_path and os.path.exists(database_path):
            self.recognizer.load_database(database_path)
            print(f"Loaded existing database with {len(self.recognizer.labels)} faces")
        else:
            print("Starting with empty database")
    
    def add_person_to_database(self, person_name: str, camera_index: int = 0):
        """
        Add a new person to the database using webcam.
        
        Args:
            person_name: Name of the person to add
            camera_index: Camera index (usually 0 for default camera)
        """
        # Create directory for this person
        person_dir = Path(f"../data/known_faces/{person_name}")
        person_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return False
        
        # Optimize camera settings
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        print(f"\n=== Adding {person_name} to database ===")
        print("Instructions:")
        print("- Position your face clearly in the frame")
        print("- Press 'c' to capture a photo")
        print("- Press 'q' to quit without saving")
        print("- You can capture multiple photos for better recognition")
        print("- Press 's' when you're done capturing photos")
        print("\nPress any key to start the webcam feed...")
        input()
        
        captured_images = []
        capture_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Detect faces in current frame
            results = self.recognizer.recognize_face(frame, confidence_threshold=0.1)  # Low threshold for detection
            
            # Draw face detection boxes
            for result in results:
                bbox = result['bbox']
                # Draw green box around detected faces
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (bbox[0], bbox[1] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Add instructions to frame
            cv2.putText(frame, f"Adding: {person_name}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, f"Captured: {capture_count} photos", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'c' to capture, 's' to save & finish, 'q' to quit", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show status
            if len(results) > 0:
                cv2.putText(frame, "READY TO CAPTURE", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "NO FACE DETECTED", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            cv2.imshow(f'Add Person: {person_name}', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('c'):
                # Capture photo
                if len(results) > 0:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_filename = f"{person_name}_{timestamp}_{capture_count + 1}.jpg"
                    image_path = person_dir / image_filename
                    
                    cv2.imwrite(str(image_path), frame)
                    captured_images.append(str(image_path))
                    capture_count += 1
                    
                    print(f"✓ Captured photo {capture_count}: {image_filename}")
                    
                    # Visual feedback
                    cv2.putText(frame, "CAPTURED!", (250, 250), 
                               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    cv2.imshow(f'Add Person: {person_name}', frame)
                    cv2.waitKey(500)  # Show feedback for 500ms
                else:
                    print("⚠ No face detected. Please position your face in the frame.")
            
            elif key == ord('s'):
                # Save to database and finish
                if captured_images:
                    print(f"\n=== Processing {len(captured_images)} captured images ===")
                    success_count = 0
                    
                    for image_path in captured_images:
                        if self.recognizer.add_face_to_database(image_path, person_name):
                            success_count += 1
                            print(f"✓ Added {os.path.basename(image_path)} to database")
                        else:
                            print(f"✗ Failed to add {os.path.basename(image_path)}")
                    
                    if success_count > 0:
                        # Save database
                        if self.database_path:
                            self.recognizer.save_database(self.database_path)
                            print(f"\n✓ Database saved to {self.database_path}")
                            print(f"✓ Successfully added {person_name} with {success_count} face samples!")
                        else:
                            print(f"\n✓ Added {person_name} with {success_count} face samples to memory!")
                            print("Note: Specify --database to save permanently")
                        
                        cap.release()
                        cv2.destroyAllWindows()
                        return True
                    else:
                        print("\n✗ No faces were successfully added to database")
                else:
                    print("⚠ No photos captured. Please capture at least one photo before saving.")
            
            elif key == ord('q') or key == 27:  # 'q' or ESC
                print("\n⚠ Cancelled. No changes made to database.")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return False
    
    def show_database_stats(self):
        """Show current database statistics."""
        if hasattr(self.recognizer, 'labels') and self.recognizer.labels:
            print(f"\n=== Database Statistics ===")
            print(f"Total people: {len(set(self.recognizer.labels))}")
            print(f"Total face samples: {len(self.recognizer.labels)}")
            
            # Count faces per person
            from collections import Counter
            face_counts = Counter(self.recognizer.labels)
            print("\nFaces per person:")
            for name, count in sorted(face_counts.items()):
                print(f"  {name}: {count} samples")
        else:
            print("Database is empty")

def main():
    """Main function to add person to face database."""
    parser = argparse.ArgumentParser(description='Add Person to Face Recognition Database')
    parser.add_argument('person_name', type=str, help='Name of the person to add')
    parser.add_argument('--database', type=str, default='../models/face_database.pkl', 
                       help='Path to face database file (default: ../models/face_database.pkl)')
    parser.add_argument('--camera', type=int, default=0, help='Camera index (default: 0)')
    parser.add_argument('--stats', action='store_true', help='Show database statistics after adding')
    
    args = parser.parse_args()
    
    # Validate person name
    if not args.person_name.strip():
        print("Error: Person name cannot be empty")
        return 1
    
    # Clean person name (remove special characters that might cause issues)
    clean_name = "".join(c for c in args.person_name if c.isalnum() or c in (' ', '-', '_')).strip()
    if clean_name != args.person_name:
        print(f"Using cleaned name: '{clean_name}' (was: '{args.person_name}')")
        args.person_name = clean_name
    
    print(f"=== Face Recognition Database - Add Person ===")
    print(f"Person to add: {args.person_name}")
    print(f"Database path: {args.database}")
    print(f"Camera index: {args.camera}")
    
    # Initialize person adder
    adder = PersonAdder(args.database)
    
    # Show current database stats
    adder.show_database_stats()
    
    # Add person
    success = adder.add_person_to_database(args.person_name, args.camera)
    
    if success:
        print(f"\n🎉 Successfully added {args.person_name} to the database!")
        
        if args.stats:
            adder.show_database_stats()
        
        print(f"\nYou can now test recognition with:")
        print(f"python main.py realtime --database {args.database}")
        return 0
    else:
        print(f"\n❌ Failed to add {args.person_name} to database")
        return 1

if __name__ == "__main__":
    exit(main())