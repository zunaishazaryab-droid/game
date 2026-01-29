# Contributing to Forget to Win

Thank you for your interest in contributing to **Forget to Win**! 🎉

We welcome contributions from everyone. This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers
- ✅ Focus on what is best for the community
- ✅ Show empathy towards others

### Unacceptable Behavior

- ❌ Harassment or discrimination
- ❌ Trolling or insulting comments
- ❌ Personal or political attacks
- ❌ Publishing others' private information

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of terminal/command line
- Familiarity with Python

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/forget-to-win.git
   cd forget-to-win
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game**
   ```bash
   python main.py
   ```

6. **Run demo**
   ```bash
   python demo.py
   ```

---

## 💡 How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 1. **Code Contributions**
- Bug fixes
- New features
- Performance improvements
- Code refactoring

#### 2. **Documentation**
- Improving README
- Adding code comments
- Writing tutorials
- Translating documentation

#### 3. **Design**
- UI/UX improvements
- New color themes
- ASCII art enhancements

#### 4. **Testing**
- Writing unit tests
- Manual testing
- Reporting bugs

#### 5. **Content**
- New item themes
- Daily wisdom tips
- Rank titles and taglines

---

## 🔄 Development Process

### 1. **Find or Create an Issue**

- Check [existing issues](https://github.com/yourusername/forget-to-win/issues)
- If your idea is new, create an issue first
- Discuss your approach before coding

### 2. **Create a Branch**

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Or bug fix branch
git checkout -b fix/bug-description
```

### 3. **Make Your Changes**

- Write clean, readable code
- Follow coding standards (see below)
- Add comments for complex logic
- Update documentation if needed

### 4. **Test Your Changes**

```bash
# Run the game
python main.py

# Run demo
python demo.py

# Test your specific feature
# (Add unit tests in future versions)
```

### 5. **Commit Your Changes**

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new item theme for sports"

# Or
git commit -m "fix: handle empty input in recall phase"
```

**Commit Message Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### 6. **Push to Your Fork**

```bash
git push origin feature/your-feature-name
```

### 7. **Create Pull Request**

- Go to your fork on GitHub
- Click "New Pull Request"
- Fill in the PR template
- Link related issues
- Request review

---

## 📝 Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guide:

#### **1. Type Hints (Required)**

```python
# Good
def calculate_score(correct: int, total: int) -> float:
    return (correct / total) * 100

# Bad
def calculate_score(correct, total):
    return (correct / total) * 100
```

#### **2. Docstrings (Required)**

```python
def get_rank(score: int) -> str:
    """
    Determine player rank based on score.
    
    Args:
        score: Total game score (0-100)
    
    Returns:
        Rank name (e.g., "Zen Master")
    
    Examples:
        >>> get_rank(85)
        'Zen Master'
    """
    pass
```

#### **3. Naming Conventions**

```python
# Constants: UPPER_CASE
MAX_LEVELS = 5
POINTS_PER_CORRECT = 10

# Classes: PascalCase
class GameEngine:
    pass

# Functions/Variables: snake_case
def calculate_level_score():
    pass

user_input = "1,3,5"

# Private: leading underscore
def _internal_helper():
    pass
```

#### **4. Code Organization**

```python
# 1. Imports (standard library first)
import time
from dataclasses import dataclass
from typing import List, Tuple

# 2. Third-party imports
from rich.console import Console

# 3. Local imports
from game_engine import ScoreCalculator

# 4. Constants
MAX_LEVELS = 5

# 5. Classes
class GameEngine:
    pass

# 6. Functions
def main():
    pass

# 7. Main execution
if __name__ == "__main__":
    main()
```

---

## 🔍 Code Review Checklist

Before submitting, ensure:

### Functionality
- ✅ Code works as intended
- ✅ Edge cases handled
- ✅ No regressions (existing features still work)

### Code Quality
- ✅ Follows PEP 8 style guide
- ✅ Type hints present
- ✅ Docstrings complete
- ✅ No code duplication
- ✅ Meaningful variable names

### Testing
- ✅ Manual testing done
- ✅ Game runs without errors
- ✅ Demo mode works (if applicable)

### Documentation
- ✅ README updated (if needed)
- ✅ Comments added for complex logic
- ✅ Docstrings updated

---

## 🐛 Reporting Bugs

### Before Reporting

1. Check if the bug is already reported
2. Try to reproduce the bug
3. Gather relevant information

### Bug Report Template

```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- Python Version: 3.11
- Rich Version: 13.0.0

## Screenshots
(if applicable)

## Additional Context
Any other relevant information
```

---

## 💡 Suggesting Features

### Feature Request Template

```markdown
## Feature Description
Brief description of the feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How would this feature work?

## Alternatives Considered
What other solutions did you consider?

## Additional Context
Mockups, examples, or references
```

---

## 🎯 Good First Issues

Looking to contribute but not sure where to start? Look for issues labeled:

- `good first issue` - Perfect for newcomers
- `help wanted` - We need your help!
- `documentation` - Improve docs
- `enhancement` - New features

---

## 📚 Resources

### Documentation
- [README](README.md) - User guide
- [Architecture](docs/architecture/index.md) - System design
- [Development Process](docs/development/index.md) - Development workflow

### Learning
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

---

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the project

---

## 📞 Getting Help

- **Questions**: Open a [Discussion](https://github.com/yourusername/forget-to-win/discussions)
- **Bugs**: Open an [Issue](https://github.com/yourusername/forget-to-win/issues)
- **Chat**: Join our community (if applicable)

---

## ✅ Pull Request Checklist

Before submitting your PR:

- ✅ Code follows style guidelines
- ✅ Type hints and docstrings added
- ✅ Manual testing complete
- ✅ Documentation updated
- ✅ Commit messages follow format
- ✅ Branch is up-to-date with main
- ✅ PR description is clear

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Thank you for contributing to **Forget to Win**! Your contributions help make this project better for everyone.

**Happy Coding!** 🚀
