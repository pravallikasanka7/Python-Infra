import os
import yaml
import re
import json

directory = "task"
c=1
task_list_indirect_image=[]
task_list_without_tag=[]
break_point=0
for task_folder in os.listdir(directory):
  task_folder = os.path.join(directory, task_folder)
  if os.path.isfile(task_folder):
     continue
  else:
      for task_version_folder in os.listdir(task_folder):
         task_version_folder = os.path.join(task_folder, task_version_folder)
         if os.path.isfile(task_version_folder):
            continue
         else:
            print("c",c)
            c=c+1
            for task_file in os.listdir(task_version_folder):
                  if(".yaml" in task_file):
                     print(task_file)
                     task_file = os.path.join(task_version_folder, task_file)
                     try:
                      with open(task_file, 'r') as file:
                          task_data = yaml.load(file, Loader=yaml.UnsafeLoader)
                     except yaml.scanner.ScannerError as e:
                       print("task skipped due to yaml scan error")
                     for i in range(len(task_data["spec"]["steps"])):
                        image_name_tag=task_data["spec"]["steps"][i]["image"]
                        print(image_name_tag)
                        if("$" in image_name_tag ):
                           task_list_indirect_image.append(task_file)
                        else:
                              if("@" in image_name_tag):
                                 image_name_tag_list=(re.split('@', image_name_tag))
                              elif(":" in image_name_tag):
                                 image_name_tag_list=(re.split(':', image_name_tag))
                              else:
                                 task_list_without_tag.append(task_file)
                                 break;
                              image_name = image_name_tag_list[0]
                              image_tag = image_name_tag_list[1]
                              image_file = image_name.split("/")
                              image_org = image_file[1]
                              image_file=image_file[-1]+".json"
                              image_path="image-task-map-json"
                              pwd=str(os.getcwd())
                              print(pwd)
                              image_full_path=os.path.join(pwd, image_path)
                              image_full_path=image_full_path+"/"+image_org
                              print("i",i)
                              if not os.path.exists(image_full_path):
                                      os.mkdir(image_full_path) 
                              image_file_path = image_full_path+"/"+image_file
                              if image_file in os.listdir(image_full_path):
                                 print("exists")
                                 with open(image_file_path) as image_task:
                                     image_task_data = json.load(image_task)
                                 print(image_task_data[image_name][0])
                                 if(task_file in image_task_data[image_name][0].keys()):
                                     l=image_task_data[image_name][0][task_file]
                                 else:
                                     l=[]
                                 if(i not in l):
                                      l.append(i)
                                 image_task_data[image_name][0][task_file]=l
                                 print(image_task_data[image_name][0][task_file])
                                 print(image_task_data)
                                 with open(image_file_path, 'w') as image_task:
                                      json.dump(image_task_data, image_task)
                              else:
                                 image_dictionary={}
                                 image_dictionary[image_name]=[]
                                 image_dictionary[image_name].append({})
                                 image_dictionary[image_name].append(image_tag)
                                 image_dictionary[image_name][0][task_file]=[]
                                 image_dictionary[image_name][0][task_file].append(i)
                                 print(image_dictionary)
                                 with open(image_file_path, 'w') as image_task:
                                    json.dump(image_dictionary, image_task)
print("indirect: " , len(task_list_indirect_image))
task_list_indirect_image_path="pipeline/image-task-map-json/task_list_indirect_image.json"
with open(task_list_indirect_image_path, 'w') as indirect_image_list_task:
   json.dump(task_list_indirect_image, indirect_image_list_task)
print(len(task_list_without_tag))
