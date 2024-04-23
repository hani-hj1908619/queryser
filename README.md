# SQL Query Cost Estimator

**College of Engineering**  
**Department of Computer Science and Engineering**  
**CMPS 451 – Database Management Systems**  
**Fall 2023 Course Project**

For this project, we chose PostgreSQL hosted online on Supabase as our DBMS.

## Phase 1: Mapping ER/EER Schema to Relational Database Schema

We mapped our ER/EER schema to a relational database schema. Here's the schema map:

![Schema Map](https://i.imgur.com/9VPlrWR.jpeg)

## Phase 2: Meta Data and Statistics

1. From our relational database schema, we picked two tables with at least one relationship between them.
2. For each table and their respective relationships, we stored metadata and statistics necessary for the query optimizer to choose a proper execution plan. We referred to the textbook and slides to determine the list of features to store and assumed reasonable values for each feature.
3. We arranged these statistics as relational tables and stored them in our PostgreSQL database hosted on Supabase. Our metadata is like an application hosted on the DBMS, and we connected our frontend application with the database using proper API.

![Metadata Tables](https://i.imgur.com/6bbt302.png)

## Phase 3: The Cost Estimator

1. Our cost estimator is a standalone application.
2. It accepts queries involving SELECT or JOIN operations. For SELECT operation, we focused on selection using a primary key and equality operator, selection using a primary key with range operator, selection on a non-primary key using equality operator, and selection on a non-primary key with range operator. For JOIN operation, we considered only equi-join operation.
3. We implemented a graphical user interface using the Streamlit Python framework to read the required details and provide the necessary data to our cost estimator.
4. Once the query is fed to our query estimator, it explores all possible query plans based on the form of the query and the stored statistics.
5. The output of the query estimator includes the query information and the list of possible execution plans with the estimated cost for each of them.
6. The estimator also supports utility functions such as displaying the statistics associated with relations.

## Application Description

We used the Streamlit Python framework for creating the UI, ensuring a seamless user experience. The project is containerized using Docker for portability and consistent performance. Our backend is a Postgres DB hosted on Supabase for easy access and management.

## Supported Queries

The queries currently supported include:
- Simple selection with a condition on any attribute for equality and range.
- Simple selection with multiple chained conditions using AND operator.
- Natural join query with the prior 2 types of simple selections.

## Application Preview Images

1. Simple Select Query:

    - The prompted query for a simple SELECT:
    
    ![Prompted Query](https://i.imgur.com/ZjRni0U.png)

    - SQL Query generated as per the GUI selections, with the algorithms used to execute it:
    
    ![SQL Query](https://i.imgur.com/Lg5UXuF.png)

    - List of possible execution plans with the estimated cost:
    
    ![Execution Plans](https://i.imgur.com/LjerjET.png)

For more detailed information about our project, please refer to our project report.
