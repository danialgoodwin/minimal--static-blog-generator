import json
import logging
import shutil

import css_html_js_minify
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
    <link rel="stylesheet" type="text/css" href="assets/blog.min.css">
    <link href="data:image/x-icon;base64,AAABAAEAEBAAAAAAAABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AJzn/2A+z///O8z//zfJ//80xv//nuL/L////wD///8A////AP///wD///8A////AP///wD///8A////AEnY//9F1f//QtL//z/P//87zP//Pcr///b8//8xw//7////AP///wD///8A////AP///wD///8A////AP///wBN3P//Sdn//0bV//9C0v//P8///0vQ///7/v//NMb//////wD///8A////AP///wD///8A////AP///wD///8AUN///03c//9J2f//Rtb//0PT//8/0P//PM3//zjJ//////8A////AP///wD///8A////AJ9wN/6cbjb/mWw2/1Ti//9R3///Tdz//0rZ//9G1v//Q9P//z/Q//88zf//OMr//zXH//8xw//+////AKZzN6ajcjf/oHA3/51uNv9Y5v//VOP//1Hg//9O3f//Str//0fW//9D0///QND//zzN//85yv//Ncf///X8/wSpdTf/pnM3/6NyN/+gcDf/XOn//1jm//9V4///UeD//07d//9K2v//R9f//0PT//9A0P//PM3//znK//82x///rHc3/6l1N/+mdDf/o3I3/////wBc6f//WOb//1Xj//9S4P//Tt3//0va//9H1///RNT//0DR//89zf//Ocv//7B5N/+tdzf/qnY3/6d0N/+kcjf/oHA3/51uNv+bbTb/l2s2/5RpNv+UaTb/m+r/ZEfX//9E1P//QdH//z3O//+zezf/sHk3/613N/+qdjf/p3Q3/6RyN/+hcDf/nm82/5ttNv+Yazb/lGk2/5RpNv9L2v//R9f//0TU//9B0f//tn045LN7N/+weTf/rXg3/6p2N/+ndDf/pHI3/6FxN/+ebzb/m202/5hrNv+VaTb/T97//0vb//9I1///ZNv/df///wC3fTj+tHs3/7B6N/+teDf/qnY3/6d0N/+kczf/oXE3/55vNv+bbTb/mGs2/1Ph//9P3v//TNv//////wD///8A////AP///wD///8AsXo37654N++rdjfvqHQ376VzN/+hcTf/nm82/5ttNv////8A////AP///wD///8A////AP///wD///8A////ALR8N//v5Nb/rng3/6t2N/+odTf/pXM3/6JxN/+fbzf/////AP///wD///8A////AP///wD///8A////AP///wC3fjj//////7R/Pv+ueDf/q3c3/6h1N/+lczf/onE3/////wD///8A////AP///wD///8A////AP///wD///8A////ALh+OP+1fDj/sno3/694N/+sdzf/qXU3/////wD///8A////AP///wD///8A/D8AAPAPAADwDwAA8A8AAIABAAAAAQAAAAAAAAgAAAAAEAAAAAAAAAABAACAAQAA8A8AAPAPAADwDwAA+B8AAA==" rel="icon" type="image/x-icon" />
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
    <link rel="stylesheet" type="text/css" href="../assets/blog.min.css">
    <link href="data:image/x-icon;base64,AAABAAEAEBAAAAAAAABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AJzn/2A+z///O8z//zfJ//80xv//nuL/L////wD///8A////AP///wD///8A////AP///wD///8A////AEnY//9F1f//QtL//z/P//87zP//Pcr///b8//8xw//7////AP///wD///8A////AP///wD///8A////AP///wBN3P//Sdn//0bV//9C0v//P8///0vQ///7/v//NMb//////wD///8A////AP///wD///8A////AP///wD///8AUN///03c//9J2f//Rtb//0PT//8/0P//PM3//zjJ//////8A////AP///wD///8A////AJ9wN/6cbjb/mWw2/1Ti//9R3///Tdz//0rZ//9G1v//Q9P//z/Q//88zf//OMr//zXH//8xw//+////AKZzN6ajcjf/oHA3/51uNv9Y5v//VOP//1Hg//9O3f//Str//0fW//9D0///QND//zzN//85yv//Ncf///X8/wSpdTf/pnM3/6NyN/+gcDf/XOn//1jm//9V4///UeD//07d//9K2v//R9f//0PT//9A0P//PM3//znK//82x///rHc3/6l1N/+mdDf/o3I3/////wBc6f//WOb//1Xj//9S4P//Tt3//0va//9H1///RNT//0DR//89zf//Ocv//7B5N/+tdzf/qnY3/6d0N/+kcjf/oHA3/51uNv+bbTb/l2s2/5RpNv+UaTb/m+r/ZEfX//9E1P//QdH//z3O//+zezf/sHk3/613N/+qdjf/p3Q3/6RyN/+hcDf/nm82/5ttNv+Yazb/lGk2/5RpNv9L2v//R9f//0TU//9B0f//tn045LN7N/+weTf/rXg3/6p2N/+ndDf/pHI3/6FxN/+ebzb/m202/5hrNv+VaTb/T97//0vb//9I1///ZNv/df///wC3fTj+tHs3/7B6N/+teDf/qnY3/6d0N/+kczf/oXE3/55vNv+bbTb/mGs2/1Ph//9P3v//TNv//////wD///8A////AP///wD///8AsXo37654N++rdjfvqHQ376VzN/+hcTf/nm82/5ttNv////8A////AP///wD///8A////AP///wD///8A////ALR8N//v5Nb/rng3/6t2N/+odTf/pXM3/6JxN/+fbzf/////AP///wD///8A////AP///wD///8A////AP///wC3fjj//////7R/Pv+ueDf/q3c3/6h1N/+lczf/onE3/////wD///8A////AP///wD///8A////AP///wD///8A////ALh+OP+1fDj/sno3/694N/+sdzf/qXU3/////wD///8A////AP///wD///8A/D8AAPAPAADwDwAA8A8AAIABAAAAAQAAAAAAAAgAAAAAEAAAAAAAAAABAACAAQAA8A8AAPAPAADwDwAA+B8AAA==" rel="icon" type="image/x-icon" />
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
    (post_dir / Path('index.htm')).write_text(page_html)


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
    Path(f'{POSTS_OUTPUT_DIR}/index.htm').write_text(home_page)
    shutil.copytree(ASSETS_INPUT_DIR, ASSETS_OUTPUT_DIR)

    for f in Path(POSTS_OUTPUT_DIR).rglob('*.*'):
        css_html_js_minify.minify.process_multiple_files(str(f))


def main():
    generate_site()


if __name__ == '__main__':
    main()
