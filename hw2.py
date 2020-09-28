from path import Path
from typing import Union, List, Tuple, Dict

class Company():
    
    def __init__(self):
        
        self.departments = {}
        self.workers = []
        self.csv_separator = ';'
        self.print_separator = '  --  '
        self.csv_header = self.csv_separator.join(['Dept.', '# Workers', 'Min. Salary', 'Max. Salary', 'Avg. Salary'])
        self.print_header = self.print_separator.join(['\nDept.', '# Workers', 'Min. Salary', 'Max. Salary', 'Avg. Salary'])
        self.filename = './company_report.csv'
        
    def add_instance(self, record: dict) -> None:
        """
        adding new record about worker into Company's structure
        """
        
        dept_name = record['dept']
        
        if self.departments.get(dept_name, None) is not None:
            
            self.departments[dept_name].add_worker(record['salary'])
            
        else:
            
            dept = Department(dept_name)
            dept.add_worker(record['salary'])
            self.departments[dept_name] = dept
            
        self.workers.append(record)
            
    def list_departments(self):
        """
        lists all departments
        """
        
        print("\nCurrent departments are:")
        print('\n'.join(sorted(self.departments.keys())))
        
        
    def get_report(self) -> None:
        
        """
        prints departments report
        """
        
        print(self.print_header)
        
	for dept_name, dept in self.departments.items():
		
            stats = dept.get_salary_stats()
            print(self.print_separator.join([f'{dept.name :<11}', str(dept.count)]) + self.print_separator +\
                  self.print_separator.join([f'{s:.2f}' for s in stats]))
            
            
    def write_report(self) -> None:
        
        """
        writes departments report into csv-file
        """
        
        with open(self.filename, 'w', encoding = 'utf-8') as f:
        
            print(self.csv_header, file = f)
        
	    for dept_name, dept in self.departments.items():
			
                stats = dept.get_salary_stats()

                print(self.csv_separator.join([f'{dept.name:<11}', str(dept.count)]) + self.csv_separator +\
                      self.csv_separator.join([f'{s:.2f}' for s in stats]), file = f)
                
        print(f'\n File saved to {self.filename}')

class Department():
    
    def __init__(self, name: str):
        
        self.name = name
        self.count = 0
        self.salaries = []
        
    def add_worker(self, salary: float) -> None:
        
        """
        adds worker's salary to Department info
        """
        
        self.count += 1
        self.salaries.append(salary)
        
    def get_salary_stats(self) -> Tuple:
        
        """ 
        returns min, max and avg salary within department
        """
        
        total_salary_volume = sum(self.salaries)
        
        return min(self.salaries), max(self.salaries), total_salary_volume / self.count
        
def parse_line(line, main_separator: str = ';', add_separator: str = ' -> ') -> Dict:
    
    """
    parses line from input data into record's dictionary
    """
    
    name, job, dept, grade, salary =  line.rstrip().split(main_separator)
    
    record = {}
    
    record['name'] = name.strip()
    record['job'] = job.strip()
    record['grade'] = float(grade.strip())
    record['salary'] = float(salary.strip())
    
    dept_parts = dept.split(add_separator)
    
    if len(dept_parts) > 1:

        record['dept'] = dept_parts[0].strip()
        record['team'] = dept_parts[1].strip()

    else:
        record['dept'] = dept_parts[0].strip()
        record['team'] = None
    
    return record
	
	
	
def load_data(filepath: Union[str, Path], encoding: str  = 'utf-8'):
    """
    takes path to file with records in format 
    '
    ФИО полностью
    Занимаемая должность
    Подразделение, включая всю иерархию
    Квартальная оценка – результат ревью
    Текущая зарплата
    '
    and returns Company's instance
    """    
    with open(filepath, 'r', encoding = 'utf-8') as f:

        lines = f.readlines()

        company = Company()

        for line in lines[1:]:

            record = parse_line(line)

            company.add_instance(record)
    
    return company
	
	
	
	
DEP_SEP = ' -> '
FILEPATH = Path('./funcs_homework_employees_sample.csv')

if __name__ == '__main__':

    company = load_data(FILEPATH, DEP_SEP)
    
    while True:

        input_s = input('\nType 1 if you wanna see all departments\nType 2 if you wanna print report on departments\n'
                    'Type 3 if you wanna save report to csv-file\nType 4 if you wanna quit\n')

        try:
            input_s = int(input_s)

        except ValueError:
            print('Please, type value from 1 to 4')

        if input_s == 4:
            break
            
        elif input_s == 1:
            company.list_departments()

        elif input_s == 2:
            company.get_report()

        elif input_s == 3:
            company.write_report()

        else:
            print('Please, type value from 1 to 4')
