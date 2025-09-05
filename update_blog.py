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
        self.posts_index = os.path.join(self.posts_dir, "index.html")
        self.post_template = os.path.join(self.templates_dir, "post_template.html")
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
        
        # Replace {date} placeholder with current date
        current_date = datetime.now().strftime("%B %d, %Y")
        content = content.replace('{date}', current_date)
        
        # Extract title (first # heading)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled Post"
        
        # Extract metadata from frontmatter or content
        date_match = re.search(r'\*\*Published:\*\* (.+)', content)
        published_date = date_match.group(1) if date_match else current_date
        
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
                    <a href="posts/{post['slug']}.html" class="read-more">Read More →</a>
                </div>
            </article>
            """
        
        return cards_html
    
    def generate_post_html(self, post):
        """Generate HTML for individual post using template"""
        if not os.path.exists(self.post_template):
            print(f"Template not found: {self.post_template}")
            return
        
        with open(self.post_template, 'r', encoding='utf-8') as f:
            template = f.read()
        
        html = template.format(
            title=post['title'],
            date=post['date'],
            category=post['category'],
            read_time=post['read_time'],
            content=post['content']
        )
        
        output_path = os.path.join(self.posts_dir, f"{post['slug']}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated: {output_path}")
    
    def update_main_html(self, posts):
        """Update the main HTML file with new blog posts"""
        with open(self.main_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate new blog cards
        new_cards = self.generate_blog_cards(posts)
        
        # Replace the blog grid section completely
        # Find the start and end of the blog-grid div
        pattern = r'(<div class="blog-grid">[\s\S]*?</div>)'
        replacement = f'<div class="blog-grid">\n{new_cards}\n</div>'
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # If no match, perhaps append it, but assuming it exists
        with open(self.main_html, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"Updated {self.main_html} with {len(posts)} posts")
    
    def update_posts_index(self, posts):
        """Generate or update posts/index.html with list of all posts"""
        # Basic template for posts/index.html
        # You can make this more sophisticated
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Blog Posts - BLOGIIIIII</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Add styles here similar to above -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.6;
            color: #f8f8f2;
            background: #272822;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        header {
            background: rgba(39, 40, 34, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid #49483e;
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #a6e22e;
            text-decoration: none;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: #f8f8f2;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: #66d9ef;
        }

        .main-content {
            padding: 120px 0 80px;
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
            color: #f8f8f2;
        }

        .posts-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }

        .post-item {
            background: #3e3d32;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #49483e;
        }

        .post-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            border-color: #a6e22e;
        }

        .post-title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #f8f8f2;
        }

        .post-meta {
            color: #a6e22e;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .post-excerpt {
            color: #e6db74;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        .read-more {
            color: #66d9ef;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .read-more:hover {
            color: #f92672;
        }

        .back-link {
            display: inline-block;
            margin-bottom: 2rem;
            color: #66d9ef;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .back-link:hover {
            color: #a6e22e;
        }

        .no-posts {
            text-align: center;
            padding: 4rem 2rem;
            background: #3e3d32;
            border-radius: 15px;
            border: 1px solid #49483e;
        }

        .no-posts h3 {
            color: #f8f8f2;
            margin-bottom: 1rem;
        }

        .no-posts p {
            color: #e6db74;
            margin-bottom: 2rem;
        }

        .create-post {
            display: inline-block;
            background: #a6e22e;
            color: #272822;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .create-post:hover {
            background: #66d9ef;
            transform: translateY(-2px);
        }

        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .posts-list {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav class="container">
            <a href="../index.html" class="logo">BLOGIIIIII</a>
            <ul class="nav-links">
                <li><a href="../index.html#home">Home</a></li>
                <li><a href="../index.html#blog">Blog</a></li>
                <li><a href="../index.html#about">About</a></li>
                <li><a href="../index.html#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    <section class="main-content">
        <div class="container">
            <a href="../index.html" class="back-link">← Back to Home</a>
            <h2 class="section-title">All Blog Posts</h2>
            <div class="posts-list">
"""
        if not posts:
            html += """
                <div class="no-posts">
                    <h3>No Posts Yet</h3>
                    <p>You haven't written any blog posts yet. Start creating content to see your posts here!</p>
                    <a href="#" class="create-post">Create Your First Post</a>
                </div>
"""
        else:
            for post in posts:
                html += f"""
                <div class="post-item">
                    <h3 class="post-title">{post['title']}</h3>
                    <div class="post-meta">Published: {post['date']} • Category: {post['category']} • {post['read_time']} read</div>
                    <p class="post-excerpt">{post['excerpt']}</p>
                    <a href="{post['slug']}.html" class="read-more">Read Full Post →</a>
                </div>
"""
        
        html += """
            </div>
        </div>
    </section>
</body>
</html>
"""
        with open(self.posts_index, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Updated {self.posts_index}")
    
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
        if not os.path.exists(self.posts_dir) or not [f for f in os.listdir(self.posts_dir) if f.endswith('.md')]:
            print("No posts found. Creating example post...")
            self.create_post_template()
        
        # Get all posts
        posts = self.get_all_posts()
        
        if not posts:
            print("No posts to process!")
            return
        
        # Generate individual post HTMLs
        for post in posts:
            self.generate_post_html(post)
        
        # Update main HTML
        self.update_main_html(posts)
        
        # Update posts index
        self.update_posts_index(posts)
        
        # Create upload script
        self.create_github_upload_script()
        
        print("\nBlog update complete!")
        print(f"Processed {len(posts)} posts")
        print("\nNext steps:")
        print("1. Write your posts in the posts/ directory as .md files")
        print("2. Run: python update_blog.py")
        print("3. Run: upload_to_github.bat")

if __name__ == "__main__":
    updater = BlogUpdater()
    updater.run()
