## constraint satisfaction problem

# Timetable Scheduler for 1CS Semester 2

## Overview

This project aims to generate a feasible timetable for the 1st-year Computer Science (1CS) students for Semester 2 using Constraint Satisfaction Problem (CSP) techniques. The timetable must satisfy a set of hard constraints and aim to satisfy as many soft constraints as possible.

## Problem Description

The task is to schedule the timetable for the 1CS students considering the following constraints

## Constraints

### Hard Constraints

1. The week consists of five days: Sunday, Monday, Tuesday, Wednesday, and Thursday.
2. Each day has five work slots, except Tuesday which has only three in the morning.
3. A maximum of three successive slots of work are allowed.
4. Lectures of the same course should not be scheduled in the same slot.
5. Lectures of different courses should not be scheduled in the same slot.
6. Different courses for the same group must have different slot allocations.

### Soft Constraints

1. Each teacher should have a maximum of two days of work.

## Installation

Ensure you have Python installed. Then, install the required packages:

```bash
pip install python-constraint pandas
```
```bash
python script.py
```

## Example Output
![](/Screenshot.png)







