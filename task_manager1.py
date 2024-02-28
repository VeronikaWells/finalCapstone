"""
Task manager.
This is a program designed for a small business 
to help it manage tasks assigned to each member of a team.
The program allows a user to add new users, generate reports and statistics, 
add new tasks, view all the tasks available, edit them and mark as completed or not.
"""

# Notes: 
#1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.
# 

import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# This function is called when the user inputs 'r' to register a user.
def reg_user(username_password):
    new_username = input("\nNew Username: ").lower()
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check  the availability of the user name and if the new password and confirmed password are the same.
    if new_username in username_password or new_password != confirm_password:
        print("Invalid username or passwords do not match. Please try again.")
    else:
        print("New user added.")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            out_file.write("\n".join([f"{k};{username_password[k]}" for k in username_password]))


# This function is called when the user inputs 'a' to add a task.
def add_task():
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        open("tasks.txt", "w").close()

    task_list = []
    with open("tasks.txt", 'r') as task_file:
        task_data = [t.split(";") for t in task_file.read().split("\n") if t]

    task_username = input("\nName of person assigned to task: ").lower()
    while task_username not in username_password:
        print("User does not exist. Please enter a valid username.")
        task_username = input("\nName of person assigned to task: ").lower()

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified.")

    curr_date = date.today()
    # Add the data to the file task.txt and include 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_data.append([task_username, task_title, task_description, due_date_time.strftime(DATETIME_STRING_FORMAT),
                      curr_date.strftime(DATETIME_STRING_FORMAT), "No"])

    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([";".join(map(str, t)) for t in task_data]))

    print("Task successfully added.")


# This function is called when the user inputs 'va' to view all the tasks.
def view_all():
    with open("tasks.txt", "r") as task_file:
        task_lines = task_file.readlines()

    for index, line in enumerate(task_lines, 1):
        task_components = line.strip().split(";")

        if len(task_components) == 6:
            t = dict(zip(['username', 'title', 'description', 'due_date', 'assigned_date', 'completed'],
                         task_components))
            disp_str = f"\nTask: \t\t {t['title']}\nAssigned to: \t {t['username']}\nDate Assigned: \t {t['assigned_date']}\nDue Date: \t {t['due_date']}\nTask Description: {t['description']}\n"
            print(f"\n ({index}) {disp_str}")


# This function is called when the user inputs 'vm' to view the current user`s tasks.
def view_mine(curr_user):
    try:
        with open("tasks.txt", "r+") as task_file:
            tasks = [line.strip().split(";") for line in task_file.readlines()]

        # Check if the current user matches the current task available.
        user_tasks = [task for task in tasks if task[0].lower() == curr_user]

        if not user_tasks:
            print("\nThere are no tasks for this user.")
        else:
            print("\n~~~~~~~~~~\nYour tasks: ")
            for index, task_info in enumerate(user_tasks, 1):
                t = dict(zip(['username', 'title', 'description', 'due_date', 'assigned_date', 'completed'], task_info))
                disp_str = f"\nTask: \t\t {t['title']}\nAssigned to: \t{t['username']}\nDate Assigned: \t{t['assigned_date']}\nDue Date: \t{t['due_date']}\nTask Description: \t{t['description']}\n"

                if task_info[0].lower() == curr_user:
                    print(f"\n({index}){disp_str}")

    except FileNotFoundError:
        print("\nError: 'tasks.txt' not found")


# This try-except block catches errors from the user when the function is executed.
    try:
        choice = int(input("\nPlease enter the task number to select, or enter '-1' to return to the Main Menu: "))

        if choice == -1:
            return
        elif 1 <= choice <= len(tasks):
            selected_task = tasks[choice - 1]
            task_status = selected_task[5].lower()

            if task_status == 'no':
                action = input("\nPlease enter 'Yes' to mark the task as complete, enter 'Edit' to edit the task or enter 'Back' to return to the Main Menu: ").lower()

                if action == "back":
                    return
                elif action == "yes":
                    selected_task[5] = "Yes"
                    tasks[choice - 1] = selected_task
                    with open("tasks.txt", "w") as task_file:
                        task_file.write("\n".join([";".join(map(str, t)) for t in tasks]))
                    print("\nTask marked as completed.")
                elif action == "edit":
                    new_username = input("Enter the new username: ")
                    new_due_date = input("Enter the new due date: ")
                    selected_task[0] = new_username
                    selected_task[3] = new_due_date
                    tasks[choice - 1] = selected_task
                    with open("tasks.txt", "w") as task_file:
                        task_file.write("\n".join([";".join(map(str, t)) for t in tasks]))
                    print("\nTask is edited.")
                else:
                    print("\nInvalid action. The task has not been modified.")
            else:
                print("\nTask is marked as completed and cannot be modified.")
        else:
            print("\nInvalid task number.")
    except ValueError:
        print("\nInvalid input. Please enter a valid task number.")
    except FileNotFoundError:
        print("Error: 'tasks.txt' not found.")


