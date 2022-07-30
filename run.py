# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
import numpy as np

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('SurveyResponseForm')


def begin_program():
    """
    This function will run, welcome the user and take a response from them
    If they want to see their form responses it will call get_row_count
    If not it will close the program
    """
    while True:
        print('Welcome to your Survey Response Handler. \n')
        first_response = input(
            'Would you like to check for new responses? y/n\n')
        if validate_str_input(first_response):
            if first_response in ['y', 'Y']:
                print('Checking worksheet for added responses...')
                previous_responses = int(response_counter())
                print(previous_responses)
                new_responses = get_row_count('Form responses 4')
                print(new_responses)
                if new_responses > previous_responses:
                    print('There are new responses to your survey.\n')
                    print('Would you like to see them in a table?\n\n')
                    second_response = input('y/n\n')
                    print('\n')
                    if validate_str_input(second_response):
                        if second_response in ['y', 'Y']:
                            full_form = show_full_responses()
                            print(full_form)
                            SHEET.worksheet('Form responses 4').update(
                                'W2', new_responses)
                            break
                        elif second_response in ['n', 'N']:
                            close_program()

            elif first_response in ['n', 'N']:
                close_program()


def validate_str_input(user_input):
    """
    Function to validate users input of y or n.
    """
    str_options = ['y', 'n', 'Y', 'N']
    while user_input not in str_options:
        print(f'Incorrect input: [{user_input}].\n')
        print(f'Valid Input = {str_options}\n')
        return False

    return True


def validate_int_input(user_input):
    """
    A function to validate integer inputs
    """
    int_options = [1, 2, 3, 4, 4, 6]
    while user_input not in int_options:
        print(f'Incorrect input: [{user_input}].\n')
        print(f'Valid Input = {int_options}\n')
        return False

    return True


def response_counter():
    """
    Keeps a running total of how many responses there
    have been and returns this value.
    """
    # all_values = SHEET.worksheet('Form Responses').get_all_values()
    # row_total = int(len(all_values)) - 1
    # row_total = get_row_count()
    # SHEET.worksheet('Form Responses').update_acell('AB2', row_total)
    val = SHEET.worksheet('Form responses 4').acell('W2').value
    return val


def get_row_count(sheet):
    """
    Access the form responses and count the number of rows
    """
    # existing_responses = int(response_counter())
    all_values = SHEET.worksheet(sheet).get_all_values()
    row_count = int(len(all_values)) - 1
    return row_count


def show_full_responses():
    """
    Get all the table responses
    """
    print('Getting response data now...\n')
    print('Table of most recent responses:\n')
    batch_1 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_1')
    batch_2 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_2')
    batch_3 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_3')
    batch_4 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_4')
    batch_5 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_5')
    batch_6 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_6')
    batch_7 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_7')
    batch_8 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_8')
    batch_9 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_9')
    batch_10 = SHEET.worksheet('Form responses 4').get_values(
        'Form_Responses_part_10')
    batched_data = batch_1 + batch_2 + batch_3 + batch_4 + \
        batch_5 + batch_6 + batch_7 + batch_8 + batch_9 + batch_10

    return tabulate(batched_data, tablefmt="grid")


def present_options():
    """
    A function to display choices of sorted data tables.
    """
    print('\nChoose an option below to see organised data.\n\n')

    print('Option 1: Time spent on Social Media per age group')

    user_choice = input('Which table would you like to see?\n')

    if validate_int_input(user_choice):
        if user_choice == 1:
            display_table(user_choice)
        elif user_choice == 2:
            display_table(user_choice)
        elif user_choice == 3:
            display_table(user_choice)
        elif user_choice == 4:
            display_table(user_choice)
        elif user_choice == 5:
            display_table(user_choice)
        elif user_choice == 6:
            display_table(user_choice)


def display_table(user_choice):
    """
    A function that will pull the correct table of data
    based on the choice entered by the user.
    """


def populate_tables():
    """
    A function to split the main form responses
    into smaller tables so they can be analysed
    seperately.
    """
    hours_spent_values = SHEET.worksheet('Form responses 4').get('B1:F50')
    SHEET.worksheet('Hours Spent').update('A1:E50', hours_spent_values)
    number_of_rows = get_row_count('Hours Spent')
    cell_range = SHEET.worksheet('Hours Spent').batch_get(['B2:E50'])
    totals = []
    # cell_list = SHEET.worksheet('Hours Spent').range('F2:F50')
    for row in cell_range:
        for list_of_values in row:
            total = [(sum(map(int, list_of_values)))]
            SHEET.worksheet('Hours Spent').update('Total Hours', total)
            totals.append(total)
                
    print(totals)
    # SHEET.worksheet('Hours Spent').update('Total Hours', [totals])


def close_program():
    """
    Function to close the program.
    """
    print('Closing the program now...')
    quit()


def main():
    """
    This is the main function that controls the general flow of the program
    """
    # begin_program()
    populate_tables()
    # present_options()


main()
