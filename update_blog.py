#!/usr/bin/env python3
"""
Blog Update System for BLOGIIIIII
Converts Markdown posts to HTML and updates the main blog page
"""

import os
import re
import markdown
from datetime import datetime
import json

class BlogUpdater:
    def __init__(self):
        self.posts_dir = "posts"
        self.templates_dir = "templates"
        self.main_html = "index.html"
        self.posts_data = []
        
        # Create directories if they don't exist
        os.makedirs(self.posts_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
    
    def create_post_template(self):
        """Create a template for new blog posts"""
        template = """# My First Blog Post

**Published:** {date}
**Category:** Technology
**Read Time:** 5 min

## Introduction

This is my first blog post! I'm excited to share my thoughts and experiences with you.

## Main Content

Write your main content here. You can use:

- **Bold text**
- *Italic text*
- `Code snippets`
- [Links](https://example.com)

### Subheadings

You can create subheadings like this.

## Conclusion

Thanks for reading! Feel free to leave comments or reach out to me.

---
*This post was written in Markdown and automatically converted to HTML.*
"""
        
        template_path = os.path.join(self.posts_dir, "example-post.md")
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"Created example post template: {template_path}")
    
    def parse_markdown_post(self, file_path):
        """Parse a markdown file and extract metadata"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title (first # heading)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled Post"
        
        # Extract metadata from frontmatter or content
        date_match = re.search(r'\*\*Published:\*\* (.+)', content)
        published_date = date_match.group(1) if date_match else datetime.now().strftime("%B %d, %Y")
        
        category_match = re.search(r'\*\*Category:\*\* (.+)', content)
        category = category_match.group(1) if category_match else "General"
        
        read_time_match = re.search(r'\*\*Read Time:\*\* (.+)', content)
        read_time = read_time_match.group(1) if read_time_match else "5 min"
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc'])
        html_content = md.convert(content)
        
        # Extract excerpt (first paragraph after title)
        excerpt_match = re.search(r'<p>(.+?)</p>', html_content)
        excerpt = excerpt_match.group(1) if excerpt_match else "No excerpt available"
        
        return {
            'title': title,
            'date': published_date,
            'category': category,
            'read_time': read_time,
            'content': html_content,
            'excerpt': excerpt,
            'filename': os.path.basename(file_path),
            'slug': os.path.splitext(os.path.basename(file_path))[0]
        }
    
    def get_all_posts(self):
        """Get all markdown posts from the posts directory"""
        posts = []
        
        if not os.path.exists(self.posts_dir):
            print(f"Posts directory '{self.posts_dir}' not found!")
            return posts
        
        for filename in os.listdir(self.posts_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(self.posts_dir, filename)
                try:
                    post = self.parse_markdown_post(file_path)
                    posts.append(post)
                    print(f"Processed: {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        # Sort posts by date (newest first)
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts
    
    def generate_blog_cards(self, posts):
        """Generate HTML for blog cards"""
        if not posts:
            return """
            <article class="blog-card">
                <div class="blog-image">
                    <i class="fas fa-plus"></i>
                </div>
                <div class="blog-content">
                    <h3 class="blog-title">No Posts Yet</h3>
                    <div class="blog-meta">Start writing your first post!</div>
                    <p class="blog-excerpt">Create a .md file in the posts/ directory to get started.</p>
                    <a href="#" class="read-more">Coming Soon →</a>
                </div>
            </article>
            """
        
        cards_html = ""
        for i, post in enumerate(posts[:6]):  # Show only latest 6 posts
            # Choose icon based on category
            icon_map = {
                'technology': 'fas fa-code',
                'programming': 'fas fa-laptop-code',
                'life': 'fas fa-heart',
                'general': 'fas fa-lightbulb',
                'tutorial': 'fas fa-graduation-cap'
            }
            icon = icon_map.get(post['category'].lower(), 'fas fa-file-alt')
            
            cards_html += f"""
            <article class="blog-card">
                <div class="blog-image">
                    <i class="{icon}"></i>
                </div>
                <div class="blog-content">
                    <h3 class="blog-title">{post['title']}</h3>
                    <div class="blog-meta">Published on {post['date']} • {post['read_time']} read</div>
                    <p class="blog-excerpt">{post['excerpt']}</p>
                    <a href="#post-{post['slug']}" class="read-more">Read More →</a>
                </div>
            </article>
            """
        
        return cards_html
    
    def update_main_html(self, posts):
        """Update the main HTML file with new blog posts"""
        with open(self.main_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate new blog cards
        new_cards = self.generate_blog_cards(posts)
        
        # Replace the blog grid section
        pattern = r'(<div class="blog-grid">).*?(</div>)'
        replacement = f'\\1\n{new_cards}\n        \\2'
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # Write updated HTML
        with open(self.main_html, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"Updated {self.main_html} with {len(posts)} posts")
    
    def create_github_upload_script(self):
        """Create a script to upload to GitHub"""
        script_content = '''@echo off
echo Uploading BLOGIIIIII to GitHub...

REM Add all files
git add .

REM Commit changes
git commit -m "Update blog posts - %date% %time%"

REM Push to GitHub
git push origin main

echo Blog updated successfully!
pause
'''
        
        with open('upload_to_github.bat', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print("Created upload_to_github.bat script")
    
    def run(self):
        """Main function to update the blog"""
        print("BLOGIIIIII Update System")
        print("=" * 40)
        
        # Create example post if no posts exist
        if not os.path.exists(self.posts_dir) or not os.listdir(self.posts_dir):
            print("No posts found. Creating example post...")
            self.create_post_template()
        
        # Get all posts
        posts = self.get_all_posts()
        
        if not posts:
            print("No posts to process!")
            return
        
        # Update main HTML
        self.update_main_html(posts)
        
        # Create upload script
        self.create_github_upload_script()
        
        print("\nBlog update complete!")
        print(f"Processed {len(posts)} posts")
        print("\nNext steps:")
        print("1. Write your posts in the posts/ directory")
        print("2. Run: python update_blog.py")
        print("3. Run: upload_to_github.bat")

if __name__ == "__main__":
    updater = BlogUpdater()
    updater.run()
