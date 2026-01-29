# Development Process Document
## Forget to Win - Development Workflow & Best Practices

---

**Document Version**: 1.0  
**Last Updated**: January 29, 2026  
**Status**: ✅ Approved  
**Owner**: Development Team  
**Related Documents**: Architecture (`docs/architecture/index.md`), Testing (`docs/testing/index.md`)

---

## 📋 Document Information

| Field | Value |
|-------|-------|
| **Product Name** | Forget to Win |
| **Development Methodology** | Agile + Iterative |
| **Version Control** | Git |
| **Development Status** | v1.0 Production Ready |

---

## 🎯 Development Philosophy

### **Core Principles**

1. **Simplicity First** - Start simple, add complexity only when needed
2. **User-Centric** - Every feature serves user needs
3. **Quality Over Speed** - Working software > rushed features
4. **Documentation as Code** - Document while developing
5. **Test-Driven Mindset** - Think about testing from day one

---

## 🔄 Development Workflow

### **Phase 1: Planning & Design** 📋

#### **Step 1.1: Requirements Gathering**
```
Input: User needs, market research
Output: PRD (Product Requirements Document)
Duration: 1-2 weeks
```

**Activities**:
- ✅ Define product vision
- ✅ Create user personas
- ✅ Document functional requirements
- ✅ Define success metrics

**Deliverables**:
- `docs/prd/index.md`

---

#### **Step 1.2: Architecture Design**
```
Input: PRD
Output: Architecture Document
Duration: 1 week
```

**Activities**:
- ✅ Design system architecture
- ✅ Choose technology stack
- ✅ Define module boundaries
- ✅ Create data flow diagrams

**Deliverables**:
- `docs/architecture/index.md`

---

#### **Step 1.3: UX Design**
```
Input: PRD, Architecture
Output: UX Design Document
Duration: 1 week
```

**Activities**:
- ✅ Create visual design system
- ✅ Design layout patterns
- ✅ Create user flow wireframes
- ✅ Define accessibility standards

**Deliverables**:
- `docs/ux-design/index.md`

---

### **Phase 2: Implementation** 💻

#### **Step 2.1: Setup Development Environment**

**Tools Required**:
```bash
# Python
python --version  # 3.8+

# Virtual Environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Dependencies
pip install rich

# Version Control
git init
git add .
git commit -m "Initial commit"
```

---

#### **Step 2.2: Module Development**

**Development Order**:
1. **Data Layer** (`item_pool.py`)
   - Define data models
   - Create item themes
   - Implement selection logic

2. **Game Engine** (`game_engine.py`)
   - Implement scoring logic
   - Create level management
   - Build UI components

3. **Application Layer** (`main.py`)
   - Implement game loop
   - Handle user input
   - Coordinate modules

4. **Demo/Testing** (`demo.py`)
   - Create component demos
   - Interactive testing

---

#### **Step 2.3: Coding Standards**

**Python Style Guide**:
```python
# 1. Type Hints (Always)
def calculate_score(correct: int, total: int) -> float:
    return (correct / total) * 100

# 2. Docstrings (Always)
def get_rank(score: int) -> str:
    """
    Determine player rank based on score.
    
    Args:
        score: Total game score (0-100)
    
    Returns:
        Rank name (e.g., "Zen Master")
    """
    pass

# 3. Constants (UPPER_CASE)
MAX_LEVELS = 5
POINTS_PER_CORRECT = 10

# 4. Class Names (PascalCase)
class GameEngine:
    pass

# 5. Function Names (snake_case)
def calculate_level_score():
    pass

# 6. Private Methods (leading underscore)
def _internal_helper():
    pass
```

---

#### **Step 2.4: Git Workflow**

**Branch Strategy**:
```
main (production)
  ├── develop (integration)
  │   ├── feature/scoring-system
  │   ├── feature/item-pool
  │   └── feature/ui-components
  └── hotfix/critical-bug
```

**Commit Message Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Examples**:
```bash
# Feature
git commit -m "feat(scoring): add streak bonus calculation"

# Bug fix
git commit -m "fix(input): handle empty recall input"

# Documentation
git commit -m "docs(readme): add installation instructions"

# Refactor
git commit -m "refactor(engine): extract scoring to separate class"

# Test
git commit -m "test(scoring): add unit tests for edge cases"
```

---

### **Phase 3: Testing** 🧪

#### **Step 3.1: Manual Testing**
```
Input: Implemented features
Output: Test results
Duration: Ongoing
```

**Testing Checklist**:
- ✅ Run `python demo.py` - All demos work
- ✅ Run `python main.py` - Full game playthrough
- ✅ Test invalid inputs - Error handling works
- ✅ Test edge cases - All correct, all wrong, etc.
- ✅ Cross-platform - Windows, macOS, Linux

