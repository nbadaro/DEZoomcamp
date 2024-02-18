"""
pip install dlt[duckdb]
https://colab.research.google.com/drive/1Te-AT0lfh0GpChg1Rbd0ByEKOHYtWXfm#scrollTo=pY4cFAWOSwN1&forceEdit=true&sandboxMode=true
https://dlthub.com/docs/intro
"""
import dlt
import duckdb

db = duckdb.connect()


def square_root_generator(limit: int):
    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1


def question_1():
    """
    Q: What is the sum of the outputs of the generator for limit = 5?
    A: 8.382332347441762
    """
    limit = 5
    generator = square_root_generator(limit)
    total_sum = 0

    for sqrt_value in generator:
        total_sum += sqrt_value

    print(f'The total sum after 5 iterations is: {total_sum}')


def question_2():
    """
    Q: What is the 13th number yielded
    A: 3.605551275463989
    """
    limit = 13
    generator = square_root_generator(limit)

    for sqrt_value in generator:
        print(f"{sqrt_value}")


def question_3():
    """
    Q: Calculate the sum of all ages of people.
    A: 353
    """
    def people_1():
        for i in range(1, 6):
            yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

    for person in people_1():
        print(person)

    def people_2():
        for i in range(3, 9):
            yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}

    for person in people_2():
        print(person)

    pipeline = dlt.pipeline(
        pipeline_name="people_pipeline",
        destination='duckdb',
        dataset_name='people_data',
        credentials=db
    )

    info_1 = pipeline.run(
        people_1,
        table_name="people",
        # write_disposition="append"
    )

    info_2 = pipeline.run(
        people_2,
        table_name="people",
        # write_disposition="append"
    )

    result = db.execute(query="SELECT * FROM people_data.people")
    result_df = result.df()
    sum_age = result_df["age"].sum()

    print(sum_age)


def question_4():
    """
    Q: Calculate the sum of all ages of people.
    A: 266
    """
    def people_1():
        for i in range(1, 6):
            yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

    for person in people_1():
        print(person)

    def people_2():
        for i in range(3, 9):
            yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}

    for person in people_2():
        print(person)

    pipeline = dlt.pipeline(
        pipeline_name="people_pipeline",
        destination='duckdb',
        dataset_name='people_data',
        credentials=db
    )

    info_1 = pipeline.run(
        people_1,
        table_name="people",
        write_disposition="append"
    )

    info_2 = pipeline.run(
        people_2,
        table_name="people",
        write_disposition="merge",
        primary_key="ID"
    )

    result = db.execute(query="SELECT sum(Age) as sum_age FROM people_data.people")
    result_df = result.df()
    sum_age = result_df["age"].sum()

    print(sum_age)


if __name__ == '__main__':
    # question_1()
    # question_2()
    # question_3()
    question_4()
