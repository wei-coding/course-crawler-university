def clean_class_fmt(class_string,order):
    ans = []
    if "\xa0" in class_string:
        l_split = class_string.split("\xa0")
        for s in l_split:
            data = s.replace(" ", "").replace("節","").replace("星期","").split(":")
            ans.append({"d":data[0],"t":data[1]})
    else:
        data = class_string.replace(" ", "").replace("節","").replace("星期","").split(":")
        ans.append({"d":data[0],"t":data[1]})
    ordered_ans = []
    # remake class_time by order
    for k in range(1,-1,-1):
        for i in range(len(ans)):
            if i<len(order) and order[i] == k:
                ordered_ans.append(ans[i])

    return ordered_ans

def clean_space(class_string):
    class_string = class_string.replace("/", "／")
    data = class_string.split(" ")
    try:
        ans = {"id":data[0],"name":data[1]}
    except:
        ans = {"id":data[0]}
    return ans

def clean_special_char(input_string):
    return input_string.replace("／", "_").replace(" ", "")


def clean_teacher(teacher_string):
    teacher_dict = {} # teacher_object
    teacher_dict["正課"] = []
    teacher_dict["實習"] = []
    # exception (school's source_data have no </td> tag)
    if "星期" in teacher_string:
        teacher_string = teacher_string[0:teacher_string.find("星期")]

    # chk the teacher's order
    order = []
    for i in range(len(teacher_string)):
        if teacher_string[i:i+2] == "正課":
            order.append(1)
        elif teacher_string[i:i+2] == "實習":
            order.append(0)

    # split teachers
    ll = teacher_string.split("正課: ")
    for ele in ll:
        list2 = ele.split("實習: ")
        teacher_dict["正課"].append(''.join([i for i in list2[0] if i.isalpha()])) # clear \n \t
        if len(list2)>1:
            teacher_dict["實習"].append(''.join([i for i in list2[1] if i.isalpha()])) 
           
    # clean null ele in list
    teacher_dict["正課"] = [i for i in teacher_dict["正課"] if i]
    teacher_dict["實習"] = [i for i in teacher_dict["實習"] if i]
    teacher_dict["order"] = order

    return teacher_dict
  
def clean_campus(campus_string):
    campus_lst = campus_string.strip().replace("】",".").replace("【",".").replace(" ","").split(".")
    obj_lst = {}
    obj_lst["教室"] = []
    obj_lst["校區"] = []
    

    for e in campus_lst:
        if (e==""):
            continue
        if ('A'<=e[0] and e[0]<='Z'):
            obj_lst["教室"].append(e)
        else:
            obj_lst["校區"].append(e)
    
    return obj_lst