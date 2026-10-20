from organizer import Organizer

def main():
    organizer = Organizer("downloads")
    operations = organizer.build_plan()
    organizer.preview_plan(operations)
    if not operations:
        return
    choice = input("Do you want to execute the plan? (y/n): ")
    if choice.lower() == "y":
        organizer.execute_plan(operations)

    else:
        print("Plan execution canceled.")

if __name__ == "__main__":
    main()