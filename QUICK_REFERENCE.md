# Git Branch Strategy - Quick Reference

## 🚀 **Quick Start**

### **1. Setup Branch Strategy**
```bash
# Run the setup script
.\setup_branch_strategy.bat
```

### **2. Deploy Changes**
```bash
# Use the deployment script
.\deploy_branch.bat
```

## 🌳 **Branch Overview**

| Branch | Purpose | Access | Content |
|--------|---------|--------|---------|
| `main` | Public portfolio | Public | Portfolio, core framework |
| `blog` | Blog content | Limited | Blog posts, management tools |
| `analyzers` | Data tools | Private | Analysis tools, CSV processor |
| `development` | Source code | Private | C++ code, Python scripts |
| `docs` | Documentation | Public | Guides, tutorials, API docs |

## 🔄 **Common Workflows**

### **Add New Blog Post**
```bash
git checkout blog
git pull origin blog
# ... create/edit post ...
git add .
git commit -m "blog: add new post about algorithms"
git push origin blog
```

### **Update Analyzer Tool**
```bash
git checkout analyzers
git pull origin analyzers
# ... update analyzer ...
git add .
git commit -m "analyzer: improve CSV processing"
git push origin analyzers
```

### **Update Core Framework**
```bash
git checkout main
git pull origin main
# ... update framework ...
git add .
git commit -m "framework: update navigation component"
git push origin main
```

### **Add New Feature**
```bash
git checkout main
git checkout -b feature/new-analyzer
# ... develop feature ...
git add .
git commit -m "feat: add JSON analyzer"
git push origin feature/new-analyzer
# Create Pull Request to merge into appropriate branch
```

## 🔐 **Access Levels**

### **Public (main, docs)**
- ✅ Anyone can view
- ✅ Portfolio showcase
- ✅ Core framework
- ✅ Documentation

### **Limited (blog)**
- 🔒 Owner + collaborators
- 🔒 Blog content
- 🔒 Management tools

### **Private (analyzers, development)**
- 🔒 Owner only
- 🔒 Data analysis tools
- 🔒 Source code

## 📁 **Content Organization**

### **Main Branch**
```
/
├── index.html              # Main hub
├── portfolio.html          # Portfolio page
├── core-framework/         # Core components
├── js-framework/           # JavaScript framework
├── scripts/                # Public scripts
└── README.md               # Main documentation
```

### **Blog Branch**
```
/
├── blogii/                 # Blog system
│   ├── index.html
│   ├── posts/
│   ├── templates/
│   └── update_blog.py
└── README_BLOG.md
```

### **Analyzers Branch**
```
/
├── analyzers/              # Analysis tools
│   ├── index.html
│   ├── csv-analyzer.html
│   ├── csv-analyzer-js.html
│   └── css/
└── README_ANALYZERS.md
```

### **Development Branch**
```
/
├── code/                   # Source code
│   ├── cpp/
│   ├── python/
│   └── data/
└── README_DEVELOPMENT.md
```

## 🛠️ **Useful Commands**

### **Branch Management**
```bash
# List all branches
git branch -a

# Switch to branch
git checkout <branch-name>

# Create new branch
git checkout -b <new-branch-name>

# Delete branch
git branch -d <branch-name>
```

### **Deployment**
```bash
# Deploy specific branch
git checkout <branch-name>
git pull origin <branch-name>
git add .
git commit -m "deploy: update <branch-name>"
git push origin <branch-name>
```

### **Merge Changes**
```bash
# Merge feature branch
git checkout main
git merge feature/new-feature
git push origin main
```

## 📋 **Best Practices**

### **Commit Messages**
- Use conventional commits: `feat:`, `fix:`, `docs:`, `style:`
- Be descriptive and clear
- Reference issues when applicable

### **Branch Naming**
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `release/version` - Release preparation

### **Code Review**
- Review all changes before merging
- Test changes locally first
- Document complex changes
- Maintain code quality

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Merge conflicts**: Resolve conflicts before merging
2. **Access denied**: Check branch protection rules
3. **Pages not updating**: Verify GitHub Pages settings
4. **Branch not found**: Check if branch exists remotely

### **Emergency Procedures**
1. **Revert changes**: `git revert <commit-hash>`
2. **Reset branch**: `git reset --hard <commit-hash>`
3. **Force push**: `git push --force-with-lease origin <branch>`

## 📞 **Support**

- **Documentation**: See `BRANCH_STRATEGY.md`
- **GitHub Setup**: See `GITHUB_SETUP_GUIDE.md`
- **Git Help**: `git help <command>`
- **GitHub Docs**: https://docs.github.com

## 🎯 **Success Metrics**

- ✅ Clean separation of content
- ✅ Controlled access levels
- ✅ Independent development workflows
- ✅ Easy maintenance and updates
- ✅ Scalable project structure

---

**Remember**: This branch strategy is designed to keep your project organized, secure, and scalable. Follow the workflows and best practices for optimal results!
