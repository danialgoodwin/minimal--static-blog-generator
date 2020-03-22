import json
import logging
import shutil

import markdown
from pathlib import Path

BLOG_TITLE = 'My Minimal Blog'
BLOG_DESCRIPTION = 'Saving bytes one blog at a time.'

POSTS_INPUT_DIR = 'posts/'
POSTS_OUTPUT_DIR = 'public/blog/'

ASSETS_INPUT_DIR = 'assets/'
ASSETS_OUTPUT_DIR = 'public/blog/assets/'

HOME_PAGE_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="Description" content="{description}">
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="assets/blog.css">
  </head>
  <body>
    <div class="blog">
      <h1>{title}</h1>
      <p>{description}</p>
      <hr>
      <h2>Recent posts:</h2>
      {posts}
    </div>
  </body>
</html>
'''

POST_PAGE_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="Description" content="{description}">
    <title>{title} - {blog_title}</title>
    <link rel="stylesheet" type="text/css" href="../assets/blog.css">
  </head>
  <body>
    <div class="blog">
      <h1><a href="../">{blog_title}</a></h1>
      <p>{description}</p>
      <hr>
      <small>{date}</small>
      {content}
    </div>
  </body>
</html>
'''


def parse_blog_post_file(file: Path) -> json:
    values = {'file': file.name, 'date': file.name[0:10], 'content': ''}
    is_content = False
    with file.open() as f:
        for i, line in enumerate(f):
            if i == 0:
                if line != '---\n':
                    logging.error(f'Missing "---" on first line in {file}')
            elif line == '---\n':
                is_content = True
            elif is_content:
                values['content'] += line
            elif ': ' in line:
                tokens = line.split(': ')
                values[tokens[0]] = tokens[1].rstrip('\n')
            else:
                logging.error(f'This syntax is not supported yet: {line}')
    values['content'] = markdown.markdown(values['content'])
    if 'slug' not in values:
        values['slug'] = file.name.lower().rstrip('.md').replace(' ', '-')
    return values


def generate_post(values: json):
    post_dir = Path(f'{POSTS_OUTPUT_DIR}/{values["slug"]}')
    post_dir.mkdir(parents=True, exist_ok=True)
    page_html = POST_PAGE_TEMPLATE.format(
        blog_title=BLOG_TITLE,
        title=values['title'],
        description=BLOG_DESCRIPTION,
        date=values['date'],
        content=values['content'])
    (post_dir / Path('index.html')).write_text(page_html)


def generate_site():
    shutil.rmtree(POSTS_OUTPUT_DIR, ignore_errors=True)
    Path(POSTS_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    posts_html = '<ul class="posts">'
    post_files = list(Path(POSTS_INPUT_DIR).glob('*.md'))
    post_files.reverse()  # Put more recent posts at the top
    for file in post_files:
        values = parse_blog_post_file(file)
        generate_post(values)
        slug = values['slug']
        posts_html += f'<li><a href="{slug}">{values["title"]}</a></li>'
    posts_html += '</ul>'
    home_page = HOME_PAGE_TEMPLATE.format(title=BLOG_TITLE, description=BLOG_DESCRIPTION, posts=posts_html)
    Path(f'{POSTS_OUTPUT_DIR}/index.html').write_text(home_page)
    shutil.copytree(ASSETS_INPUT_DIR, ASSETS_OUTPUT_DIR)


def main():
    generate_site()


if __name__ == '__main__':
    main()
