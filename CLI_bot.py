def input_error(func):
    
    def wrapper(*args):

        try:
            return func(*args)
        
        except KeyError:
            return "No such contact"
        
        except ValueError:
            return "Give me name and phone please"
        
        except IndexError:
            return "Enter user name"
        
    return wrapper


@input_error
def hello_handler(command, contacts):

    return "How can I help you?"


@input_error
def add_handler(command, contacts):

    name, phone = command.split()[1:]
    contacts.setdefault(name, phone)

    return f"Contact {name} with phone {phone} added"


@input_error
def change_handler(command, contacts):

    name, phone = command.split()[1:]
    contacts[name] = phone

    return f"Contact {name} changed phone to {phone}"


@input_error
def phone_handler(command, contacts):

    name = command.split()[1]
    phone = contacts.get(name)
    if phone:
        return f"Phone number of {name} is {phone}"
    
    else:
        return f"No such contact"


@input_error
def show_all_handler(command, contacts):

    result = ''
    for name, phone in contacts.items():

        result += f"{name.title()} - {phone}\n"
        
    return result.strip()


def main():
    contacts = {}
    handlers = {
                 "hello": hello_handler,
                 "add": add_handler,
                 "change": change_handler,
                 "phone": phone_handler,
                 "show": show_all_handler,
                }
    while True:

        command = input("Enter command: ").lower()

        if command in ["good bye", "close", "exit"]:

            print("Good bye!")
            break

        handler = handlers.get(command.split()[0])
        
        if handler:
            print(handler(command, contacts))
        
        else:
            print("Wrong command")

if __name__ == "__main__":
    main()
