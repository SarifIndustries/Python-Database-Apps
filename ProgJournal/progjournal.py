#!/usr/bin/env python3

#======================================#
#=  PROGRAMMING JOURNAL DATABASE APP  =#
#======================================#

from database import storage_add, storage_get, create_table_if_not_exists

greetings_text = "=" * 10 + "  Welcome to programming journal app  " + "=" * 10

menu_text = """
[ Please select option ]
1. Add new entry for today.
2. View entries.
3. Exit.

Your selection: """


def prompt_new_entry():
	date = input("Date: ")
	content = input("Content: ")
	storage_add(date=date, content=content)


def show_all_entries():
	print()
	cursor = storage_get()
	for entry in cursor:
		print(f"[{entry['date_stamp']}]\n{entry['content']}\n\n\t")


#===================== MAIN =====================

def main():
	create_table_if_not_exists()
	print(greetings_text)
	while (user_input := input(menu_text)) != "3":
		if user_input == "1":
			prompt_new_entry()
		elif user_input == "2":
			show_all_entries()
		else:
			print("Wrong option, please try again.")

#================================================

if __name__ == "__main__":
	main()
