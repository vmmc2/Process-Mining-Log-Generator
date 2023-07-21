# Imports
import csv
import random
from datetime import datetime, timedelta

# Case Count
CASE_COUNT = 10

# Start Date
START_DATE = datetime(2023, 7, 19, 9, 30, 15)

# CSV File Setup
CSV_FILEPATH = "ecommerce_log.csv"
CSV_COLUMNS = ["CaseId", "Activity", "Resource", "Start Date", "End Date"]

# Start and End Activities
START_ACTIVITY = "Sign Up"

# All Activities
ACTIVITIES = [
    "Sign In", "Sign Out", "Choose Match Mode",
    "Summoners' Rift", "Howling Abyss", "Twisted Treeline",
    "Choose Character", "Choose Runes and Spells",
    "Match Start", "Match End", "Match Statistics"
]

# Resources
RESOURCES = [
    "Odoamne", "Jankos", "Alex Ich", "Trigo", "Juliera", "Peach",
    "Patrik", "Labrov", "Mersa", "Perkz"
]

# Obligation Rules
OBLIGATION_RULES = {
    "Sign Up": ["Sign In"],
    "Sign In": ["Choose Match Mode"],
    "Choose Match Mode": ["Summoners' Rift", "Howling Abyss", "Twisted Treeline"],
    "Summoners' Rift": ["Choose Character"],
    "Howling Abyss": ["Choose Character"],
    "Twisted Treeline": ["Choose Character"],
    "Choose Character": ["Choose Runes and Spells"],
    "Choose Runes and Spells": ["Match Start"],
    "Match Start": ["Match End"],
    "Match End": ["Match Statistics"],
    "Match Statistics": ["Sign Out"]
}

# Precedence Rules
PRECEDENCE_RULES = {
    "Sign In": ["Sign Up"],
    "Choose Match Mode": ["Sign In"],
    "Summoners' Rift": ["Choose Match Mode"],
    "Howling Abyss": ["Choose Match Mode"],
    "Twisted Treeline": ["Choose Match Mode"],
    "Choose Character": ["Summoners' Rift", "Howling Abyss", "Twisted Treeline"],
    "Choose Runes and Spells": ["Choose Character"],
    "Match Start": ["Choose Runes and Spells"],
    "Match End": ["Match Start"],
    "Match Statistics": ["Match End"],
    "Sign Out": ["Match Statistics"]
}

# Prohibition Rules
PROHIBITION_RULES = {
    "Summoners' Rift": ["Summoners' Rift", "Howling Abyss", "Twisted Treeline"],
    "Howling Abyss": ["Summoners' Rift", "Howling Abyss", "Twisted Treeline"],
    "Twisted Treeline": ["Summoners' Rift", "Howling Abyss", "Twisted Treeline"],
}