# This function is called when the user inputs 'gr' to generate reports.
def gen_reports():
    try:
        with open("tasks.txt", "r+") as task_file:
            tasks = [line.strip().split(";") for line in task_file.readlines()]

        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task[5].lower() == "yes")
        uncompleted_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(1 for task in tasks if task[5].lower() == "no" and datetime.strptime(task[3], DATETIME_STRING_FORMAT).date() < date.today())

        percentage_incomplete = (uncompleted_tasks / total_tasks) * 100
        percentage_overdue = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"Total Tasks:{total_tasks}\n")
            task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
            task_overview_file.write(f"Uncompleted Tasks: {uncompleted_tasks}\n")
            task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
            task_overview_file.write(f"Percentage of Incomplete Tasks: {percentage_incomplete:.2f}%\n")
            task_overview_file.write(f"Percentage of Overdue Tasks: {percentage_overdue:.2f}%\n")

        with open("user.txt", "r") as user_file:
            users = [line.strip().split(";")[0] for line in user_file.readlines()]

        total_users = len(users)
        # Calculate user-specific statistics.
        user_statistics = []
        for user in users:
            user_tasks = [task for task in tasks if task[0].lower() == user.lower()]
            total_user_tasks = len(user_tasks)
            percentage_total_tasks = (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            completed_user_tasks = sum(1 for task in user_tasks if task[5].lower() == "yes")
            percentage_completed_user_tasks = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            uncompleted_user_tasks = total_user_tasks - completed_user_tasks
            percentage_uncompleted_user_tasks = (uncompleted_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            overdue_user_tasks = sum(1 for task in user_tasks if task[5].lower() == "no" and datetime.strptime(task[3], DATETIME_STRING_FORMAT).date() < date.today())
            percentage_overdue_user_tasks = (overdue_user_tasks / uncompleted_user_tasks) * 100 if uncompleted_user_tasks > 0 else 0

            user_statistics.append({
                "username": user,
                "total_user_tasks": total_user_tasks,
                "percentage_total_tasks": percentage_total_tasks,
                "percentage_completed_user_tasks": percentage_completed_user_tasks,
                "percentage_uncompleted_user_tasks": percentage_uncompleted_user_tasks,
                "percentage_overdue_user_tasks": percentage_overdue_user_tasks
            })

        with open("user_overview.txt", "w") as user_overview_file:
            user_overview_file.write(f"Total Users:{total_users}\n")
            user_overview_file.write(f"Total Tasks:{total_tasks}\n")

            for user_stat in user_statistics:
                user_overview_file.write(f"\nUser: {user_stat['username']}\n")
                user_overview_file.write(f"Total Tasks Assigned to User: {user_stat['total_user_tasks']}\n")
                user_overview_file.write(f"Percentage of Total Tasks: {user_stat['percentage_total_tasks']:.2f}%\n")
                user_overview_file.write(
                    f"Percentage of Completed Tasks: {user_stat['percentage_completed_user_tasks']:.2f}%\n")
                user_overview_file.write(
                    f"Percentage of Uncompleted Tasks: {user_stat['percentage_uncompleted_user_tasks']:.2f}%\n")
                user_overview_file.write(
                    f"Percentage of Overdue Tasks: {user_stat['percentage_overdue_user_tasks']:.2f}%\n")

        print("\nReports generated successfully. Please see file 'user_overview.txt' and 'task_overview.txt'.")
    except FileNotFoundError:
        print("\nError: 'tasks.txt' or 'user_overview.txt' are not found.")


# This function is called when the user inputs 'ds' to display statistics.
def display_stat():
    try:
        #Check it the logged-in user is the admin, if not displays an error message and return to the main menu.
        if curr_user != "admin":
            print("\nError: Only the admin user can display statistics.")
            return

        # Check it the text files exist, and generate them if needed
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            print("\nGenerating reports...")
            gen_reports()

        with open("task_overview.txt", "r") as task_overview_file:
            task_overview = task_overview_file.read()
            print("\nTask Overview: \n" + task_overview)

        with open("user_overview.txt", "r") as user_overview_file:
            user_overview = user_overview_file.read()
            print("\nUser Overview: \n" + user_overview)

    except FileNotFoundError:
        print("\nError: 'task_overview.txt' or 'user_overview.txt' are not found.")

#Login Section
#This code reads usernames and password from the user.txt file to  allow a user to login.

if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

if not os.path.exists("tasks.txt"):
    open("tasks.txt", "w").close()

with open("user.txt", 'r') as user_file:
    username_password = dict(line.strip().split(";") for line in user_file.readlines())

logged_in = False
while not logged_in:
    print("""\n~~~~~~ WELCOME TO TASK MANAGER ~~~~~~ 
          \n~~~~~ PLEASE LOGIN ~~~~~""")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password or username_password[curr_user] != curr_pass:
        print("Invalid username or password. Please try again.")
    else:
        print("Login Successful!")
        logged_in = True

while True:
    main_menu = input('''\n ~~~~~ MAIN MENU ~~~~~
Please select one of the following options below:
r \t- \tRegister user
a \t- \tAdd task
va \t- \tView all tasks
vm \t- \tView my tasks
gr \t- \tGenerate reports
ds \t- \tDisplay statistics
e \t- \tExit
: ''').lower()

    # Conditional statements to control the functions based on the user input.
    if main_menu == 'r':
        reg_user(username_password)

    elif main_menu == 'a':
        add_task()

    elif main_menu == 'va':
        view_all()

    elif main_menu == 'vm':
        view_mine(curr_user)

    elif main_menu == 'gr':
        gen_reports()

    elif main_menu == 'ds':
        display_stat()

    elif main_menu == 'e':
        exit("\nThank you for using the task manager! Have a nice day! Goodbye!")

    else:
        print("You have put an invalid choice, please, try again.")