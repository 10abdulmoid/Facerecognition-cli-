#!/usr/bin/env python3
"""
Photo Capture Script - Take 100 photos from webcam and save to person-specific directory
"""

import cv2
import os
import argparse
from datetime import datetime
from pathlib import Path

class PhotoCapture:
    """Simple webcam photo capture system for collecting 100 photos of a person."""
    
    def __init__(self, person_name: str, output_base_dir: str = "captured_photos", camera_index: int = 0):
        """
        Initialize photo capture system.
        
        Args:
            person_name: Name of the person (used for directory and filenames)
            output_base_dir: Base directory to save captured photos
            camera_index: Camera index (usually 0 for default camera)
        """
        # Clean person name for directory/filename use
        self.person_name = person_name
        self.clean_name = "".join(c for c in person_name if c.isalnum() or c in (' ', '-', '_')).strip()
        self.clean_name = self.clean_name.replace(' ', '_')
        
        self.output_dir = Path(output_base_dir) / self.clean_name
        self.camera_index = camera_index
        self.photo_count = 0
        self.target_photos = 100
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Photos will be saved to: {self.output_dir.absolute()}")
        print(f"Target: {self.target_photos} photos for {self.person_name}")
    
    def start_capture_session(self):
        """Start the photo capture session for 100 photos."""
        # Initialize camera
        cap = cv2.VideoCapture(self.camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}")
            return False
        
        # Optimize camera settings
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"\n=== Photo Capture Session Started for {self.person_name} ===")
        print("Instructions:")
        print("- Press 'c' to capture a photo")
        print("- Press 'q' or 'ESC' to quit early")
        print(f"- Target: {self.target_photos} photos")
        print("\nReady to capture photos!")
        
        window_name = f'Capturing {self.person_name} - Press C to capture, Q to quit'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        while self.photo_count < self.target_photos:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Create a copy for display
            display_frame = frame.copy()
            
            # Add status information
            self.add_status_info(display_frame)
            
            # Display frame
            cv2.imshow(window_name, display_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('c'):  # Only 'c' to capture
                self.capture_photo(frame)
                
                # Show capture feedback
                feedback_frame = display_frame.copy()
                remaining = self.target_photos - self.photo_count
                
                # Large capture feedback
                cv2.putText(feedback_frame, "CAPTURED!", 
                           (display_frame.shape[1]//2 - 150, display_frame.shape[0]//2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
                
                # Show remaining count
                if remaining > 0:
                    cv2.putText(feedback_frame, f"{remaining} more to go!", 
                               (display_frame.shape[1]//2 - 120, display_frame.shape[0]//2 + 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                else:
                    cv2.putText(feedback_frame, "COMPLETE!", 
                               (display_frame.shape[1]//2 - 100, display_frame.shape[0]//2 + 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                
                cv2.imshow(window_name, feedback_frame)
                cv2.waitKey(800)  # Show feedback for 800ms
                
                # Check if we've reached target
                if self.photo_count >= self.target_photos:
                    print(f"\n🎉 TARGET REACHED! Captured all {self.target_photos} photos!")
                    break
                
            elif key == ord('q') or key == 27:  # 'q' or ESC to quit
                print("Ending capture session early...")
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n=== Session Complete ===")
        print(f"Photos captured: {self.photo_count}/{self.target_photos}")
        print(f"Photos saved in: {self.output_dir.absolute()}")
        
        return True
    
    def capture_photo(self, frame):
        """
        Capture and save a photo with person's name in filename.
        
        Args:
            frame: The frame to save
        """
        # Generate filename with person name and counter
        filename = f"{self.clean_name}_{self.photo_count + 1:03d}.jpg"
        filepath = self.output_dir / filename
        
        # Save the photo
        success = cv2.imwrite(str(filepath), frame)
        
        if success:
            self.photo_count += 1
            remaining = self.target_photos - self.photo_count
            print(f"✓ Captured {self.photo_count}/{self.target_photos}: {filename}")
            if remaining > 0:
                print(f"  → {remaining} more photos needed")
            else:
                print(f"  → 🎉 ALL {self.target_photos} PHOTOS COMPLETE!")
        else:
            print(f"✗ Failed to save: {filename}")
    
    def add_guidelines(self, frame):
        """Add visual guidelines to help with photo composition."""
        height, width = frame.shape[:2]
        
        # Rule of thirds lines
        third_h = height // 3
        third_w = width // 3
        
        # Horizontal lines
        cv2.line(frame, (0, third_h), (width, third_h), (255, 255, 255), 1)
        cv2.line(frame, (0, third_h * 2), (width, third_h * 2), (255, 255, 255), 1)
        
        # Vertical lines
        cv2.line(frame, (third_w, 0), (third_w, height), (255, 255, 255), 1)
        cv2.line(frame, (third_w * 2, 0), (third_w * 2, height), (255, 255, 255), 1)
        
        # Center point
        cv2.circle(frame, (width // 2, height // 2), 5, (255, 255, 255), 2)
        
        # Corner indicators
        corner_size = 20
        thickness = 2
        color = (255, 255, 255)
        
        # Top-left
        cv2.line(frame, (0, 0), (corner_size, 0), color, thickness)
        cv2.line(frame, (0, 0), (0, corner_size), color, thickness)
        
        # Top-right
        cv2.line(frame, (width - corner_size, 0), (width, 0), color, thickness)
        cv2.line(frame, (width, 0), (width, corner_size), color, thickness)
        
        # Bottom-left
        cv2.line(frame, (0, height), (corner_size, height), color, thickness)
        cv2.line(frame, (0, height - corner_size), (0, height), color, thickness)
        
        # Bottom-right
        cv2.line(frame, (width - corner_size, height), (width, height), color, thickness)
        cv2.line(frame, (width, height - corner_size), (width, height), color, thickness)
    
    def add_status_info(self, frame):
        """Add status information to the frame."""
        height, width = frame.shape[:2]
        
        # Background for status text (larger to accommodate more info)
        cv2.rectangle(frame, (10, 10), (500, 120), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (500, 120), (255, 255, 255), 2)
        
        # Person name
        cv2.putText(frame, f"Person: {self.person_name}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Photo counter - large and prominent
        cv2.putText(frame, f"Photos: {self.photo_count}/{self.target_photos}", (20, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Progress percentage
        progress = (self.photo_count / self.target_photos) * 100
        cv2.putText(frame, f"Progress: {progress:.1f}%", (20, 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Instructions
        cv2.putText(frame, "Press 'C' to capture photo", (20, 115), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Large counter in top right
        counter_text = f"{self.photo_count}/{self.target_photos}"
        counter_size = cv2.getTextSize(counter_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
        cv2.putText(frame, counter_text, (width - counter_size[0] - 20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        
        # Ready indicator or completion status
        if self.photo_count < self.target_photos:
            cv2.putText(frame, "READY", (width - 100, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "COMPLETE!", (width - 150, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

def main():
    """Main function for photo capture - captures 100 photos of a person."""
    parser = argparse.ArgumentParser(description='Webcam Photo Capture Tool - Capture 100 photos of a person')
    parser.add_argument('--output-dir', type=str, default='captured_photos', 
                       help='Base directory to save captured photos (default: captured_photos)')
    parser.add_argument('--camera', type=int, default=0, 
                       help='Camera index (default: 0)')
    parser.add_argument('--person-name', type=str, 
                       help='Person name (if not provided, will ask for input)')
    
    args = parser.parse_args()
    
    # Get person name if not provided
    person_name = args.person_name
    if not person_name:
        print("=== Photo Capture Setup ===")
        person_name = input("Enter the person's name: ").strip()
        
        if not person_name:
            print("Error: Person name cannot be empty")
            return 1
    
    print(f"\n=== Webcam Photo Capture ===")
    print(f"Person: {person_name}")
    print(f"Target: 100 photos")
    print(f"Base directory: {args.output_dir}")
    print(f"Camera: {args.camera}")
    
    # Initialize and start capture
    capturer = PhotoCapture(person_name, args.output_dir, args.camera)
    success = capturer.start_capture_session()
    
    if success and capturer.photo_count > 0:
        completion_rate = (capturer.photo_count / capturer.target_photos) * 100
        print(f"\n🎉 Session completed!")
        print(f"📊 Captured: {capturer.photo_count}/{capturer.target_photos} photos ({completion_rate:.1f}%)")
        print(f"📁 Location: {capturer.output_dir.absolute()}")
        
        # List some captured files as examples
        captured_files = sorted(capturer.output_dir.glob("*.jpg"))
        if captured_files:
            print(f"\n📸 Sample files:")
            # Show first 5 and last 5 files
            sample_files = captured_files[:5] + captured_files[-5:] if len(captured_files) > 10 else captured_files
            for file in sample_files:
                print(f"  - {file.name}")
            if len(captured_files) > 10:
                print(f"  ... and {len(captured_files) - 10} more files")
                
        # Summary
        if capturer.photo_count >= capturer.target_photos:
            print(f"\n✅ SUCCESS: All {capturer.target_photos} photos captured!")
        else:
            print(f"\n⚠️  PARTIAL: {capturer.photo_count} photos captured (stopped early)")
            
    else:
        print("\n❌ No photos were captured")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())