def main():
    with open(CSV_FILEPATH, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(CSV_COLUMNS)

        for case_id in range(1, CASE_COUNT + 1):
            case_data = []
            precedence_activities = set()
            precedence_activities.add("Sign Up") # Parto do presuposto que minha atividade precedente inicial para cada caso eh "Sign Up"
            pending_obligations = set()

            MINIMUM_NUMBER_ACTIVITIES = 10
            current_number_activities = 1

            activity_start_date = START_DATE + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
            activity_duration_seconds = timedelta(seconds=random.randint(0, 59))
            activity_duration_minutes = timedelta(minutes=random.randint(0, 59))
            activity_duration_hours = timedelta(hours=random.randint(0, 2))
            activity_duration = activity_duration_hours + activity_duration_minutes + activity_duration_seconds
            activity_end_date = activity_start_date + activity_duration
            activity_resource = random.choice(RESOURCES)
            case_data.append([case_id, START_ACTIVITY, activity_resource, activity_start_date, activity_end_date, activity_duration])

            while len(pending_obligations) > 0 or current_number_activities < MINIMUM_NUMBER_ACTIVITIES:
                current_activity = random.choice(ACTIVITIES) # Escolho aleatoriamente uma atividade qualquer
                print("Current Activity:", current_activity)
                print("Precedence Activities:", precedence_activities) # Vejo as atividades precedentes (Ja realizadas)
                print("Pending Obligations:", pending_obligations) # Verifico minhas obrigacoes futuras (Nao realizadas)

                print("current number activities:", current_number_activities)
                if current_number_activities >= MINIMUM_NUMBER_ACTIVITIES and len(pending_obligations) == 0:
                    break

                # Nao executo atividades proibidas.
                if current_activity in PROHIBITION_RULES:
                    if any(prohibited_activity in PROHIBITION_RULES[current_activity] for prohibited_activity in precedence_activities):
                        continue
                
                # Nao executo atividades ja executadas.
                if current_activity in precedence_activities:
                    continue

                # Devo verificar se posso ou nao executar a atividade atual (inseri-la no log de eventos)
                if current_activity in PRECEDENCE_RULES:
                    if len(PRECEDENCE_RULES[current_activity]) == 1 and PRECEDENCE_RULES[current_activity][0] in precedence_activities:
                        pass
                    elif len(PRECEDENCE_RULES[current_activity]) == 3 and any(act in PRECEDENCE_RULES[current_activity] for act in precedence_activities): 
                        pass
                    print("current activity:", current_activity)
                    print(type(current_activity))
                    if (len(PRECEDENCE_RULES[current_activity]) == 1 and PRECEDENCE_RULES[current_activity][0] not in precedence_activities) or (len(PRECEDENCE_RULES[current_activity]) == 3 and PRECEDENCE_RULES[current_activity][0] not in precedence_activities and PRECEDENCE_RULES[current_activity][1] not in precedence_activities and PRECEDENCE_RULES[current_activity][2] not in precedence_activities):
                        continue

                # Adiciono as obrigacoes relacionadas a minha atividade atual.
                if current_activity in OBLIGATION_RULES:
                    if len(OBLIGATION_RULES[current_activity]) == 1:
                        pending_obligations.add(OBLIGATION_RULES[current_activity][0])
                    else:
                        pending_activity = random.choice(OBLIGATION_RULES[current_activity])
                        pending_obligations.add(pending_activity)

                # Add Activity to Log
                current_number_activities += 1
                duration_between_activities = random.randint(10, 240)
                activity_start_date = activity_end_date + timedelta(minutes=duration_between_activities)
                activity_duration_seconds = timedelta(seconds=random.randint(0, 59))
                activity_duration_minutes = timedelta(minutes=random.randint(0, 59))
                activity_duration_hours = timedelta(hours=random.randint(0, 2))
                activity_duration = activity_duration_hours + activity_duration_minutes + activity_duration_seconds
                activity_end_date = activity_start_date + activity_duration
                activity_resource = random.choice(RESOURCES)
                case_data.append([case_id, current_activity, activity_resource, activity_start_date, activity_end_date, activity_duration])
                
                # Adiciono a minha atividade atual como uma atividade precedente (ja realizada) para a proxima iteracao
                precedence_activities.add(current_activity)
                
                # Se a atividade atual era uma obrigacao pendente, removo-a.
                if current_activity in pending_obligations:
                    pending_obligations.remove(current_activity)

                # Retirando obrigacoes pendentes que ja foram cumpridas.
                for completed_activity in precedence_activities:
                    if completed_activity in pending_obligations:
                        pending_obligations.remove(completed_activity)
                if "Summoners' Rift" in precedence_activities and ("Twisted Treeline" in pending_obligations or "Howling Abyss" in pending_obligations):
                    pending_obligations.discard("Twisted Treeline")
                    pending_obligations.discard("Howling Abyss")
                if "Howling Abyss" in precedence_activities and ("Twisted Treeline" in pending_obligations or "Summoners' Rift" in pending_obligations):
                    pending_obligations.discard("Twisted Treeline")
                    pending_obligations.discard("Summoners' Rift")
                if "Twisted Treeline" in precedence_activities and ("Summoners' Rift" in pending_obligations or "Howling Abyss" in pending_obligations):
                    pending_obligations.discard("Summoners' Rift")
                    pending_obligations.discard("Howling Abyss")

                print("current number of activities:", current_number_activities)
                print("len(pending_obligations):", len(pending_obligations))

            '''
            duration_between_activities = random.randint(10, 240)
            activity_start_date = activity_end_date + timedelta(minutes=duration_between_activities)
            activity_duration_seconds = timedelta(seconds=random.randint(0, 59))
            activity_duration_minutes = timedelta(minutes=random.randint(0, 59))
            activity_duration_hours = timedelta(hours=random.randint(0, 2))
            activity_duration = activity_duration_hours + activity_duration_minutes + activity_duration_seconds
            activity_end_date = activity_start_date + activity_duration
            activity_resource = random.choice(RESOURCES)
            case_data.append([case_id, END_ACTIVITY, activity_resource, activity_start_date, activity_end_date, activity_duration])
            '''

            for csv_line in case_data:
                writer.writerow(csv_line)

        print(f"The Log Event file was successfully created in current folder: ${CSV_FILEPATH}")

    return


if __name__ == "__main__":
    main()
