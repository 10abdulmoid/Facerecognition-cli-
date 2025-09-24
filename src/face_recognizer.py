import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import pickle
import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import json

class InsightFaceRecognizer:
    """
    A comprehensive face recognition system using InsightFace.
    
    Features:
    - Face detection and embedding extraction
    - Face database management
    - Real-time face recognition
    - Face verification and identification
    - Similarity scoring
    """
    
    def __init__(self, model_name: str = 'buffalo_l', ctx_id: int = 0, det_size: Tuple[int, int] = (640, 640)):
        """
        Initialize the InsightFace recognizer.
        
        Args:
            model_name: Model to use ('buffalo_l', 'buffalo_m', 'buffalo_s')
            ctx_id: Context ID (0 for CPU, positive for GPU)
            det_size: Detection size for face detection
        """
        self.model_name = model_name
        self.ctx_id = ctx_id
        self.det_size = det_size
        
        # Initialize face analysis app
        self.app = FaceAnalysis(name=model_name, providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=ctx_id, det_size=det_size)
        
        # Face database
        self.face_database = {}
        self.embeddings = []
        self.labels = []
        
        print(f"InsightFace initialized with model: {model_name}")
    
    def extract_face_embedding(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract face embedding from an image.
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            Face embedding vector or None if no face detected
        """
        faces = self.app.get(image)
        
        if len(faces) == 0:
            return None
        
        # Return embedding of the largest face (by area)
        largest_face = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
        return largest_face.embedding
    
    def detect_faces(self, image: np.ndarray) -> List[Dict]:
        """
        Detect all faces in an image and return detailed information.
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            List of face information dictionaries
        """
        faces = self.app.get(image)
        face_info = []
        
        for face in faces:
            info = {
                'bbox': face.bbox.astype(int),
                'landmark': face.landmark_2d_106,
                'embedding': face.embedding,
                'age': getattr(face, 'age', None),
                'gender': getattr(face, 'gender', None),
                'score': face.det_score
            }
            face_info.append(info)
        
        return face_info
    
    def add_face_to_database(self, image_path: str, person_name: str) -> bool:
        """
        Add a face to the recognition database.
        
        Args:
            image_path: Path to the image file
            person_name: Name/ID of the person
            
        Returns:
            True if face was successfully added, False otherwise
        """
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return False
        
        # Load and process image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not load image: {image_path}")
            return False
        
        # Extract embedding
        embedding = self.extract_face_embedding(image)
        if embedding is None:
            print(f"No face detected in: {image_path}")
            return False
        
        # Add to database
        if person_name not in self.face_database:
            self.face_database[person_name] = []
        
        self.face_database[person_name].append({
            'embedding': embedding,
            'image_path': image_path
        })
        
        # Update embeddings and labels for quick search
        self.embeddings.append(embedding)
        self.labels.append(person_name)
        
        print(f"Added face for {person_name} from {image_path}")
        return True
    
    def load_faces_from_directory(self, directory_path: str) -> int:
        """
        Load all face images from a directory structure.
        Expected structure: directory_path/person_name/image.jpg
        
        Args:
            directory_path: Path to directory containing person folders
            
        Returns:
            Number of faces successfully loaded
        """
        directory_path = Path(directory_path)
        faces_loaded = 0
        
        if not directory_path.exists():
            print(f"Directory not found: {directory_path}")
            return 0
        
        for person_dir in directory_path.iterdir():
            if person_dir.is_dir():
                person_name = person_dir.name
                
                for image_file in person_dir.glob("*"):
                    if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                        if self.add_face_to_database(str(image_file), person_name):
                            faces_loaded += 1
        
        print(f"Loaded {faces_loaded} faces from {directory_path}")
        return faces_loaded
    
    def recognize_face(self, image: np.ndarray, threshold: float = 0.5) -> List[Dict]:
        """
        Recognize faces in an image against the database.
        
        Args:
            image: Input image as numpy array (BGR format)
            threshold: Similarity threshold for recognition
            
        Returns:
            List of recognition results
        """
        if len(self.embeddings) == 0:
            print("No faces in database. Please add faces first.")
            return []
        
        face_info = self.detect_faces(image)
        results = []
        
        for face in face_info:
            embedding = face['embedding'].reshape(1, -1)
            
            # Calculate similarities with all database embeddings
            similarities = cosine_similarity(embedding, self.embeddings)[0]
            
            # Find best match
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            
            if best_similarity >= threshold:
                recognized_name = self.labels[best_match_idx]
                confidence = best_similarity
            else:
                recognized_name = "Unknown"
                confidence = best_similarity
            
            result = {
                'bbox': face['bbox'],
                'name': recognized_name,
                'confidence': confidence,
                'age': face.get('age'),
                'gender': face.get('gender')
            }
            results.append(result)
        
        return results
    
    def verify_faces(self, image1: np.ndarray, image2: np.ndarray) -> Dict:
        """
        Verify if two images contain the same person.
        
        Args:
            image1: First image
            image2: Second image
            
        Returns:
            Verification result dictionary
        """
        embedding1 = self.extract_face_embedding(image1)
        embedding2 = self.extract_face_embedding(image2)
        
        if embedding1 is None or embedding2 is None:
            return {
                'verified': False,
                'similarity': 0.0,
                'error': 'No face detected in one or both images'
            }
        
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        
        return {
            'verified': similarity >= 0.5,  # Common threshold
            'similarity': similarity,
            'error': None
        }
    
    def save_database(self, filepath: str):
        """Save the face database to a file."""
        database_data = {
            'face_database': self.face_database,
            'embeddings': self.embeddings,
            'labels': self.labels
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(database_data, f)
        
        print(f"Database saved to {filepath}")
    
    def load_database(self, filepath: str):
        """Load the face database from a file."""
        if not os.path.exists(filepath):
            print(f"Database file not found: {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            database_data = pickle.load(f)
        
        self.face_database = database_data['face_database']
        self.embeddings = database_data['embeddings']
        self.labels = database_data['labels']
        
        print(f"Database loaded from {filepath}")
    
    def visualize_results(self, image: np.ndarray, results: List[Dict], save_path: Optional[str] = None):
        """
        Visualize face recognition results on an image.
        
        Args:
            image: Input image
            results: Recognition results from recognize_face()
            save_path: Optional path to save the visualization
        """
        vis_image = image.copy()
        
        for result in results:
            bbox = result['bbox']
            name = result['name']
            confidence = result['confidence']
            
            # Draw bounding box
            cv2.rectangle(vis_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            
            # Prepare label text
            label = f"{name}: {confidence:.2f}"
            if result.get('age'):
                label += f" (Age: {result['age']:.0f})"
            
            # Draw label background
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(vis_image, (bbox[0], bbox[1] - label_size[1] - 10), 
                         (bbox[0] + label_size[0], bbox[1]), (0, 255, 0), -1)
            
            # Draw label text
            cv2.putText(vis_image, label, (bbox[0], bbox[1] - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        if save_path:
            cv2.imwrite(save_path, vis_image)
            print(f"Visualization saved to {save_path}")
        
        return vis_image
    
    def get_database_stats(self) -> Dict:
        """Get statistics about the face database."""
        stats = {
            'total_people': len(self.face_database),
            'total_faces': len(self.embeddings),
            'people': {}
        }
        
        for person_name, faces in self.face_database.items():
            stats['people'][person_name] = len(faces)
        
        return stats