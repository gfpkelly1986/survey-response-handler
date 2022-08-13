"""
A form response handler program
"""
from operator import itemgetter
import sys
import pyfiglet
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

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
    This function will run, welcome the user and take an initial
    response from them.
    If they want to check for form responses it will call get_row_count
    and check for new responses against a responsecounter variable which
    is stored in 'Cell W2' in Form Responses 4 worksheet.
    If not it will close the program.
    """
    title = pyfiglet.figlet_format('Survey Response Handler', font='slant')
    print(title)
    while True:
        print('Welcome to your Survey Response Handler. \n')
        first_response = input(
            'Would you like to check for new responses? y/n\n')
        if validate_str_input(first_response):
            if first_response in ['y', 'Y']:
                print('Checking worksheet for added responses...')
                previous_responses = int(response_counter())
                print(f'There was {previous_responses} responses')
                new_responses = get_row_count('Form responses 4')
                print(f'There are now {new_responses} responses')
                if new_responses > previous_responses:
                    print('Would you like a table of the responses?\n\n')
                    second_response = input('y/n\n')
                    print('\n')
                    if validate_str_input(second_response):
                        if second_response in ['y', 'Y']:
                            full_form = show_full_responses()
                            print(full_form)
                            print('Gathering data to present options...')
                            # The response counter is blocked so the form can
                            # be tested repeatedly
                            # SHEET.worksheet('Form responses 4').update_acell
                            # ('W2', new_responses)
                            break
                        elif second_response in ['n', 'N']:
                            close_program()

            elif first_response in ['n', 'N']:
                close_program()


def validate_str_input(user_input):
    """
    A function to validate users string inputs of y or n.
    """
    str_options = ['y', 'n', 'Y', 'N']
    while user_input not in str_options:
        print(f'Incorrect input: [{user_input}].\n')
        print(f'Valid Input = {str_options}\n')
        return False

    return True


def validate_int_input(user_input):
    """
    A function to validate numbers entered on the keyboard.
    This is used to validate the 5 options of organised
    data presented to the user.
    """
    int_options = ['1', '2', '3', '4', '5']
    while user_input not in int_options:
        print(f'Incorrect input: [{user_input}].\n')
        print(f'Valid Input = {int_options}\n')
        return False

    return True


def response_counter():
    """
    Keeps a running total of how many responses there
    have been and returns this value. This value is
    stored in the worksheet 'Form responses 4' in cell 'W2'
    """
    val = SHEET.worksheet('Form responses 4').acell('W2').value
    return val


def get_row_count(sheet):
    """
    Access the form responses and count the number of rows to
    help assess if new rows have been added.
    If there are new rows the row count will be greater than
    the value returned from response_counter().
    """
    all_values = SHEET.worksheet(sheet).get_all_values()
    row_count = int(len(all_values)) - 1
    return row_count


def show_full_responses():
    """
    Get all the form responses and return a table
    of the responses. No data grouped or sorted yet
    outside of how the form was designed to gather
    the data.
    """
    print('Getting response data now\n')
    print('This may take a moment...\n')
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
    A function to display choices to the user to select
    one of 5 sorted data options based on their input choice
    of '1' '2' '3' '4' '5'. One displays a age related table
    of data, the others are top performers in each category
    of question type related to feelings.
    """
    print('\nChoose an option below to see organised data.\n\n')

    print('Option 1: Time spent on Social Media per age group\n'
          'Option 2: Leading Platform for Happiness\n'
          'Option 3: Leading platform for Informedness\n'
          'Option 4: Leading Platform for Connectedness\n'
          'Option 5: Leading Platform for Anxiousness\n\n')

    user_choice = input('Which option would you like to see? (1 - 5)\n')

    if validate_int_input(user_choice):
        if user_choice == '1':
            list_of_totals = set_total_hours()
            get_age_related_hours(list_of_totals)

            while True:
                continue_with_options = input(
                    'Do you want to see more options?\n')
                if validate_str_input(continue_with_options):
                    if continue_with_options in ['y', 'Y']:
                        present_options()
                    elif continue_with_options in ['n', 'N']:
                        close_program()

        elif user_choice == '2':
            column_values_list = get_column_values()
            leading_platforms = set_totals_for_feelings(column_values_list)

            platform_dict = {
                'Facebook': (leading_platforms[0][0][0]),
                'Instagram': (leading_platforms[0][0][1]),
                'Twitter': (leading_platforms[0][0][2]),
                'Linked-In': (leading_platforms[0][0][3])
            }

            top_platform = max(platform_dict, key=platform_dict.get)
            print(f'{top_platform} is the top Social Media platform\n'
                  f'for feelings of happiness when used.\n')
            while True:
                continue_with_options = input(
                    'Do you want to see more options?\n')
                if validate_str_input(continue_with_options):
                    if continue_with_options in ['y', 'Y']:
                        present_options()
                    elif continue_with_options in ['n', 'N']:
                        close_program()
        elif user_choice == '3':
            column_values_list = get_column_values()
            leading_platforms = set_totals_for_feelings(column_values_list)
            platform_dict = {
                'Facebook': (leading_platforms[1][0][0]),
                'Instagram': (leading_platforms[1][0][1]),
                'Twitter': (leading_platforms[1][0][2]),
                'Linked-In': (leading_platforms[1][0][3])
            }

            top_platform = max(platform_dict, key=platform_dict.get)
            print(f'{top_platform} is the top Social Media platform\n'
                  f'for feelings of Informedness when used.')

            while True:
                continue_with_options = input(
                    'Do you want to see more options?\n')
                if validate_str_input(continue_with_options):
                    if continue_with_options in ['y', 'Y']:
                        present_options()
                    elif continue_with_options in ['n', 'N']:
                        close_program()

        elif user_choice == '4':
            column_values_list = get_column_values()
            leading_platforms = set_totals_for_feelings(column_values_list)
            platform_dict = {
                'Facebook': (leading_platforms[2][0][0]),
                'Instagram': (leading_platforms[2][0][1]),
                'Twitter': (leading_platforms[2][0][2]),
                'Linked-In': (leading_platforms[2][0][3])
            }

            top_platform = max(platform_dict, key=platform_dict.get)
            print(f'{top_platform} is the top Social Media platform\n'
                  f'for feelings of Connectedness when used.')

            while True:
                continue_with_options = input(
                    'Do you want to see more options?\n')
                if validate_str_input(continue_with_options):
                    if continue_with_options in ['y', 'Y']:
                        present_options()
                    elif continue_with_options in ['n', 'N']:
                        close_program()
        elif user_choice == '5':
            column_values_list = get_column_values()
            leading_platforms = set_totals_for_feelings(column_values_list)
            platform_dict = {
                'Facebook': (leading_platforms[3][0][0]),
                'Instagram': (leading_platforms[3][0][1]),
                'Twitter': (leading_platforms[3][0][2]),
                'Linked-In': (leading_platforms[3][0][3])
            }

            top_platform = max(platform_dict, key=platform_dict.get)
            print(f'{top_platform} is the top Social Media platform\n'
                  f'for feelings of Anxiousness when used.')
            while True:
                continue_with_options = input(
                    'Do you want to see more options?\n')
                if validate_str_input(continue_with_options):
                    if continue_with_options in ['y', 'Y']:
                        present_options()
                    elif continue_with_options in ['n', 'N']:
                        close_program()
    else:
        present_options()


