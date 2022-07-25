# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

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
    If they want to see their form responses it will call check_response_data
    If not it will close the program
    """
    while True:
        print('Welcome to your Survey Response Handler. \n')
        first_response = input(
            'Would you like to see the latest form responses? y/n\n')
        if validate_str_input(first_response):
            break


def validate_str_input(user_input):
    """
    Function to validate users input of y or n.
    """
    str_options = ['y', 'n', 'Y', 'n']
    while user_input not in str_options:
        print(f'Incorrect input: [{user_input}].\n')
        print(f'Valid Input = {str_options}\n')
        return False

    return True


def check_response_data():
    """
    Access the form responses and count the number of rows
    """
    all_values = SHEET.worksheet('Form Responses').get_all_values()
    row_count = int(len(all_values)) - 1
    return row_count


def main():
    """
    This is the main function that controls the general flow of the program
    """
    begin_program()


main()
