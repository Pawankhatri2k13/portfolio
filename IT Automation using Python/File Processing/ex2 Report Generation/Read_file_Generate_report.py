
import csv

csv.register_dialect('empDialect', skipinitialspace=True,strict=True)

def read_employees(csv_file_location):
    with open(csv_file_location) as openedFile:
        reader = csv.DictReader(openedFile,dialect='empDialect')
        employee_list = []
        for data in reader:
            employee_list.append(data)
    return employee_list


employee_list = read_employees('./employees.txt')
employee_list[0]

def process_data(employee_list):
    department_list = []
    for employee_data in employee_list:
        department_list.append(employee_data['Department'])
        
    department_data = {}
    for department_name in set(department_list):
        department_data[department_name] = department_list.count(department_name)
    
    return department_data

dictionary = process_data(employee_list)
print(dictionary)

def write_report(dictionary, report_file):
    with open(report_file, 'w+') as f:
        for k in sorted(dictionary):
            f.write(str(k)+':'+str(dictionary[k])+'\n')
            
write_report(dictionary,'./report.txt')