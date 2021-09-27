import requests
import json
import codecs

url = 'https://onepiece.nchu.edu.tw/cofsys/plsql/json_for_course'

def get_json_for_course(career='U'):
    if career not in ('U', 'G', 'O', 'N'):
        raise ValueError('Requesting invalid career.')
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38'})
    with open('course.json', 'w', encoding='utf-8') as f:
        f.write(r.text)

def jsonify(json_path='course.json'):
    with open(json_path, 'r', encoding='utf-8') as f:
        json_string = f.read()
        course_dict = json.loads(json_string)
    return course_dict

def standard_format():
    standard_json = {
        "_id" : 0,
        "制別" : "",
        "科目" : {
            "id" : "",
            "name" : ""
        },
        "班級" : {
            "id" : ""
        },
        "開班選課人數" : "",
        "任課教師" : {
            "正課" : [ 
                ""
            ],
            "實習" : []
        },
        "上課日期_節次" : [ 
            # {
            #     "d" : "",
            #     "t" : ""
            # }
        ],
        "年級" : "",
        "學校" : {
            "教室" : [ 
                ""
            ],
            "校區" : [ 
                ""
            ]
        },
        "選別" : "",
        "學分" : "",
        "類別" : "",
        "畢業班" : "",
        "學期數" : "",
        "說明" : ""
    }
    return standard_json

def _to_str(i):
    if i < 10:
        return '0' + str(i)
    else:
        return str(i)

def parse_to_db_format():
    courses = jsonify()
    # print(course['course'][0]['title_parsed'])
    json_for_db = []
    for course in courses:
        item = standard_format()
        item['科目']['name'] = course['title_parsed']['zh_TW']
        item['科目']['id'] = course['url']
        item['開班選課人數'] = course['number_parsed']
        item["任課教師"]["正課"] = course['professor']
        item['選別'] = course['obligatory']
        for _class in course['time_parsed']:
            item['上課日期_節次'].append({
                'd': _class['day'],
                't': ''.join(map(_to_str, _class['time']))
            })
        item['學期數'] = course['year']
        item['學分'] = course['credits']
        item['學校']['教室'] = course['location']
        item['說明'] = course['note']
        item['制別'] = course['department']
        print(item['科目']['name'])
        json_for_db.append(item)
    return json_for_db

def get_bpeecs_classes():
    courses = jsonify()
    bpeecs_classes = []
    for course in courses['course']:
        # print(course)
        if course['for_dept'] == "電機資訊學院學士班":
            bpeecs_classes.append(course)
    with codecs.open('bpeecs.json', 'w', encoding='utf-8') as f:
        json.dump(bpeecs_classes, f, indent=4, ensure_ascii=False)