---

#### **Step 3.2: Automated Testing (v1.1+)**

**Unit Tests**:
```python
# tests/test_scoring.py
import pytest
from game_engine import ScoreCalculator

def test_perfect_score():
    base, bonus, total = ScoreCalculator.calculate_level_score(5, 5, 0, 2)
    assert total == 70

def test_accuracy():
    accuracy = ScoreCalculator.calculate_accuracy(4, 5, 1, 4)
    assert accuracy == pytest.approx(77.8, 0.1)
```

**Run Tests**:
```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

---

### **Phase 4: Documentation** 📚

#### **Step 4.1: Code Documentation**

**Inline Comments**:
```python
# Good: Explain WHY, not WHAT
# Calculate streak bonus to reward consistent performance
streak_bonus = base_score * (streak * 0.2)

# Bad: Obvious comment
# Multiply base_score by streak times 0.2
streak_bonus = base_score * (streak * 0.2)
```

**Docstrings**:
```python
def calculate_level_score(
    correct_good: int,
    total_good: int,
    remembered_bad: int,
    streak: int
) -> Tuple[int, int, int]:
    """
    Calculate score for a completed level.
    
    The scoring system rewards remembering good items and
    penalizes forgetting good items or remembering bad items.
    Streak bonuses encourage consistent performance.
    
    Args:
        correct_good: Number of good items correctly remembered
        total_good: Total number of good items shown
        remembered_bad: Number of bad items incorrectly remembered
        streak: Current streak count (consecutive levels with 80%+ accuracy)
    
    Returns:
        Tuple of (base_score, streak_bonus, total_score)
        
    Examples:
        >>> calculate_level_score(5, 5, 0, 2)
        (50, 20, 70)
        
        >>> calculate_level_score(3, 5, 2, 0)
        (14, 0, 14)
    """
    pass
```

---

#### **Step 4.2: External Documentation**

**Documentation Checklist**:
- ✅ `README.md` - User guide
- ✅ `docs/prd/index.md` - Product requirements
- ✅ `docs/architecture/index.md` - System architecture
- ✅ `docs/ux-design/index.md` - UX design
- ✅ `docs/testing/index.md` - Testing strategy
- ✅ `docs/deployment/index.md` - Deployment guide
- ✅ `VISUAL_REFERENCE.md` - Mockups & code
- ✅ `QUICK_REFERENCE.md` - Cheat sheet

---

### **Phase 5: Deployment** 🚀

#### **Step 5.1: Pre-Release Checklist**

```
□ All tests pass (29/29)
□ Documentation complete
□ Cross-platform tested
□ Performance benchmarks met
□ No critical bugs
□ Version number updated
□ Release notes prepared
□ LICENSE file included
```

---

#### **Step 5.2: Release Process**

**Version Tagging**:
```bash
# Tag version
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

**GitHub Release**:
1. Go to repository → Releases → New Release
2. Select tag: v1.0.0
3. Title: "Forget to Win v1.0.0"
4. Add release notes
5. Attach files (ZIP, executables)
6. Publish release

---

#### **Step 5.3: Distribution**

**Current (v1.0)**:
```bash
# Source distribution
zip -r forget-to-win-v1.0.0.zip forgetwingame/
```

**Future (v1.1+)**:
```bash
# PyPI distribution
python -m build
twine upload dist/*

# Users install via
pip install forget-to-win
```

---

## 🛠️ Development Tools

### **Required Tools**

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Python 3.8+** | Runtime | https://python.org |
| **pip** | Package manager | Included with Python |
| **Git** | Version control | https://git-scm.com |
| **VS Code** | Code editor | https://code.visualstudio.com |
| **Rich** | Terminal UI | `pip install rich` |

---

### **Recommended VS Code Extensions**

```json
{
  "recommendations": [
    "ms-python.python",           // Python support
    "ms-python.vscode-pylance",   // Type checking
    "njpwerner.autodocstring",    // Docstring generator
    "eamodio.gitlens",            // Git integration
    "streetsidesoftware.code-spell-checker"  // Spell check
  ]
}
```

---

### **Development Scripts**

**Create `scripts/dev.sh`**:
```bash
#!/bin/bash
# Development helper script

case "$1" in
  "test")
    python demo.py
    ;;
  "play")
    python main.py
    ;;
  "lint")
    pylint *.py
    ;;
  "format")
    black *.py
    ;;
  *)
    echo "Usage: ./dev.sh {test|play|lint|format}"
    ;;
esac
```

---

## 📊 Development Metrics

