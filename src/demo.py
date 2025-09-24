import sys
import os
from pathlib import Path
import cv2
import numpy as np
import argparse

# Add src directory to path
sys.path.append(str(Path(__file__).parent))
from face_recognizer import InsightFaceRecognizer

class FaceRecognitionDemo:
    """Demonstration script for face recognition capabilities."""
    
    def __init__(self, database_path: str = None):
        """Initialize the demo with optional database."""
        self.recognizer = InsightFaceRecognizer()
        
        if database_path and os.path.exists(database_path):
            self.recognizer.load_database(database_path)
            print(f"Loaded database with {len(self.recognizer.labels)} faces")
        else:
            print("No database loaded. Will create demo database.")
    
    def demo_face_detection(self, image_path: str):
        """Demonstrate face detection capabilities."""
        print(f"\n=== Face Detection Demo ===")
        print(f"Processing: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not load image: {image_path}")
            return
        
        # Detect faces
        faces = self.recognizer.detect_faces(image)
        print(f"Detected {len(faces)} face(s)")
        
        # Draw results
        vis_image = image.copy()
        for i, face in enumerate(faces):
            bbox = face['bbox']
            score = face['score']
            
            # Draw bounding box
            cv2.rectangle(vis_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            
            # Draw face number and confidence
            label = f"Face {i+1}: {score:.3f}"
            cv2.putText(vis_image, label, (bbox[0], bbox[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Print face info
            print(f"  Face {i+1}:")
            print(f"    Bbox: ({bbox[0]}, {bbox[1]}) to ({bbox[2]}, {bbox[3]})")
            print(f"    Confidence: {score:.3f}")
            if face.get('age'):
                print(f"    Age: {face['age']:.1f}")
            if face.get('gender') is not None:
                gender = "Male" if face['gender'] == 1 else "Female"
                print(f"    Gender: {gender}")
        
        # Save result
        output_path = "../results/detection_demo.jpg"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, vis_image)
        print(f"Detection result saved to: {output_path}")
    
    def demo_face_verification(self, image1_path: str, image2_path: str):
        """Demonstrate face verification between two images."""
        print(f"\n=== Face Verification Demo ===")
        print(f"Comparing: {image1_path} vs {image2_path}")
        
        # Load images
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)
        
        if image1 is None or image2 is None:
            print("Could not load one or both images")
            return
        
        # Verify faces
        result = self.recognizer.verify_faces(image1, image2)
        
        print(f"Verification result:")
        print(f"  Similarity: {result['similarity']:.4f}")
        print(f"  Verified: {result['verified']}")
        if result.get('error'):
            print(f"  Error: {result['error']}")
        
        # Create comparison visualization
        h1, w1 = image1.shape[:2]
        h2, w2 = image2.shape[:2]
        
        # Resize images to same height
        target_height = 300
        new_w1 = int(w1 * target_height / h1)
        new_w2 = int(w2 * target_height / h2)
        
        resized1 = cv2.resize(image1, (new_w1, target_height))
        resized2 = cv2.resize(image2, (new_w2, target_height))
        
        # Create side-by-side comparison
        comparison = np.hstack([resized1, resized2])
        
        # Add text overlay
        status_text = f"Similarity: {result['similarity']:.4f} - {'MATCH' if result['verified'] else 'NO MATCH'}"
        color = (0, 255, 0) if result['verified'] else (0, 0, 255)
        
        cv2.putText(comparison, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Save result
        output_path = "../results/verification_demo.jpg"
        cv2.imwrite(output_path, comparison)
        print(f"Verification result saved to: {output_path}")
    
    def demo_face_recognition(self, image_path: str):
        """Demonstrate face recognition against database."""
        print(f"\n=== Face Recognition Demo ===")
        print(f"Processing: {image_path}")
        
        if len(self.recognizer.embeddings) == 0:
            print("No faces in database for recognition demo")
            return
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not load image: {image_path}")
            return
        
        # Recognize faces
        results = self.recognizer.recognize_face(image, threshold=0.5)
        print(f"Recognition results for {len(results)} face(s):")
        
        for i, result in enumerate(results):
            print(f"  Face {i+1}:")
            print(f"    Name: {result['name']}")
            print(f"    Confidence: {result['confidence']:.4f}")
            if result.get('age'):
                print(f"    Age: {result['age']:.1f}")
            if result.get('gender') is not None:
                gender = "Male" if result['gender'] == 1 else "Female"
                print(f"    Gender: {gender}")
        
        # Visualize results
        vis_image = self.recognizer.visualize_results(image, results)
        
        # Save result
        output_path = "../results/recognition_demo.jpg"
        cv2.imwrite(output_path, vis_image)
        print(f"Recognition result saved to: {output_path}")
    
    def create_sample_database(self):
        """Create a sample database for demonstration."""
        print("\n=== Creating Sample Database ===")
        
        # Check if sample images exist
        known_faces_dir = Path("../data/known_faces")
        if not known_faces_dir.exists():
            print("Creating sample directories...")
            known_faces_dir.mkdir(parents=True, exist_ok=True)
            
            # Create sample person directories
            (known_faces_dir / "person1").mkdir(exist_ok=True)
            (known_faces_dir / "person2").mkdir(exist_ok=True)
            
            print("Sample directories created. Please add images to:")
            print(f"  {known_faces_dir / 'person1'}")
            print(f"  {known_faces_dir / 'person2'}")
            print("Then run the demo again.")
            return False
        
        # Load faces from directory structure
        loaded_count = self.recognizer.load_faces_from_directory(str(known_faces_dir))
        
        if loaded_count > 0:
            # Save database
            database_path = "../models/face_database.pkl"
            os.makedirs(os.path.dirname(database_path), exist_ok=True)
            self.recognizer.save_database(database_path)
            print(f"Sample database created and saved to: {database_path}")
            return True
        else:
            print("No faces found in sample directories")
            return False
    
    def run_full_demo(self, test_image: str = None):
        """Run a complete demonstration of all features."""
        print("=" * 50)
        print("InsightFace Recognition System Demo")
        print("=" * 50)
        
        # Create or load database
        if len(self.recognizer.embeddings) == 0:
            if not self.create_sample_database():
                print("Cannot run full demo without a database")
                return
        
        # Print database stats
        stats = self.recognizer.get_database_stats()
        print(f"\nDatabase loaded with {stats['total_people']} people and {stats['total_faces']} faces")
        
        # Use default test image if none provided
        if test_image is None:
            test_images_dir = Path("../data/test_images")
            test_images_dir.mkdir(exist_ok=True)
            
            # Look for any image in test directory
            test_files = list(test_images_dir.glob("*.jpg")) + list(test_images_dir.glob("*.png"))
            if test_files:
                test_image = str(test_files[0])
            else:
                print("\nNo test images found. Please add images to:")
                print(f"  {test_images_dir}")
                return
        
        # Run demos
        self.demo_face_detection(test_image)
        self.demo_face_recognition(test_image)
        
        print(f"\nDemo completed! Check the results directory for output images.")
        print("Next steps:")
        print("1. Add more people to your database using database_manager.py")
        print("2. Try real-time recognition with realtime_recognition.py")
        print("3. Test with your own images")

def main():
    """Main function for running demos."""
    parser = argparse.ArgumentParser(description='Face Recognition Demo')
    parser.add_argument('--database', type=str, help='Path to face database file')
    parser.add_argument('--test-image', type=str, help='Path to test image')
    parser.add_argument('--demo', type=str, choices=['detection', 'recognition', 'verification', 'full'],
                       default='full', help='Type of demo to run')
    parser.add_argument('--image1', type=str, help='First image for verification demo')
    parser.add_argument('--image2', type=str, help='Second image for verification demo')
    
    args = parser.parse_args()
    
    # Initialize demo
    demo = FaceRecognitionDemo(args.database)
    
    # Run selected demo
    if args.demo == 'detection':
        if args.test_image:
            demo.demo_face_detection(args.test_image)
        else:
            print("Please provide --test-image for detection demo")
    
    elif args.demo == 'recognition':
        if args.test_image:
            demo.demo_face_recognition(args.test_image)
        else:
            print("Please provide --test-image for recognition demo")
    
    elif args.demo == 'verification':
        if args.image1 and args.image2:
            demo.demo_face_verification(args.image1, args.image2)
        else:
            print("Please provide --image1 and --image2 for verification demo")
    
    elif args.demo == 'full':
        demo.run_full_demo(args.test_image)

if __name__ == "__main__":
    main()