# GitHub Setup Guide for AIE Portfolio Branch Strategy

## 🎯 **Overview**
This guide will help you configure GitHub settings to implement the branch strategy for your AIE Portfolio project.

## 🔧 **Step 1: Repository Settings**

### **1.1 General Settings**
1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **General** section
4. Configure:
   - **Repository name**: `aie-portfolio` (or your preferred name)
   - **Description**: `AIE Portfolio - Personal website with blog, analyzers, and development tools`
   - **Website**: `https://yourusername.github.io/aie-portfolio`
   - **Topics**: `portfolio`, `blog`, `data-analysis`, `personal-website`

### **1.2 Visibility Settings**
- **Repository visibility**: Public (for main branch)
- **Issues**: Enabled
- **Projects**: Enabled
- **Wiki**: Disabled
- **Discussions**: Disabled

## 🔐 **Step 2: Branch Protection Rules**

### **2.1 Main Branch Protection**
1. Go to **Settings** > **Branches**
2. Click **Add rule**
3. Configure:
   - **Branch name pattern**: `main`
   - **Require pull request reviews before merging**: ✅
   - **Required number of reviewers**: 1
   - **Dismiss stale PR approvals when new commits are pushed**: ✅
   - **Require status checks to pass before merging**: ✅
   - **Require branches to be up to date before merging**: ✅
   - **Restrict pushes that create files**: ✅
   - **Allow force pushes**: ❌
   - **Allow deletions**: ❌

### **2.2 Blog Branch Protection**
1. Add another rule
2. Configure:
   - **Branch name pattern**: `blog`
   - **Require pull request reviews before merging**: ✅
   - **Required number of reviewers**: 1
   - **Restrict pushes that create files**: ✅
   - **Allow force pushes**: ❌
   - **Allow deletions**: ❌

### **2.3 Analyzers Branch Protection**
1. Add another rule
2. Configure:
   - **Branch name pattern**: `analyzers`
   - **Require pull request reviews before merging**: ✅
   - **Required number of reviewers**: 1
   - **Restrict pushes that create files**: ✅
   - **Allow force pushes**: ❌
   - **Allow deletions**: ❌

### **2.4 Development Branch Protection**
1. Add another rule
2. Configure:
   - **Branch name pattern**: `development`
   - **Require pull request reviews before merging**: ✅
   - **Required number of reviewers**: 1
   - **Restrict pushes that create files**: ✅
   - **Allow force pushes**: ❌
   - **Allow deletions**: ❌

### **2.5 Docs Branch Protection**
1. Add another rule
2. Configure:
   - **Branch name pattern**: `docs`
   - **Require pull request reviews before merging**: ✅
   - **Required number of reviewers**: 1
   - **Restrict pushes that create files**: ✅
   - **Allow force pushes**: ❌
   - **Allow deletions**: ❌

## 🌐 **Step 3: GitHub Pages Configuration**

### **3.1 Main Branch Pages (Public)**
1. Go to **Settings** > **Pages**
2. Configure:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/ (root)`
   - **Custom domain**: (optional) `yourdomain.com`

### **3.2 Blog Branch Pages (Limited Access)**
1. Create a separate repository for blog: `aie-blog`
2. Configure Pages:
   - **Source**: Deploy from a branch
   - **Branch**: `blog`
   - **Folder**: `/ (root)`
   - **Access**: Private repository

### **3.3 Analyzers Branch Pages (Private)**
1. Create a separate repository for analyzers: `aie-analyzers`
2. Configure Pages:
   - **Source**: Deploy from a branch
   - **Branch**: `analyzers`
   - **Folder**: `/ (root)`
   - **Access**: Private repository

## 👥 **Step 4: Access Control**

### **4.1 Collaborators**
1. Go to **Settings** > **Manage access**
2. Click **Invite a collaborator**
3. Add collaborators with appropriate permissions:
   - **Main branch**: Read access
   - **Blog branch**: Write access (for content contributors)
   - **Analyzers branch**: Owner only
   - **Development branch**: Owner only

### **4.2 Teams (Optional)**
1. Go to **Settings** > **Manage access**
2. Click **New team**
3. Create teams:
   - **Content Team**: Blog contributors
   - **Development Team**: Code contributors
   - **Admin Team**: Full access

## 🔄 **Step 5: Workflow Configuration**

### **5.1 GitHub Actions (Optional)**
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Portfolio
on:
  push:
    branches: [ main, blog, analyzers, development, docs ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

### **5.2 Branch Policies**
1. Go to **Settings** > **Branches**
2. Set up policies for each branch:
   - **Require linear history**: ✅
   - **Require signed commits**: ❌ (optional)
   - **Require conversation resolution before merging**: ✅

## 📊 **Step 6: Monitoring & Analytics**

### **6.1 Insights**
1. Go to **Insights** tab
2. Monitor:
   - **Traffic**: Page views and unique visitors
   - **Commits**: Activity by branch
   - **Contributors**: Team activity
   - **Community**: Issues and discussions

### **6.2 Security**
1. Go to **Security** tab
2. Enable:
   - **Dependency graph**: ✅
   - **Dependabot alerts**: ✅
   - **Dependabot security updates**: ✅
   - **Code scanning**: ✅ (if available)

## 🚀 **Step 7: Deployment Scripts**

### **7.1 Create Deployment Scripts**
Use the provided `deploy_branch.bat` script for easy deployment.

### **7.2 Automated Deployment**
Set up GitHub Actions for automatic deployment on push.

## 📋 **Step 8: Testing & Validation**

### **8.1 Test Branch Protection**
1. Try to push directly to protected branches
2. Verify that pull requests are required
3. Test merge restrictions

### **8.2 Test Access Controls**
1. Verify public access to main branch
2. Test limited access to blog branch
3. Confirm private access to analyzers/development

### **8.3 Test GitHub Pages**
1. Verify main branch Pages deployment
2. Test blog branch Pages (if separate repo)
3. Confirm analyzers branch Pages (if separate repo)

## 🎯 **Success Criteria**

### **✅ Branch Strategy Working When:**
- Each branch contains only relevant content
- Branch protection rules prevent direct pushes
- Pull requests are required for changes
- Access controls work as expected
- GitHub Pages deploy correctly
- Deployment scripts work smoothly

### **✅ Benefits Achieved:**
- Clean separation of concerns
- Controlled access to different content
- Independent development workflows
- Easy maintenance and updates
- Scalable project structure

## 🔧 **Troubleshooting**

### **Common Issues:**
1. **Branch protection not working**: Check rule configuration
2. **Pages not deploying**: Verify branch and folder settings
3. **Access denied**: Check collaborator permissions
4. **Merge conflicts**: Use proper merge strategies

### **Support Resources:**
- GitHub Documentation
- Git Branching Guide
- GitHub Pages Documentation
- Community Forums

## 📚 **Next Steps**

1. **Run** `setup_branch_strategy.bat` to create branches
2. **Configure** GitHub settings as outlined above
3. **Test** the branch strategy with sample changes
4. **Train** team members on new workflows
5. **Monitor** and optimize the system

## 🎉 **Conclusion**

This branch strategy will give you:
- **Organized** project structure
- **Controlled** access to different content
- **Independent** development workflows
- **Easy** maintenance and updates
- **Scalable** architecture for growth

Your AIE Portfolio will be well-organized, secure, and ready for professional development!
