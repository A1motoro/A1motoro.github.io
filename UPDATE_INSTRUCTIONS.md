# 🚀 Quick Update Instructions

## Manual Update Steps

Since the terminal is having issues, here's how to update your repository manually:

### Option 1: Using GitHub Desktop (Recommended)
1. Open GitHub Desktop
2. Select your AIE repository
3. Review all changes
4. Add commit message: "Add core framework and reorganize structure with Monokai theming"
5. Click "Commit to main"
6. Click "Push origin"

### Option 2: Using Command Line (Alternative)
1. Open Command Prompt or PowerShell
2. Navigate to your AIE folder: `cd D:\AIE`
3. Run these commands:
   ```bash
   git add .
   git commit -m "Add core framework and reorganize structure with Monokai theming"
   git push origin main
   ```

### Option 3: Using the Update Scripts
I've created two update scripts for you:

#### Windows Batch Script:
- Double-click `one_click_update.bat`
- This will automatically update and push everything

#### PowerShell Script:
- Right-click `one_click_update.ps1`
- Select "Run with PowerShell"
- This provides better error handling and colored output

## What's Being Updated

Your repository now includes:

✅ **Core Framework** (`core-framework/`)
- Protected Monokai theme system
- Reusable navigation and footer components
- Security configuration

✅ **Updated Pages**
- Main portfolio (`index.html`) - Now uses core framework
- Blog (`blogii/index.html`) - Updated with Monokai theme
- Data analysis (`data-analysis/csv-analyzer.html`) - Updated with Monokai theme

✅ **New Documentation**
- `STRUCTURE_INTRO.md` - Complete structure guide
- `UPDATE_INSTRUCTIONS.md` - This file
- Updated README files

✅ **Update Scripts**
- `one_click_update.bat` - Windows batch script
- `one_click_update.ps1` - PowerShell script

## After Pushing

Once you push these changes:
1. Your website will be live at: https://a1motoro.github.io
2. All pages will have consistent Monokai theming
3. Core framework will be protected
4. You can use the update scripts for future changes

## Future Updates

Use the `one_click_update.bat` or `one_click_update.ps1` scripts for quick updates:
- They automatically add, commit, and push changes
- They include error handling
- They provide status updates
- They work for the entire repository (not just blog)

Your repository is now professionally organized and ready to go! 🎉
