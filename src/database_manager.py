import sys
import os
from pathlib import Path
import argparse
import cv2
import json

# Add src directory to path
sys.path.append(str(Path(__file__).parent))
from face_recognizer import InsightFaceRecognizer

class FaceDatabaseManager:
    """Manage face recognition database."""
    
    def __init__(self, database_path: str = "../models/face_database.pkl"):
        """
        Initialize database manager.
        
        Args:
            database_path: Path to the face database file
        """
        self.database_path = database_path
        self.recognizer = InsightFaceRecognizer()
        
        # Load existing database if it exists
        if os.path.exists(database_path):
            self.recognizer.load_database(database_path)
    
    def add_person_from_images(self, person_name: str, image_paths: list) -> int:
        """
        Add a person to the database from multiple images.
        
        Args:
            person_name: Name of the person
            image_paths: List of image file paths
            
        Returns:
            Number of faces successfully added
        """
        added_count = 0
        
        for image_path in image_paths:
            if self.recognizer.add_face_to_database(image_path, person_name):
                added_count += 1
        
        return added_count
    
    def add_person_from_directory(self, person_name: str, directory_path: str) -> int:
        """
        Add a person to the database from all images in a directory.
        
        Args:
            person_name: Name of the person
            directory_path: Path to directory containing person's images
            
        Returns:
            Number of faces successfully added
        """
        directory_path = Path(directory_path)
        image_paths = []
        
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            image_paths.extend(directory_path.glob(ext))
        
        added_count = 0
        for image_path in image_paths:
            if self.recognizer.add_face_to_database(str(image_path), person_name):
                added_count += 1
        
        return added_count
    
    def load_from_structured_directory(self, root_directory: str) -> int:
        """
        Load faces from a structured directory.
        Expected structure: root_directory/person_name/images...
        
        Args:
            root_directory: Root directory containing person folders
            
        Returns:
            Total number of faces loaded
        """
        return self.recognizer.load_faces_from_directory(root_directory)
    
    def remove_person(self, person_name: str) -> bool:
        """
        Remove a person from the database.
        
        Args:
            person_name: Name of the person to remove
            
        Returns:
            True if person was removed, False if not found
        """
        if person_name not in self.recognizer.face_database:
            print(f"Person '{person_name}' not found in database")
            return False
        
        # Remove from face_database
        del self.recognizer.face_database[person_name]
        
        # Rebuild embeddings and labels
        self.recognizer.embeddings = []
        self.recognizer.labels = []
        
        for name, faces in self.recognizer.face_database.items():
            for face_data in faces:
                self.recognizer.embeddings.append(face_data['embedding'])
                self.recognizer.labels.append(name)
        
        print(f"Removed '{person_name}' from database")
        return True
    
    def list_people(self):
        """List all people in the database."""
        stats = self.recognizer.get_database_stats()
        
        print(f"\nDatabase Statistics:")
        print(f"Total people: {stats['total_people']}")
        print(f"Total faces: {stats['total_faces']}")
        print("\nPeople in database:")
        
        for person_name, face_count in stats['people'].items():
            print(f"  - {person_name}: {face_count} face(s)")
    
    def export_database_info(self, output_path: str):
        """Export database information to JSON."""
        stats = self.recognizer.get_database_stats()
        
        export_data = {
            'database_stats': stats,
            'export_timestamp': str(cv2.getTickCount()),
            'model_info': {
                'model_name': self.recognizer.model_name,
                'detection_size': self.recognizer.det_size
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Database info exported to {output_path}")
    
    def verify_database_integrity(self):
        """Verify the integrity of the database."""
        print("Verifying database integrity...")
        
        issues = []
        
        # Check if embeddings and labels match
        if len(self.recognizer.embeddings) != len(self.recognizer.labels):
            issues.append("Mismatch between embeddings and labels count")
        
        # Check if face_database entries match embeddings
        face_db_count = sum(len(faces) for faces in self.recognizer.face_database.values())
        if face_db_count != len(self.recognizer.embeddings):
            issues.append("Mismatch between face_database and embeddings count")
        
        # Check for missing image files
        missing_files = []
        for person_name, faces in self.recognizer.face_database.items():
            for face_data in faces:
                if not os.path.exists(face_data['image_path']):
                    missing_files.append(face_data['image_path'])
        
        if missing_files:
            issues.append(f"Missing image files: {missing_files}")
        
        if issues:
            print("Issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("Database integrity check passed!")
        
        return len(issues) == 0
    
    def save_database(self):
        """Save the current database."""
        os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
        self.recognizer.save_database(self.database_path)
    
    def backup_database(self, backup_path: str):
        """Create a backup of the database."""
        import shutil
        shutil.copy2(self.database_path, backup_path)
        print(f"Database backed up to {backup_path}")

def main():
    """Main function for database management."""
    parser = argparse.ArgumentParser(description='Face Database Manager')
    parser.add_argument('--database', type=str, default='../models/face_database.pkl',
                       help='Path to face database file')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add person command
    add_parser = subparsers.add_parser('add', help='Add person to database')
    add_parser.add_argument('name', type=str, help='Person name')
    add_parser.add_argument('--images', nargs='+', help='Image file paths')
    add_parser.add_argument('--directory', type=str, help='Directory containing person images')
    
    # Load directory command
    load_parser = subparsers.add_parser('load', help='Load faces from structured directory')
    load_parser.add_argument('directory', type=str, help='Root directory with person folders')
    
    # Remove person command
    remove_parser = subparsers.add_parser('remove', help='Remove person from database')
    remove_parser.add_argument('name', type=str, help='Person name to remove')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all people in database')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export database info')
    export_parser.add_argument('output', type=str, help='Output JSON file path')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify database integrity')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup database')
    backup_parser.add_argument('backup_path', type=str, help='Backup file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize database manager
    manager = FaceDatabaseManager(args.database)
    
    # Execute command
    if args.command == 'add':
        if args.images:
            added = manager.add_person_from_images(args.name, args.images)
            print(f"Added {added} faces for {args.name}")
        elif args.directory:
            added = manager.add_person_from_directory(args.name, args.directory)
            print(f"Added {added} faces for {args.name}")
        else:
            print("Please specify either --images or --directory")
            return
        
        manager.save_database()
    
    elif args.command == 'load':
        loaded = manager.load_from_structured_directory(args.directory)
        print(f"Loaded {loaded} faces from {args.directory}")
        manager.save_database()
    
    elif args.command == 'remove':
        if manager.remove_person(args.name):
            manager.save_database()
    
    elif args.command == 'list':
        manager.list_people()
    
    elif args.command == 'export':
        manager.export_database_info(args.output)
    
    elif args.command == 'verify':
        manager.verify_database_integrity()
    
    elif args.command == 'backup':
        if os.path.exists(manager.database_path):
            manager.backup_database(args.backup_path)
        else:
            print("No database file found to backup")

if __name__ == "__main__":
    main()