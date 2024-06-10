import streamlit as st
from constraint import Problem, AllDifferentConstraint
import pandas as pd

def generate_timetable(courses, teachers, days_per_course):
    # Initialize the problem
    problem = Problem()

    # Define time slots
    days = ["Sun", "Mon", "Tue", "Wed", "Thu"]
    slots_per_day = {
        "Sun": 5, "Mon": 5, "Tue": 3, "Wed": 5, "Thu": 5
    }
    time_slots = []
    for day in days:
        for slot in range(1, slots_per_day[day] + 1):
            time_slots.append(f"{day}_{slot}")

    # Define variables and domains
    for course in courses:
        allowed_slots = [slot for slot in time_slots if slot.split('_')[0] in days_per_course[course]]
        if "TP" in teachers[course]:
            problem.addVariables([f"{course}_lecture", f"{course}_TD", f"{course}_TP"], allowed_slots)
        else:
            problem.addVariables([f"{course}_lecture", f"{course}_TD"], allowed_slots)

    # Hard Constraints

    # Four or five successive slots of work are not accepted (max three successive slots)
    def max_three_successive(*args):
        slots = sorted([int(slot.split('_')[1]) for slot in args])
        return all(abs(slots[i] - slots[i-1]) <= 1 for i in range(1, len(slots))) and len(slots) <= 3

    for course in courses:
        if "TP" in teachers[course]:
            problem.addConstraint(max_three_successive, [f"{course}_lecture", f"{course}_TD", f"{course}_TP"])
        else:
            problem.addConstraint(max_three_successive, [f"{course}_lecture", f"{course}_TD"])

    # Lectures of the same course should not be scheduled in the same slot
    for course in courses:
        if "TP" in teachers[course]:
            problem.addConstraint(lambda lecture, td, tp: lecture != td and lecture != tp and td != tp, (f"{course}_lecture", f"{course}_TD", f"{course}_TP"))
        else:
            problem.addConstraint(lambda lecture, td: lecture != td, (f"{course}_lecture", f"{course}_TD"))

    # Different courses for the same group must have different slot allocations
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            problem.addConstraint(AllDifferentConstraint(), [f"{courses[i]}_lecture", f"{courses[j]}_lecture"])
            problem.addConstraint(AllDifferentConstraint(), [f"{courses[i]}_TD", f"{courses[j]}_TD"])
            if "TP" in teachers[courses[i]] and "TP" in teachers[courses[j]]:
                problem.addConstraint(AllDifferentConstraint(), [f"{courses[i]}_TP", f"{courses[j]}_TP"])

    # Soft Constraints

    # Each teacher should have a maximum of two days of work
    def max_two_days(*args):
        days = [slot.split('_')[0] for slot in args]
        return len(set(days)) <= 2

    # Add the max_two_days constraint for each teacher's courses
    for course, teacher_list in teachers.items():
        if "TP" in teacher_list:
            problem.addConstraint(max_two_days, [f"{course}_lecture", f"{course}_TD", f"{course}_TP"])
        else:
            problem.addConstraint(max_two_days, [f"{course}_lecture", f"{course}_TD"])

    # Solve the problem
    solution = problem.getSolution()
    return solution

# Streamlit UI
st.title("Timetable Scheduler for Semester 2 1CS")

# Default courses and predefined teacher names
default_courses = [
    "Securite", "MethodesFormelles", "NumericalAnalysis", "Entrepreneuriat", 
    "RechercheOperationnelle2", "DistributedArchitecture", "Reseaux2", "ArtificialIntelligence"
]
default_teacher_names = {
    "Securite": ["Dr. Alkama"], 
    "MethodesFormelles": ["Dr. Isaadi"], 
    "NumericalAnalysis": ["Prof. Bechar"], 
    "Entrepreneuriat": ["Dr. Zenadji"], 
    "RechercheOperationnelle2": ["Dr. Lekhali"], 
    "DistributedArchitecture": ["Dr. Zedek"], 
    "Reseaux2": ["Dr. Djennadi", "Dr. Kaci", "Prof. Djennan", "Dr. Djerbi"], 
    "ArtificialIntelligence": ["Prof. Zaidi", "Dr. Isaadi", "Dr. Kaci"]
}
days = ["Sun", "Mon", "Tue", "Wed", "Thu"]

# User input for courses
courses = st.multiselect("Select Courses", options=default_courses, default=default_courses)

# User input for days for each selected course
teachers = {}
days_per_course = {}
for course in courses:
    selected_days = st.multiselect(f"Select Days for {course}", options=days, default=days)
    teachers[course] = default_teacher_names[course]
    days_per_course[course] = selected_days

if st.button("Generate Timetable"):
    solution = generate_timetable(courses, teachers, days_per_course)
    
    if solution:
        st.write("Generated Timetable:")
        timetable_data = []
        for var, slot in solution.items():
            course, class_type = var.split('_')
            timetable_data.append((course, class_type, slot))
        
        df = pd.DataFrame(timetable_data, columns=["Course", "Class Type", "Time Slot"])
        st.table(df)
    else:
        st.write("No solution found")
