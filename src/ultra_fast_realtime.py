import cv2
import numpy as np
import sys
import os
from pathlib import Path
import time
import threading
from collections import deque

# Add src directory to path
sys.path.append(str(Path(__file__).parent))
from face_recognizer import InsightFaceRecognizer

class UltraFastRealTimeFaceRecognition:
    """Ultra high-performance real-time face recognition optimized for maximum speed."""
    
    def __init__(self, database_path: str = None, confidence_threshold: float = 0.2):
        """
        Initialize ultra-fast real-time face recognition.
        
        Args:
            database_path: Path to saved face database
            confidence_threshold: Minimum confidence for recognition (very low for best detection)
        """
        self.recognizer = InsightFaceRecognizer()
        self.confidence_threshold = confidence_threshold
        
        # Load existing database if provided
        if database_path and os.path.exists(database_path):
            self.recognizer.load_database(database_path)
            print(f"Loaded database with {len(self.recognizer.labels)} faces")
        else:
            print("Starting with empty database")
            
        # Threading for background processing
        self.processing_queue = deque(maxlen=2)  # Keep only latest frames
        self.results_queue = deque(maxlen=1)
        self.processing_thread = None
        self.should_process = True
    
    def process_frames_background(self):
        """Background thread for face recognition processing."""
        while self.should_process:
            if self.processing_queue:
                frame = self.processing_queue.popleft()
                try:
                    results = self.recognizer.recognize_face(frame, self.confidence_threshold)
                    # Only keep good results
                    good_results = [r for r in results if r['name'] != "Unknown" or r['confidence'] > 0.15]
                    
                    # Update results queue
                    if self.results_queue:
                        self.results_queue.clear()
                    self.results_queue.append(good_results)
                    
                    # Minimal output for recognized faces only
                    for result in good_results:
                        if result['name'] != "Unknown":
                            print(f"{result['name']} ({result['confidence']:.2f})")
                            
                except Exception as e:
                    pass  # Skip errors for performance
            else:
                time.sleep(0.001)  # Very short sleep
    
    def run_webcam_recognition(self, camera_index: int = 0):
        """
        Run ultra high-performance real-time face recognition using webcam.
        """
        # Initialize camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return
        
        # Ultra-aggressive camera optimizations
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)  # Smaller resolution for speed
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        cap.set(cv2.CAP_PROP_FPS, 60)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        
        print("Ultra-fast real-time face recognition started. Press 'q' to quit.")
        
        # Start background processing thread
        self.processing_thread = threading.Thread(target=self.process_frames_background, daemon=True)
        self.processing_thread.start()
        
        frame_count = 0
        last_results = []
        skip_frames = 0
        
        # Performance tracking
        fps_counter = 0
        fps_start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Skip frames to reduce camera buffer lag
            skip_frames += 1
            if skip_frames < 2:  # Skip every other frame from camera
                continue
            skip_frames = 0
            
            # Send frame for processing every 8th frame only
            if frame_count % 8 == 0:
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (320, 240))
                if len(self.processing_queue) < 2:  # Don't overflow queue
                    self.processing_queue.append(small_frame)
            
            # Get latest results
            if self.results_queue:
                latest_results = self.results_queue[-1]
                if latest_results:
                    last_results = latest_results
            
            # Draw results (very fast drawing)
            self.draw_results_fast(frame, last_results)
            
            # Display frame
            cv2.imshow('Ultra-Fast Recognition (Press Q)', frame)
            
            # Fast key check
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stopping...")
                break
            
            frame_count += 1
            fps_counter += 1
            
            # FPS display every 3 seconds for less overhead
            if fps_counter % 90 == 0:
                current_time = time.time()
                elapsed = current_time - fps_start_time
                fps = fps_counter / elapsed
                print(f"FPS: {fps:.1f}")
                fps_counter = 0
                fps_start_time = current_time
        
        # Cleanup
        self.should_process = False
        if self.processing_thread:
            self.processing_thread.join(timeout=1)
        cap.release()
        cv2.destroyAllWindows()
        print("Ultra-fast recognition stopped.")
    
    def draw_results_fast(self, frame: np.ndarray, results: list):
        """Ultra-fast drawing of recognition results."""
        height, width = frame.shape[:2]
        
        for result in results:
            bbox = result['bbox']
            name = result['name']
            confidence = result['confidence']
            
            # Scale bbox back to full frame size
            scale_x = width / 320
            scale_y = height / 240
            bbox = [int(bbox[0] * scale_x), int(bbox[1] * scale_y), 
                   int(bbox[2] * scale_x), int(bbox[3] * scale_y)]
            
            # Choose color
            if name == "Unknown":
                color = (0, 0, 255)  # Red
            else:
                color = (0, 255, 255) if name.lower() == "trump" else (0, 255, 0)  # Yellow for Trump, Green for others
            
            # Fast drawing - minimal operations
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            
            # Simple text
            if name != "Unknown":
                cv2.putText(frame, f"{name}", (bbox[0], bbox[1] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def main():
    """Main function for testing."""
    ultra_fast_recognizer = UltraFastRealTimeFaceRecognition(
        database_path="../models/face_database.pkl",
        confidence_threshold=0.2
    )
    ultra_fast_recognizer.run_webcam_recognition()

if __name__ == "__main__":
    main()