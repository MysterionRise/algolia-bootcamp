import json
import time
import datetime

if __name__ == '__main__':
    with open('data/News_Category_Dataset_v2.json', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        with open("data/news-algolia.json", "w", encoding="utf-8") as out_file:
            out_file.write("[")
            for line in lines[:-1]:
                doc = json.loads(line.strip())
                doc['timestamp'] = int(time.mktime(datetime.datetime.strptime(doc['date'], "%Y-%m-%d").timetuple()))
                out_file.write(f"{json.dumps(doc)},")
            out_file.write(lines[-1])
            out_file.write("]")

