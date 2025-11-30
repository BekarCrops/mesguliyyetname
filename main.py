import os
import re
from datetime import datetime
import yaml


def define_env(env):
    @env.macro
    def list_posts():

        posts_dir = os.path.join(env.project_dir, 'docs', 'bend')

        yaml_front_matter_re = re.compile(r'^---\s*$(.*?)^---\s*$', re.MULTILINE | re.DOTALL)
        
        posts = []

        for root, _, files in os.walk(posts_dir):
            for filename in files:
                if filename.endswith('.md'):
                    filepath = os.path.join(root, filename)

                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        match = yaml_front_matter_re.match(content)
                        metadata = {}

                        if match:
                            front_matter_text = match.group(1)
                            metadata = yaml.safe_load(front_matter_text) or {}

                            slug = os.path.splitext(filename)[0]
                            page_url = f"/bend/{slug}/"

                            title = metadata.get('title')
                            date_str = metadata.get('date')

                            if date_str:
                                sort_date = datetime.strptime(date_str, '%Y-%m-%d')
                            else:
                                continue

                            posts.append({
                                'title': title,
                                'date': sort_date,
                                'url': page_url
                            })

                    except Exception as e:
                        print(f"Error processing file {filepath}: {e}")
        
        posts.sort(key=lambda post: post['date'], reverse=True)

        markdown_output = []

        for post in posts:
            markdown_output.append(
                f"- [{post['title']}]({post['url']})"
            )

        return "\n".join(markdown_output)

