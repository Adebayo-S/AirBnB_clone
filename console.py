#!/usr/bin/python3
"""
Entry point of the command interpreter
"""

import cmd
from models.__init__ import storage
from models.base_model import BaseModel
from models import storage  # in the init file


class HBNBCommand(cmd.Cmd):
    """
    command interpreter class
    """
    prompt = '(hbnb)'
    classes = {"BaseModel", "State", "City",
               "Amenity", "Place", "Review", "User"}

    def do_quit(self, line):
        """Exit the program"""
        return True

    def do_EOF(self, line):
        """Exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing"""
        pass

    def do_create(self, line):
        """creates a new instance of basemodel class"""
        line_list = line.split()
        if len(line_list) < 1:
            print("** class name missing **")
            return
        if line not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_inst = eval(line)()
        new_inst.save()
        print(new_inst.id)

    def do_show(self, line):
        """Print string representation: name and id"""
        line_list = line.split()
        if len(line_list) < 1:
            print("** class name missing **")
            return
        if line_list[0] != "BaseModel":  # this also has to be dynamic
            print("** class doesn't exist **")
            return
        if len(line_list) < 2:
            print("** instance id missing **")
            return
        obj_key = ".".join(line_list)
        if obj_key not in storage.all().keys():  # this too
            print("** no instance found **")
            return
        print(storage.all()[obj_key])

    def do_destroy(self, line):
        """Destroy instance specified by user; Save changes to JSON file"""
        line_list = line.split()
        if len(line_list) < 1:
            print("** class name missing **")
            return
        if line_list[0] != "BaseModel":  # this
            print("** class doesn't exist **")
            return
        if len(line_list) < 2:
            print("** instance id missing **")
            return
        obj_key = ".".join(line_list)
        if obj_key not in storage.all().keys():  # this too
            print("** no instance found **")
            return
        del storage.all()[obj_key]
        storage.save()

    def do_all(self, line):
        """Print all objects or all objects of specified class"""
        line_list = line.split()
        if len(line_list) == 0:  # if no arg is passed to all command
            print([str(v) for v in storage.all().values()])
        elif line_list[0] != "BaseModel":  # has to be dynamic
            print("** class doesn't exist **")
            return
        elif len(line_list) > 0:
            print([str(v) for v in storage.all().values()
                  if type(v).__name__ == line_list[0]])

    def do_update(self, line):
        """Update if given exact object, exact attribute"""
        line_list = line.split()
        if len(line_list) < 1:
            print("** class name missing **")
            return
        if line_list[0] != "BaseModel":
            print("** class doesn't exist **")
            return
        if len(line_list) < 2:
            print("** instance id missing **")
            return
        key = f"{line_list[0]}.{line_list[1]}"
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        if len(line_list) < 3:
            print("** attribute name missing **")
            return
        if len(line_list) < 4:
            print("** value missing **")
            return
        if isinstance(eval(line_list[3]), int):  # strip off str ndcheck if int
            line_list[3] = int(line_list[3])
        elif isinstance(eval(line_list[3]), float):  # or if float
            line_list[3] = float(line_list[3])
        else:
            line_list[3] = line_list[3]

        obj = storage.all()[key]  # check for d particular inst
        setattr(obj, line_list[2], line_list[3])
        storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