def populate_tables(age_list):
    """
    A function to split the main form responses
    into smaller tables\\worksheets so they can be analysed
    seperately.
    """
    age_list = get_responder_ages()
    hours_spent_values = SHEET.worksheet('Form responses 4').get('B1:F50')
    SHEET.worksheet('Hours Spent').update('A1:E50', hours_spent_values)
    SHEET.worksheet('Happy').update('A1:A50', age_list)
    SHEET.worksheet('Anxious').update('A1:A50', age_list)
    SHEET.worksheet('Connected').update('A1:A50', age_list)
    SHEET.worksheet('Informed').update('A1:A50', age_list)
    hrs_happy = SHEET.worksheet('Form responses 4').get('Hrs_Happy')
    SHEET.worksheet('Happy').update('B1:E50', hrs_happy)
    hrs_informed = SHEET.worksheet('Form responses 4').get('Hrs_Informed')
    SHEET.worksheet('Informed').update('B1:E50', hrs_informed)
    hrs_connected = SHEET.worksheet('Form responses 4').get('Hrs_Connected')
    SHEET.worksheet('Connected').update('B1:E50', hrs_connected)
    hrs_anxious = SHEET.worksheet('Form responses 4').get('Hrs_Anxious')
    SHEET.worksheet('Anxious').update('B1:E50', hrs_anxious)


def get_responder_ages():
    """
    A function to get age data from the 'what is your age'
    in the form responses worksheet column and return this
    data. This is used to group age related data together.
    """
    age_list = SHEET.worksheet('Form responses 4').get('Age_List')
    return age_list


def set_total_hours():
    """
    A function to get the total hrs spent on Social
    Media from the Hours Spent worksheet and updates
    the totals coulmn, returns a list of lists
    containing the new totals.
    """
    cell_range = SHEET.worksheet('Hours Spent').batch_get(['B2:E50'])
    list_of_totals = []
    for row in cell_range:
        for list_of_values in row:
            total = [(sum(map(int, list_of_values)))]
            list_of_totals.append(total)

    SHEET.worksheet('Hours Spent').update('Total_Hours', list_of_totals)
    return list_of_totals


