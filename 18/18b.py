def generate_new_equation(equation):
    new_equ = ""
    new_idx = 0
    previous_value = ""
    addition = False
    after_group = False

    for idx, element in enumerate(equation):
        if new_idx > idx:
            continue
        if element == "+":
            new_equ += element
            addition = True
        elif element == "*":
            new_equ += element
            addition = False
        elif element == " ":
            new_equ += element
        elif element.isnumeric():
            if addition and not after_group:
                previous_group = f"({previous_value} + {element})"
                new_equ = f"{new_equ[:-4]}{previous_group}"
                after_group = True
            elif addition and after_group:
                previous_group_after = f"({previous_group} + {element})"
                new_equ = new_equ[:-(len(previous_group)+3)] + previous_group_after
                previous_group = previous_group_after
                after_group = True
            else:
                new_equ = new_equ + element
                previous_value = element
                after_group = False
        elif element == "(":
            return_value = generate_new_equation(equation[idx+1:])
            new_idx = idx + return_value[1] + 2
            if addition and not after_group:
                previous_group = f"({previous_value} + ({return_value[0]}))"
                new_equ = f"{new_equ[:-4]}{previous_group}"
                after_group = True
            elif addition and after_group:
                previous_group_after = f"({previous_group} + ({return_value[0]}))"
                new_equ = new_equ[:-(len(previous_group)+3)] + previous_group_after
                previous_group = previous_group_after
                after_group = True
            else:
                new_equ = new_equ + "(" + return_value[0] + ")"
                previous_group = f"({return_value[0]})"
                after_group = True
        elif element == ")":
            return [new_equ, idx]
    return new_equ

def sum_all_equations():
    result = 0

    with open("input.txt") as f:
        for line in f:
            line = line.rstrip('\n')
            new_val = eval(generate_new_equation(line))
            result += new_val

    return result

print(sum_all_equations())