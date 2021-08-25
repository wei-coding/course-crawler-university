"""
search_table.py
"""
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

print(__doc__)

def get_class_search_json_table():
    print("making class search table...",end="")
    # params-ch(學期) d(department)
    d_res = requests.get('https://www.mcu.edu.tw/student/new-query/sel-6-1.asp', params={"ch":0})
    d_res.encoding = 'big5-hkscs'
    d_soup = BeautifulSoup(d_res.text, 'html.parser')
    d_name_tags =  d_soup.find_all('td',align="left")
    d_id_tags =  d_soup.find_all('td', align="center")

    d_names = [] # department_list
    for t in d_name_tags:
        d_names.append(t.text.strip())

    d_ids = []
    def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)

    for t in d_id_tags:
        if hasNumbers(t.text.strip()):
            d_ids.append(t.text.strip())

    # link name and id to dict
    dict_names_ids = dict(zip(d_ids, d_names))
    df = pd.DataFrame(list(zip(d_ids, d_names)), columns=['class_id', "class_name"])
    with open('data/department_ids_names.json', 'w+') as fp:
        json.dump(dict_names_ids, fp)
    print("done.")
    return d_ids



def get_name_search_json_table(d_ids):
    print("找班級...",end="")
    class_ids = []
    class_has_meeting_ids = []
    q_class_session = requests.session()
    i=0
    for d_id in d_ids:
        #找班級代碼
        q_res = q_class_session.get('https://www.mcu.edu.tw/student/new-query/sel-6-2.asp', params={"ch":2, "tdept":d_id})
        q_res.encoding = 'big5-hkscs'
        q_soup = BeautifulSoup(q_res.text, 'html.parser')
        class_tags = q_soup.findAll('a')
        q_class_meet = requests.session()
        for t in class_tags:
            class_id = t.text
            class_ids.append(class_id)
            # 找班會
            q_res = q_class_meet.get('https://www.mcu.edu.tw/student/new-query/sel-6-3.asp', params={"ch":2, "tempno":t.text})
            q_res.encoding = 'big5-hkscs'
            q_soup2 = BeautifulSoup(q_res.text, 'html.parser')
            class_meeting = q_soup2.find('td', text = re.compile('班會'))
            if class_meeting!=None:
                class_meeting_id = class_meeting.find_parent().a.text
                #print("*",class_id, end="")
                percentage = int(i/334.0*100)
                print("[%d%%]"%(percentage),"="*percentage,end="⭐️\r")
                class_has_meeting_ids.append(class_id)
                i+=1
            
    print("\ndone.")
    print("課程數：", len(class_ids))
    print("班級數：", len(class_has_meeting_ids))

    print("找姓名...")
    student_names = []
    student_ids = []
    q_student_session = requests.session()
    for c_id in class_has_meeting_ids:
        d_res = q_student_session.get('https://www.mcu.edu.tw/student/new-query/sel-6-4.asp', params={"ch":2, "text0":c_id, "text3":"00997"})
        d_res.encoding = 'big5-hkscs'
        d_soup = BeautifulSoup(d_res.text, 'html.parser')
        if d_soup.table!=None:
            ids_tags = d_soup.table.findAll("td", bgcolor="DBFDFF")

            for t_id in ids_tags:
                name = t_id.next_sibling.text
                student_names.append(name)
            for t_id in ids_tags:
                student_ids.append(t_id.text)
    #print(len(student_names), len(student_ids))
    print("學生數：",len(student_names))
    dict_students = dict(zip(student_ids,student_names))
    with open('data/students_ids_names.json', 'w+') as fp:
        json.dump(dict_students, fp)

# get_name_search_json_table(get_class_search_json_table())