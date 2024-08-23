import os
import imaplib
import email
import chardet
import smtplib
from email.policy import default
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def extract_text(msg):
    email_text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset()
                if charset is None:
                    charset = 'utf-8'
                email_text = part.get_payload(decode=True)
                result = chardet.detect(email_text)
                email_text = email_text.decode(result['encoding'])
                break
    else:
        email_text = msg.get_payload(decode=True)
        result = chardet.detect(email_text)
        email_text = email_text.decode(result['encoding'])
    return email_text


def fetch_email_details(username, password, mail_server="imap.naver.com", latest_count=20):
    mail = imaplib.IMAP4_SSL(mail_server)
    try:
        mail.login(username, password)
    except Exception as e:
        os.system(f'curl -d "Failed to login : {username}" ntfy.sh/hjkim-arxiv')

    
    mail.select("inbox")

    result, data = mail.search(None, 'ALL')
    assert result == 'OK', "Error fetching email"
    email_indices = data[0].split()
    print(f'Searched {len(email_indices)} emails. Use the latest {latest_count} emails....')
    email_indices = email_indices[-latest_count:]
    email_indices.reverse()
    
    email_text = None
    for email_index in email_indices:
        result, data = mail.fetch(email_index, '(RFC822)')
        assert result == 'OK', "Error fetching email"

        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email, policy=default)
        
        from_email = msg['From']
        subject = msg['Subject']
        
        if 'cs daily' in subject.lower():
            print(f'Found arXiv email from index {email_index}.')
            email_text = extract_text(msg)
            mail.logout()
            return email_text
        
    print('Cannot find arXiv email.')
    mail.logout()
    return email_text

def send_email(subject, html_body, to_email, from_email, from_email_password):
    # 이메일 메시지 생성
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    

    # MIMEText 객체에 HTML 본문을 추가
    msg.attach(MIMEText(html_body, "html"))
    
    try:
        # 네이버 SMTP 서버에 연결
        server = smtplib.SMTP('smtp.naver.com', 587)
        server.starttls()  # TLS 사용
        server.login(from_email, from_email_password)  # 로그인
        
        # 이메일 보내기
        server.send_message(msg)
        print("이메일이 성공적으로 전송되었습니다.")
        
    except Exception as e:
        os.system(f'curl -d "Failed send email : {to_email}" ntfy.sh/hjkim-arxiv')
    else:
        os.system(f'curl -d "Arxiving Success : {to_email}" ntfy.sh/hjkim-arxiv')
    finally:
        server.quit()  # 서버 연결 종료