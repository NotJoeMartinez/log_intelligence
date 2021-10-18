import os, re, subprocess, sqlite3, sys, random
import requests

def main():
    uniqe_ips = "[path/to/log_text_file.txt]"
    make_db()
    check_webserver(uniqe_ips)
    

def make_db():
     # make tables
    con = sqlite3.connect('ipinfo.db')
    cur = con.cursor()
    sql = 'CREATE TABLE if not exists ips (ip text, is_web_server text, html text);'
    cur.execute(sql)
    con.commit()
    con.close()



def add_ip_to_db(ip, is_webserver, html):
    # add stuff into database
    con = sqlite3.connect('ipinfo.db')
    cur = con.cursor()
    cur = con.execute("INSERT INTO ips values(?, ?, ?)", (ip,is_webserver,html))
    con.commit()
    con.close()

# progress bar
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def check_webserver(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        random.shuffle(lines)
        for count, ip in enumerate(lines):
            ip = ip.strip()
            
            progress(count,len(lines))

            try:
                resp = requests.get(f"http://{ip}", timeout=1)
                html = resp.text
                add_ip_to_db(ip,"true",html)
                with open("scanner.log", "a") as f:
                    f.write(ip+"\n")

            except requests.exceptions.RequestException as e: 
                add_ip_to_db(ip,"false", "")

                with open("scanner.log", "a") as f:
                    f.write(ip+"\n")

                pass
            

if __name__ == '__main__':
    main()