### **Code Quality Metrics**

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Lines of Code** | <2,000 | ~1,200 | ✅ |
| **Functions** | <100 | ~45 | ✅ |
| **Cyclomatic Complexity** | <10 | ~5 avg | ✅ |
| **Type Coverage** | >80% | ~90% | ✅ |
| **Docstring Coverage** | 100% | 100% | ✅ |

---

### **Development Velocity**

| Phase | Duration | Status |
|-------|----------|--------|
| **Planning** | 2 weeks | ✅ Complete |
| **Design** | 1 week | ✅ Complete |
| **Implementation** | 3 weeks | ✅ Complete |
| **Testing** | 1 week | ✅ Complete |
| **Documentation** | 1 week | ✅ Complete |
| **Total** | **8 weeks** | ✅ v1.0 Released |

---

## 🔄 Iterative Development

### **Version Roadmap**

#### **v1.0 (Current)** ✅
- Core gameplay (5 levels)
- 8 item themes
- Scoring with streaks
- 6 rank tiers
- Terminal UI
- Complete documentation

#### **v1.1 (Planned - Q1 2026)**
- High score persistence
- Unit tests (pytest)
- Sound effects
- Custom difficulty
- Statistics export

#### **v1.2 (Planned - Q2 2026)**
- Daily challenge mode
- Achievement system
- More item themes (12 total)
- Color theme customization

#### **v2.0 (Future - Q3 2026)**
- Multiplayer mode
- Online leaderboards
- Web version
- Mobile support (Termux)

---

## 🐛 Bug Tracking

### **Issue Template**

```markdown
## Bug Report

**Description**: Brief description of the bug

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- Python Version: 3.11
- Rich Version: 13.0.0

**Screenshots**: (if applicable)

**Additional Context**: Any other relevant information
```

---

### **Bug Priority Levels**

| Priority | Description | Response Time |
|----------|-------------|---------------|
| **P0 - Critical** | Game crashes, data loss | Immediate |
| **P1 - High** | Major feature broken | 1-2 days |
| **P2 - Medium** | Minor feature issue | 1 week |
| **P3 - Low** | Cosmetic, nice-to-have | Next release |

---

## 🔍 Code Review Process

### **Review Checklist**

**Functionality**:
- ✅ Code works as intended
- ✅ Edge cases handled
- ✅ Error handling present

**Code Quality**:
- ✅ Follows coding standards
- ✅ Type hints present
- ✅ Docstrings complete
- ✅ No code duplication

**Testing**:
- ✅ Manual testing done
- ✅ Test cases added (if applicable)
- ✅ No regressions

**Documentation**:
- ✅ README updated (if needed)
- ✅ Comments added for complex logic
- ✅ API docs updated

---

## 📚 Learning Resources

### **For New Developers**

1. **Start Here**:
   - Read `README.md`
   - Read `docs/architecture/index.md`
   - Run `python demo.py`

2. **Understand the Code**:
   - `item_pool.py` - Data management
   - `game_engine.py` - Core logic
   - `main.py` - Game loop

3. **Make Changes**:
   - Add new item theme
   - Modify scoring formula
   - Create new UI component

---

### **Python Best Practices**

**Resources**:
- [PEP 8](https://pep8.org/) - Style Guide
- [PEP 484](https://www.python.org/dev/peps/pep-0484/) - Type Hints
- [Real Python](https://realpython.com/) - Tutorials
- [Rich Docs](https://rich.readthedocs.io/) - Terminal UI

---

## ✅ Development Checklist

### **Before Starting Development**
- ✅ Read PRD
- ✅ Understand architecture
- ✅ Setup development environment
- ✅ Create feature branch

### **During Development**
- ✅ Write type hints
- ✅ Add docstrings
- ✅ Test as you go
- ✅ Commit frequently

### **Before Submitting**
- ✅ Run manual tests
- ✅ Update documentation
- ✅ Write commit message
- ✅ Create pull request (if team)

---

## 🎯 Success Criteria

### **Definition of Done**

A feature is "done" when:
- ✅ Code is written and works
- ✅ Type hints and docstrings added
- ✅ Manual testing complete
- ✅ Documentation updated
- ✅ Code reviewed (if team)
- ✅ Merged to develop branch

---

## 📞 Support

### **Getting Help**

| Question Type | Resource |
|---------------|----------|
| **How to use** | `README.md` |
| **How it works** | `docs/architecture/index.md` |
| **How to test** | `docs/testing/index.md` |
| **How to deploy** | `docs/deployment/index.md` |
| **Bug report** | GitHub Issues |

---

## 📅 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | Development Team | Initial development process document |

---

**Document Status**: ✅ Approved  
**Next Review Date**: Q2 2026  
**Maintained By**: Development Team

---

*This development process document represents the complete development workflow for Forget to Win. Follow these practices for consistent, high-quality development.*
