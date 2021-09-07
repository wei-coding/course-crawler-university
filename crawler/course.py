import requests
import json

url = 'https://onepiece.nchu.edu.tw/cofsys/plsql/json_for_course'

def get_json_for_course(career='U'):
    if career not in ('U', 'G', 'O', 'N'):
        raise ValueError('Requesting invalid career.')
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38'})
    with open('course.json', 'w', encoding='utf-8') as f:
        f.write(r.text)

def jsonify(json_path='course.json'):
    with open(json_path, 'r') as f:
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
            {
                "d" : "",
                "t" : ""
            }
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