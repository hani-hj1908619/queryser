import random, json, os, uuid
from faker import Faker
fake = Faker()
trade_union_uuids = [str(uuid.uuid4()) for _ in range(10)]
trade_unions = []
ssn_counter = 6
email_counter = 6
phone_counter = 31000000 + random.randint(1000, 10000)
job_types = ['secretary', 'technician', 'engineer', 'manager']
pay_types = ['salaried', 'hourly']
t_grades = ['entry_level', 'junior', 'senior']
engineer_roles = ['planning', 'site', 'network', 'electrical']
sexes = ['male', 'female']
employees = []

for trade_union_id in trade_union_uuids:
    trade_union_name = fake.company()

    trade_unions.append({
        'id': trade_union_id,
        'name': trade_union_name
        })
print(f"Created {len(trade_union_uuids)} rows into for TRADE UNION table.")


for i in range(40):
    ssn = f'{ssn_counter:03d}-{(ssn_counter+1)%10}{(ssn_counter+2)%10}{(ssn_counter+3)%10}-{(ssn_counter+4)%10}{(ssn_counter+5)%10}{(ssn_counter+6)%10}{(ssn_counter+7)%10}'
    email = f'employee{email_counter}@example.com'
    phone = f'+974{phone_counter:08d}'
    
    fname = fake.first_name()
    minit = fake.random_letter()
    lname = fake.last_name()
    birth_date = fake.date_of_birth().strftime('%Y-%m-%d')
    address = fake.address().replace('\n', ', ')
    join_date = fake.date_this_decade().strftime('%Y-%m-%d')
    job_type = random.choice(job_types)
    typing_speed = random.randint(40, 100) if job_type == 'secretary' else None
    t_grade = random.choice(t_grades) if job_type == 'technician' else None
    eng_type = random.choice(engineer_roles) if job_type == 'engineer' else None
    pay_type = 'hourly' if random.random() < 0.25 else 'salaried'
    salary = round(random.uniform(3000, 10000), 2) if pay_type == 'salaried' else None
    pay_scale = round(random.uniform(25, 100), 2) if pay_type == 'hourly' else None
    sex = random.choice(sexes)
    trade_union_id = random.choice(trade_union_uuids) if pay_type == 'hourly' else None
    # Insert data into the EMPLOYEE table
    # supabase.table('EMPLOYEE').insert().execute()
    
    employees.append({
        "SSN": ssn,
        "EMAIL": email,
        "PHONE": phone,
        "FNAME": fname,
        "MINIT": minit,
        "LNAME": lname,
        "BDATE": birth_date,
        "ADDRESS": address,
        "JOIN_DT": join_date,
        "JOB_TYPE": job_type,
        "TYPING_SPEED": typing_speed,
        "TGRADE": t_grade,
        "ENG_TYPE": eng_type,
        "PAY_TYPE": pay_type,
        "SALARY": salary,
        "PAY_SCALE": pay_scale,
        "SEX": sex,
        "TRADE_UNION_ID": trade_union_id
    })
    ssn_counter += 1
    email_counter += 1
    phone_counter += random.randint(1000, 10000)

print(f"Created {len(employees)} rows for the EMPLOYEE table.\n")

#? store the data as JSON objects in JSON file to be extracted later
import json
with open('data.json', 'w') as outfile:
    json.dump(employees, outfile)
    
with open('data.json', 'a') as outfile:
    json.dump(trade_unions, outfile)

def extract(list):
    values=""
    for data in list:
        values += "("
        for key, value in data.items():
            if isinstance(value, str):
                values = values + f"'{value}',"
            else:
                values = values + f"{value},"
        values = values[:-1] + f"),"
    values = values[:-2] + ";"
    return values

print(extract(trade_unions))
#! print(extract(employees))
with open('data.txt', 'w') as outfile:
    json.dump(extract(employees) , outfile)
