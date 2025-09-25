# Contributing to Face Recognition CLI

Thank you for your interest in contributing to this face recognition project! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues
- Use the GitHub Issues tab to report bugs or request features
- Provide detailed information about the issue
- Include steps to reproduce any bugs
- Specify your operating system and Python version

### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Making Changes
1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature-name
   ```
2. Make your changes
3. Test your changes thoroughly
4. Follow the existing code style
5. Update documentation if needed

### Submitting Changes
1. Commit your changes with descriptive messages
2. Push to your fork
3. Create a Pull Request
4. Describe what your changes do and why

## Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular

## Testing
- Test all face recognition features
- Verify real-time recognition works properly
- Test database operations (add, list, load)
- Check compatibility with different image formats

## Questions?
Feel free to open an issue for any questions about contributing.