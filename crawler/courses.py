import requests
from bs4 import BeautifulSoup
import json
import re
import pymongo
from crawler.utils.format import *
def mongoClient(doc):
    db_client = pymongo.MongoClient("mongodb://localhost:27017/")
    if 'MCU_CourseDB' not in db_client.list_database_names():
        mydb = db_client["MCU_CourseDB"]
    mycol = mydb[doc]
    #  remove data if old.exist
    if doc in mydb.list_collection_names():
        mycol.drop()
    return mycol
    
def get_courses():
    mycol = None
    print("get courses and save to database...")
    ## Crawler - all校區 ##
    url_base = "https://www.mcu.edu.tw/student/new-query/sel-query/qslist.asp"
    res = requests.get(url_base)
    res.encoding = 'big5-hkscs'
    soup = BeautifulSoup(res.text, 'html.parser')
    select_tags = soup.find_all("select")
    select_tag = ""
    for s_tag in select_tags:
        if s_tag["name"]=="sch":
            select_tag = s_tag
            break
    q_list = []
    if select_tag['name']=="sch":
        options_tags = select_tag.find_all("option")
        for o_tag in options_tags:
            ans = o_tag['value']
            if ans.isnumeric():
                q_list.append(ans)

    ## MongoClient ##
    mycol = mongoClient("courses")

    ## Crawler - CourseData ##
    url_c = "https://www.mcu.edu.tw/student/new-query/sel-query/qslist_1.asp"
    request_session = requests.session()

    # 上下學期 (1,2)
    for ggdb in range(1,3):
    # 迭代 qlist(校區) generate all data
        for q in q_list:
            # make col_names(欄位標題)
            data = {"sch":q}
            cookies = {"ggdb": str(ggdb)}
            c_res = requests.post(url_c, data=data, cookies=cookies)
            c_res.encoding = 'big5-hkscs'
            c_soup = BeautifulSoup(c_res.text, 'html.parser')
            c_tr_tags = c_soup.find_all('tr')
            c_idx_tags = c_tr_tags[0].find_all('td')
            col_names = []
            for name in c_idx_tags:
                col_names.append(clean_special_char(name.text.strip()))

            # add course_obj(課程資料) to course_data(list)
            course_data = []
            for course_tags in c_tr_tags[1:]:
                course_obj = {}
                i=0
                isnot_meet = True   # 班週會判斷
                order = []
                for c_col in course_tags.find_all('td'):
                    write_data = c_col.text.strip()
                    if col_names[i] in ["班級","科目"]:
                        course_obj[ col_names[i] ] = clean_space(write_data)
                        try:
                            if course_obj[col_names[i]]["name"] =="週會" or course_obj[col_names[i]]["name"] == "班會":
                                isnot_meet = False
                        except:
                            pass
                    elif col_names[i] == "任課教師":
                        if isnot_meet:
                            obj = clean_teacher(c_col.text)
                            order = obj["order"]
                            del obj["order"]
                            course_obj[col_names[i]] = obj
                    elif col_names[i] == "教室【校區】":
                        obj_lst = clean_campus(c_col.text)
                        course_obj[ "學校" ] = obj_lst
                        #course_obj[ col_names[i] ] = obj_lst
                    elif col_names[i] == "上課日期_節次":
                        if isnot_meet:
                            course_obj[ col_names[i] ] = clean_class_fmt(write_data,order)
                    else:
                        course_obj[col_names[i]] = write_data
                    i+=1
                if isnot_meet:
                    course_data.append(course_obj)
            #insert to database
            mycol.insert_many(course_data)


