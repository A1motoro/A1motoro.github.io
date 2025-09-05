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
    
    def get_categories(self, posts):
        """Extract unique categories from posts"""
        categories = {}
        for post in posts:
            category = post['category'].lower()
            if category not in categories:
                categories[category] = {
                    'name': post['category'],
                    'count': 0,
                    'posts': []
                }
            categories[category]['count'] += 1
            categories[category]['posts'].append(post)
        return categories
    
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
            <a href="posts/{post['slug']}.html" class="blog-card">
                <div class="blog-image">
                    <i class="{icon}"></i>
                </div>
                <div class="blog-content">
                    <h3 class="blog-title">{post['title']}</h3>
                    <div class="blog-meta">Published on {post['date']} • {post['read_time']} read</div>
                    <p class="blog-excerpt">{post['excerpt']}</p>
                    <div class="read-more">Read More →</div>
                </div>
            </a>
            """
        
        return cards_html
    
    def generate_post_html(self, post, categories=None):
        """Generate HTML for individual post using enhanced Monokai theme template"""
        if not os.path.exists(self.post_template):
            print(f"Template not found: {self.post_template}")
            return
        
        with open(self.post_template, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Generate dynamic categories HTML
        categories_html = ""
        if categories:
            for category_name, category_data in categories.items():
                category_slug = category_name.lower().replace(' ', '-')
                categories_html += f'<a href="category-{category_slug}.html" class="sidebar-tag">{category_data["name"]}</a>\n                            '
        
        html = template.format(
            title=post['title'],
            date=post['date'],
            category=post['category'],
            read_time=post['read_time'],
            content=post['content'],
            excerpt=post['excerpt'],
            categories_html=categories_html.strip()
        )
        
        output_path = os.path.join(self.posts_dir, f"{post['slug']}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated: {output_path}")
    
    def generate_category_page(self, category_name, category_data):
        """Generate HTML for a category page"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} - BLOGIIIIII</title>
    <meta name="description" content="All posts in the {category_name} category">
    <meta name="keywords" content="blog, {category_name}, programming, development">
    <meta name="author" content="A1m">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="../css/monokai-theme.css" rel="stylesheet">
</head>
<body>
    <header>
        <nav class="container">
            <a href="../index.html" class="logo">BLOGIIIIII</a>
            <ul class="nav-links">
                <li><a href="../index.html#home">Home</a></li>
                <li><a href="../index.html#featured">Featured</a></li>
                <li><a href="../index.html#blog">Blog</a></li>
                <li><a href="../index.html#about">About</a></li>
                <li><a href="../index.html#contact">Contact</a></li>
            </ul>
            <div class="mobile-menu">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </nav>
    </header>
    <section class="main-content">
        <div class="container">
            <a href="index.html" class="back-link">← Back to All Posts</a>
            <h2 class="section-title">{category_name} Posts ({category_data['count']})</h2>
            <div class="posts-list">
"""
        
        for post in category_data['posts']:
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

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2024 BLOGIIIIII. All rights reserved.</p>
            <p>Made with ❤️ and lots of coffee</p>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        const mobileMenu = document.querySelector('.mobile-menu');
        const navLinks = document.querySelector('.nav-links');

        if (mobileMenu && navLinks) {
            mobileMenu.addEventListener('click', () => {
                navLinks.classList.toggle('active');
            });
        }

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView(true);
                }
            });
        });

        // Add scroll effect to header
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (header) {
                if (window.scrollY > 100) {
                    header.style.background = 'rgba(39, 40, 34, 0.98)';
                } else {
                    header.style.background = 'rgba(39, 40, 34, 0.95)';
                }
            }
        });
    </script>
</body>
</html>"""
        
        output_path = os.path.join(self.posts_dir, f"category-{category_name.lower().replace(' ', '-')}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated category page: {output_path}")
    
    def update_main_html(self, posts):
        """Update the main HTML file with new blog posts"""
        with open(self.main_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate new blog cards
        new_cards = self.generate_blog_cards(posts)
        
        # Replace the blog grid section completely
        # Find the start and end of the blog-grid div (more specific pattern)
        pattern = r'(<div class="blog-grid">[\s\S]*?)(?=</div>\s*</div>\s*</section>)'
        replacement = f'<div class="blog-grid">\n{new_cards}\n            </div>'
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
    <link href="../css/monokai-theme.css" rel="stylesheet">
</head>
<body>
    <header>
        <nav class="container">
            <a href="../index.html" class="logo">BLOGIIIIII</a>
            <ul class="nav-links">
                <li><a href="../index.html#home">Home</a></li>
                <li><a href="../index.html#featured">Featured</a></li>
                <li><a href="../index.html#blog">Blog</a></li>
                <li><a href="../index.html#about">About</a></li>
                <li><a href="../index.html#contact">Contact</a></li>
            </ul>
            <div class="mobile-menu">
                <span></span>
                <span></span>
                <span></span>
            </div>
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

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2024 BLOGIIIIII. All rights reserved.</p>
            <p>Made with ❤️ and lots of coffee</p>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        const mobileMenu = document.querySelector('.mobile-menu');
        const navLinks = document.querySelector('.nav-links');

        mobileMenu.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Add scroll effect to header
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (window.scrollY > 100) {
                header.style.background = 'rgba(39, 40, 34, 0.98)';
            } else {
                header.style.background = 'rgba(39, 40, 34, 0.95)';
            }
        });
    </script>
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
        
        # Get categories
        categories = self.get_categories(posts)
        
        # Generate individual post HTMLs
        for post in posts:
            self.generate_post_html(post, categories)
        
        # Generate category pages
        for category_name, category_data in categories.items():
            self.generate_category_page(category_name, category_data)
        
        # Update main HTML
        self.update_main_html(posts)
        
        # Update posts index
        self.update_posts_index(posts)
        
        # Create upload script
        self.create_github_upload_script()
        
        print("\nBlog update complete!")
        print(f"Processed {len(posts)} posts")
        print(f"Generated {len(categories)} category pages")
        print("\nCategories found:")
        for category_name, category_data in categories.items():
            print(f"  - {category_data['name']}: {category_data['count']} posts")
        print("\nNext steps:")
        print("1. Write your posts in the posts/ directory as .md files")
        print("2. Run: python update_blog.py")
        print("3. Run: upload_to_github.bat")

if __name__ == "__main__":
    updater = BlogUpdater()
    updater.run()