def get_age_related_hours(list_of_totals):
    """
    A function to combine age related data in relation
    to hours spent on social media into seperate tables
    and print a filtered table to the terminal.
    """
    int_totals = []

    for num in list_of_totals:
        for val in num:
            int_totals.append(val)

    age_list = get_responder_ages()
    age_list = age_list[1:]
    age_ints = []
    for val in age_list:
        for age in val:
            age = int(age)
            age_ints.append(age)

    totals1 = []
    totals2 = []
    totals3 = []
    for age, total in zip(age_ints, int_totals):
        if age <= 25 and total > 0:
            totals1.append(int(total))
        elif age <= 45 and total > 0:
            totals2.append(int(total))
        elif age <= 65 and total > 0:
            totals3.append(total)

    total_smedia_under25 = str((sum(totals1)))
    total_smedia_under45 = str((sum(totals2)))
    total_smedia_under65 = str((sum(totals3)))
    totals = [
        [total_smedia_under25],
        [total_smedia_under45],
        [total_smedia_under65]]

    SHEET.worksheet('Useful Data').update('Total_Smedia_Hours', totals)
    hours_per_age_group = SHEET.worksheet('Useful Data').get('A31:B35')
    print(tabulate(hours_per_age_group, tablefmt="grid"))


def set_totals_for_feelings(column_values_list):
    """
    A function that will total and update all the responses
    relating to happiness, connectedness, anxiousness
    and Informedness so the program can later choose
    a top performer in each category.
    """
    sheet1 = column_values_list[0]
    sheet2 = column_values_list[1]
    sheet3 = column_values_list[2]
    sheet4 = column_values_list[3]
    list1 = []
    list2 = []
    list3 = []
    list4 = []

    # This loop is unpacking 4 rows and 4 columns from 4 sheets.
    # Short variable names are used to stay within 80 characters.
    # These variables have no other use.
    for a_1, b_2, c_3, d_4 in zip(sheet1, sheet2, sheet3, sheet4):
        for e_5, f_6, g_7, h_8 in zip(a_1, b_2, c_3, d_4):
            for i_9, j_10, k_11, l_12 in zip(e_5, f_6, g_7, h_8):
                list1.append(int(i_9))
                list2.append(int(j_10))
                list3.append(int(k_11))
                list4.append(int(l_12))
    sheet1 = list1
    sheet2 = list2
    sheet3 = list3
    sheet4 = list4

    get = itemgetter(slice(0, 4), slice(4, 8), slice(8, 12), slice(12, 16))
    sheet1_col_totals = get(sheet1)
    sheet2_col_totals = get(sheet2)
    sheet3_col_totals = get(sheet3)
    sheet4_col_totals = get(sheet4)

    sheet1_col_totals = [str(sum(x)) for x in sheet1_col_totals]
    sheet2_col_totals = [str(sum(x)) for x in sheet2_col_totals]
    sheet3_col_totals = [str(sum(x)) for x in sheet3_col_totals]
    sheet4_col_totals = [str(sum(x)) for x in sheet4_col_totals]

    SHEET.worksheet('Happy').update('Happy_Totals', [sheet1_col_totals])
    SHEET.worksheet('Informed').update('Informed_Totals', [sheet2_col_totals])
    SHEET.worksheet('Connected').update(
        'Connected_Totals', [sheet3_col_totals])
    SHEET.worksheet('Anxious').update('Anxious_Totals', [sheet4_col_totals])

    return [
        [sheet1_col_totals],
        [sheet2_col_totals],
        [sheet3_col_totals],
        [sheet4_col_totals]]


def get_column_values():
    """
    A function to return a list of lists
    containing column values for all 'feelings'
    responses in the Form responses 4 worksheet.
    These questions relate to feelings when using
    certain social media platforms.
    This is data from 4 columns in each category of
    question in the main responses form. It built
    to handle 50 responses.

    """
    column_values_list = []
    col_values_happy = SHEET.worksheet('Happy').batch_get(
        ['B2:B50', 'C2:C50', 'D2:D50', 'E2:E50'])
    col_values_connected = SHEET.worksheet('Informed').batch_get(
        ['B2:B50', 'C2:C50', 'D2:D50', 'E2:E50'])
    col_values_informed = SHEET.worksheet('Connected').batch_get(
        ['B2:B50', 'C2:C50', 'D2:D50', 'E2:E50'])
    col_values_anxious = SHEET.worksheet('Anxious').batch_get(
        ['B2:B50', 'C2:C50', 'D2:D50', 'E2:E50'])

    column_values_list.append(col_values_happy)
    column_values_list.append(col_values_connected)
    column_values_list.append(col_values_informed)
    column_values_list.append(col_values_anxious)

    return column_values_list


def close_program():
    """
    Function to close the program.
    """
    print('Thank you for using Survey Response Handler!\n')
    print('Closing the program now...')
    sys.exit()


def main():
    """
    This is the main function that controls the general flow of the program
    """
    begin_program()
    age_list = get_responder_ages()
    populate_tables(age_list)
    present_options()


main()
