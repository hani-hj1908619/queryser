import streamlit as st
import random, uuid, repo
from faker import Faker
from db import supabase

fake = Faker()


trade_union_uuids = [str(uuid.uuid4()) for i in range(10)]
ssn_counter = 6
email_counter = 6
phone_counter = 31000000 + random.randint(1000, 10000)
job_types = ['secretary', 'technician', 'engineer', 'manager']
pay_types = ['salaried', 'hourly']
t_grades = ['entry_level', 'junior', 'senior']
engineer_roles = ['planning', 'site', 'network', 'electrical']
sexes = ['male', 'female']


def insert_unions():
    for id in trade_union_uuids:
        name = fake.company()
        
        # Insert data into the TRADE_UNION table
        data = {'id': id,
                'name': name}
        res = repo.insert_trade_union_data(data)



def insert_employees():
    trade_unions = repo.read_trade_union_ids()
    for i in range(40):
        global ssn_counter, email_counter, phone_counter
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
        trade_union_id = random.choice(trade_unions) if pay_type == 'hourly' else None
        
        data = {'ssn': ssn,
            'email': email,
            'phone_number': phone,
            'fname': fname,
            'minit': minit,
            'lname': lname,
            'birth_date': birth_date,
            'address': address,
            'join_date': join_date,
            'job_type': job_type,
            'typing_speed': typing_speed,
            'tgrade': t_grade,
            'eng_type': eng_type,
            'pay_type': pay_type,
            'salary': salary,
            'pay_scale': pay_scale,
            'sex': sex,
            'trade_union_id': trade_union_id}
        
        res = repo.insert_employee_data(data)
            
        ssn_counter += 1
        email_counter += 1
        phone_counter += random.randint(1000, 10000)
        

        

def app():
    st.set_page_config(
        page_title="Seeding",
        page_icon="🌱",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    
    st.title('Seed')
    st.write('Here you can fill the database with random data')

    if st.button("Insert unions"):
        st.write("Inserting trade unions...")
        insert_unions()
        st.write("Unions inserted successfully!")

    if st.button("Insert Employees"):
        st.write("Inserting employees...")
        insert_employees()
        st.write("Employees inserted successfully!")

app()
