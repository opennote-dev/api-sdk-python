from opennote import OpennoteClient
from os import getenv
from json import dumps
import time

client = OpennoteClient(api_key=getenv("OPENNOTE_API_KEY"))

SEPERATOR = "================================\n"

if __name__ == "__main__":
    print(SEPERATOR)
    print("Creating Practice Problem Set...")

    response = client.practice.create(
        set_description="Linear algebra concepts including matrices, eigenvalues, and vector spaces",
        count=3,
        set_name="Linear Algebra Practice",
        search_for_problems=True,
    )

    print("\nPractice Set Creation Response:")
    print(dumps(response.model_dump(), indent=4))

    print(SEPERATOR)

    status_check_count = 0
    if response.success:
        while True:
            print(SEPERATOR)
            print(f"Checking Practice Set Status (#{status_check_count})...")
            status = client.practice.status(response.set_id)
            
            print("\n", dumps(status.model_dump(), indent=4))
            print(SEPERATOR)
            
            if status.status == "pending":
                time.sleep(10)
                status_check_count += 1
                continue
            else:
                break
    
    print(SEPERATOR)
    print("Practice Set Final Status\n")
    print(dumps(status.model_dump(), indent=4))
    print(SEPERATOR)

    if status.success and hasattr(status, 'practice_problems') and status.practice_problems:
        print(SEPERATOR)
        print("Grading Example - First Problem...")
        
        first_problem = status.practice_problems[0]
        
        first_problem.student_answer = "A matrix is a rectangular array of numbers. Eigenvalues are scalar values that represent how a matrix transforms vectors."
        
        grade_response = client.practice.grade(first_problem)
        
        print("\nGrading Response:")
        print(dumps(grade_response.model_dump(), indent=4))
        print(SEPERATOR)