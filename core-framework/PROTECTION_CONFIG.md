# Core Framework Protection Configuration

## 🔒 PROTECTED CORE FRAMEWORK

This directory contains the core framework components that should only be modified by the repository owner (a1motoro).

### Protected Files:
- `themes/monokai-core.css` - Core theme system
- `components/navigation.html` - Navigation component
- `components/footer.html` - Footer component
- `PROTECTION_CONFIG.md` - This file

### Protection Rules:

1. **Branch Protection**: Core framework files should be protected on the main branch
2. **Review Required**: Any changes to core files require owner approval
3. **Status Checks**: All CI/CD checks must pass before merging
4. **Restrictions**: Only repository owner can push directly to main branch

### How to Set Up Protection:

1. Go to GitHub repository settings
2. Navigate to "Branches" section
3. Add rule for "main" branch:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1 required)
   - ✅ Dismiss stale PR approvals when new commits are pushed
   - ✅ Require status checks to pass before merging
   - ✅ Restrict pushes that create files matching core-framework/**

### Core Framework Benefits:

- **Consistency**: All pages use the same Monokai theme
- **Maintainability**: Centralized styling and components
- **Security**: Protected from unauthorized modifications
- **Scalability**: Easy to add new pages with consistent theming

### Usage Guidelines:

- Always use `monokai-core.css` for styling
- Include core components via JavaScript fetch
- Follow Monokai color palette variables
- Test changes on development branch first

### Emergency Access:

If core framework needs immediate updates:
1. Create hotfix branch from main
2. Make necessary changes
3. Create PR with detailed explanation
4. Merge after review

---
**⚠️ WARNING**: Modifying core framework files without proper authorization may break site consistency and user experience.
