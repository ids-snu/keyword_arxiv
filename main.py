
import os
from datetime import datetime

from email_utils import fetch_email_details, send_email
from string_utils import (
    is_valid_paper_format,
    get_keywords,
    handle_header,
    handle_abstract,
    handle_link,
    make_context,
)
from paper import PaperClass

def main():
    
    username = os.environ.get('arxiv_email_username')
    password = os.environ.get('arxiv_email_password')

    email_text = fetch_email_details(username, password)
    if email_text is None:
        print("No email found.")
    else:
        print("Email found.")

    # 아카이브 구독 메일 형식
    papers = email_text.split("------------------------------------------------------------------------------")
    papers = [paper for paper in papers if is_valid_paper_format(paper)]
    print(f'Full papers: {len(papers)}') 
    
    # 찾고싶은 키워드들 리스트로 가져옴.
    FILTER_TEXT = get_keywords()
    
    selected_papers = list()
    for paper in papers:
        for text in FILTER_TEXT:
            if text in paper:
                selected_papers.append(paper)
                break
    print(f'Selected papers with keywords: {len(selected_papers)}')

            
    papers_class_list = list()
    for index, selected_paper in enumerate(selected_papers):
        selected_paper_str_list = selected_paper.split('\\')
        header = selected_paper_str_list[2]
        abstract = selected_paper_str_list[4]
        selected_paper_str_list = selected_paper_str_list[4:]
        for selected_paper_str in selected_paper_str_list:
            if 'https://arxiv.org/abs/' in selected_paper_str:
                link = selected_paper_str
                break   


        title, authors, comments = handle_header(header)
        filtered_abstract = handle_abstract(abstract)
        filtered_link = handle_link(link)

        paper = PaperClass(title=title, authors=authors, abstract=filtered_abstract, comments=comments, link=filtered_link, keywords=FILTER_TEXT)
        papers_class_list.append(paper)


    date = datetime.today().strftime("%Y-%m-%d")
    subject = f"My arXiv papers ({date})"
    html_body = make_context(papers_class_list)

    # 선택된 논문들 리스트를 이메일로 보냄
    send_email(subject=subject, html_body=html_body, to_email=username, from_email=username, from_email_password=password)



if __name__ == '__main__':
    main()