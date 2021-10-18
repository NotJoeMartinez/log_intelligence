import argparse, re, pathlib, csv
def main(args):

    logs_dir = args.nginx_logs
    parse_nginx(logs_dir)


def parse_nginx(log_path):
    path = pathlib.Path(log_path)
    for log_file in path.iterdir():
        with open(log_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                try:
                    ip = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s", line).group()
                    date = re.search("\-\s\-\s\[(.*)\+0000\]\s",line).group(1)
                    request_url = re.search("\s\"(.*)\"\s",line).group(0)
                    user_agent = re.search("\"\-\"\s\"(.*)$", line, re.DOTALL).group(1)
                    csv_row = [ip,date,request_url,user_agent]
                    print(csv_row)
                except:
                    pass

                try:
                    with open('nginx_logs.csv', 'a') as f:
                        writer_object = csv.writer(f)
                        writer_object.writerow(csv_row)
                            


                except:
                    pass





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="nginx log parser")
    parser.add_argument("-n","--nginx-logs",action="store",type=str,    help="Directory of nginx logs")
    args = parser.parse_args()

    main(args)
