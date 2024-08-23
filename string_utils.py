

def is_valid_paper_format(paper):
    FLAGS = ['Title:', 'Authors:', 'Categories:']
    for flag in FLAGS:
        if flag not in paper:
            return False
    return True


def get_keywords(filename='./keywords.txt') -> str:
    def read_file_to_list(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
        return lines

    FILTER_TEXT = read_file_to_list(filename)
    print(f'Select papers with keywords: {FILTER_TEXT}')
    return FILTER_TEXT


def read_file_to_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()
    return lines


def handle_header(header):
    # 앞에 내용은 필요 없음.
    header = header.split('Title:')[1]
    title, header = header.split('Authors:')
    if 'Categories:' in header:
        authors, header = header.split('Categories:')
        if 'Comments:' in header:
            categories, comments = header.split('Comments:')
        else:
            categories = header
            comments = None
    elif 'Comments' in header:
        authors, comments = header.split('Comments:')
    else:
        authors = header
        comments = None
        
   
    
    title = title.replace('\r\n', ' ').strip()
    authors = authors.replace('\r\n', ' ').strip()
    if comments is not None:
        comments = comments.replace('\r\n', ' ').strip()
    
    return title, authors, comments

def handle_abstract(abstract):
    abstract = abstract.replace('\r\n', ' ').strip()
    return abstract

def handle_link(link):
    link = link.split(',')[0].strip()
    link = link.replace('( ', '')
    return link

def make_context(papers):
    SPLIT = "<p>------------------------------------------------------------------------------</p>"
    html_body = """
<html>
<body>"""
    for paper in papers:
        html_body += f'{SPLIT}{paper}'
        
    html_body += """
</body>
</html>"""
    return html_body