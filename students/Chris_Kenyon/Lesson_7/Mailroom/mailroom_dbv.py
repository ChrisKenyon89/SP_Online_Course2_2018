#!/usr/bin/env python3

# Lesson_10 Activity 1 Functional Mailroom

import os
from init_mailroom_db import *

#class Donor:

    #def __init__(self, first_name, surname, donations=None):
        #self.first = first_name
        #self.last = surname
        #if isinstance(donations, int):
            #donations = [donations]
        #self.donations = list(donations)

    #@property
    #def full_name(self):
        #return f"{self.first} {self.last}"

    #@property
    #def total_donation(self):
        #return sum(self.donations)

    #def add_donation(self, new_donation):
        #self.donations.append(new_donation)


#class DonorChart:

    #def __init__(self, donors=None):
        #self.donors = []
        #if donors:
            #self.donors = donors

    #def add_donor(self, donor):
        #self.donors.append(donor)

    #@property
    #def donor_list(self):
        #return[donor.full_name for donor in self.donors]

    #@property
    #def total_raised(self):
        #return(sum([sum(donor.donations) for donor in self.donors]))

    #@property
    #def total_donations(self):
        #return(sum([len(donor.donations) for donor in self.donors]))

    #def sort_by_first(self):
        #return(sorted(self.donors, key=first_key, reverse=False))

    #def sort_by_last(self):
        #return(sorted(self.donors, key=last_key, reverse=False))

    #def sort_by_total(self):
        #return(sorted(self.donors, key=total_key, reverse=True))

    #def mult_donations(self, factor):
        #"""multiply donations for each donor and return new class"""
        #dc_dub = DonorChart()
        #for donor in self.donors:
            #person = Donor(donor.first, donor.last,
                           #list(map(lambda x: x * factor, donor.donations)))
            #dc_dub.add_donor(person)
        #return dc_dub

    #def min_filter(self, min_donation=10):
        #"""filter by min donation for each donor and return new class"""
        #dc_min_filt = DonorChart()
        #for donor in self.donors:
            #person = Donor(donor.first, donor.last,
                           #list(filter(lambda x: x >= min_donation,
                                       #donor.donations)))
            #dc_min_filt.add_donor(person)
        #return dc_min_filt

    #def max_filter(self, max_donation=1000):
        #"""filter by max donation for each donor and return new class"""
        #dc_max_filt = DonorChart()
        #for donor in self.donors:
            #person = Donor(donor.first, donor.last,
                           #list(filter(lambda x: x <= max_donation,
                                       #donor.donations)))
            #dc_max_filt.add_donor(person)
        #return dc_max_filt

def get_donor_list():
    
    database = SqliteDatabase('mailroom.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        return [donor.donor_name for donor in Donor.select()]

    except Exception as e:
        logger.info(e)
    finally:
        database.close()


def page_break():
    """ Print a separator to distinguish new 'pages'"""
    print("_"*75+"\n")


def get_amount():
    """Get valid donation amount from user"""
    while True:
        try:
            amount = input("How much did they donate: ")
            if str(amount).lower() == 'exit':
                return amount
            else:
                return float(amount)
        except ValueError:
            print("you have made an invalid choice, try again.")


def menu_page(option=None):
    """ Return valid menu option from user """
    while True:
        try:
            print("Please choose one of the following options(1,2,3,4):"
                  "\n1. Send a Thank you. \n2. Create a report"
                  "\n3. Delete a donation \n4. Quit")
            option = int(input('--->'))
        except ValueError:
            print("You have made an invalid choice, try again.")
            page_break()
            continue
        return option


def send_thanks():
    """ Send Thanks """
    page_break()
    while True:
        print("To whom would you like to say thank you?\n"
              "(type \"list\" for a full list of names or"
              "\"exit\" to return to the menu)")
        name = input("--->")
        if name == 'list':
            print(("{}\n"*len(get_donor_list())).format(*get_donor_list()))
            continue
        add_donation(name)
        break


def create_report():
    """ Create Report """
    database = SqliteDatabase('mailroom.db')
    database.execute_sql('PRAGMA foreign_keys = ON;')

    donor_list = []
    for donor in Donor.select():
        donor_list.append(donor)

    report = []
    page_break()
    col_lab = ["Donor Name", "Total Given", "Num Gifts", "Average Gift"]
    max_name = max([len(donor.donor_name) for donor in Donor.select()])
    max_don = max([donor.donation_total for donor in Donor.select()])
    float_max = (f"{(max_don):,.2f}")
    max_donl = len(str(float_max))
    max_gift = len(col_lab[2])
    if max_donl < len(col_lab[1]):
        max_donl = len(col_lab[1])
    format_col = "\n{:<" + "{}".format(max_name+5) + "}|{:^"
    format_col += "{}".format(max_donl+5)
    format_col += "}|{:^" + "{}".format(max_gift+5)
    format_col += "}|{:>" + "{}".format(max_donl+5) + "}"
    print(format_col.format(*col_lab))
    print("-"*len(format_col.format(*col_lab)))

    sorted_list = (sorted(donor_list, key=total_key, reverse=True))
    #return(sorted(Donors, key=donation_total reverse=True))
    for name in sorted_list:
        num_gifts = name.number_of_donations
        avg_gift = name.donation_total/donor.number_of_donations
        format_item = "{:<" + "{}".format(max_name+5) + "}${:>"
        format_item += "{}".format(max_donl+5) + ",.2f}{:>"
        format_item += "{}".format(max_gift+5) + "d} ${:>"
        format_item += "{}".format(max_donl+5) + ",.2f}"
        report.append(format_item.format(name.donor_name, name.donation_total,
                                         num_gifts, avg_gift))
    report.append(f"Total raised = $ {sum(donor.donation_total for donor in donor_list):,.2f} "
                   "from {donors_obj.total_donations} donations")
    return '\n'.join(report)


def total_key(donor):
    """ Return total donation key for sorting function """
    return(donor.donation_total)


def print_report(donors_obj=None):
    print(create_report())


#def send_letters(dir_path=None, donor_obj=None):
    #""" Write letters to each donor in the donor chart and
        #save them in a user specified directory """
    #if not dir_path:
        #dir_path = input("Please type the desired directory "
                         #"to save the letters: ")
    #if not donor_obj:
        #donor_obj = dc
    #letter_form = ("Dear {},\n\n\tThank you for your very "
                   #"kind donation of ${:,.2f}!")
    #letter_form += ("\n\n\tNow all of the kittens will "
                    #"get to eat this year!")
    #letter_form += ("\n\n\t\t\t\t Cheers! \n\t\t\t\t "
                    #"-The Team")
    #if dir_path.lower() == "exit":
        #return
    #if not os.path.exists(dir_path):
        #print("That is not a valid directory, using working directory")
        #dir_path = os.getcwd()
    #for donor in donor_obj.donors:
        #file_name = (f"{donor.full_name}.txt")
        #path_name = os.path.join(dir_path, file_name)
        #with open(path_name, 'w') as cur_file:
            #cur_file.write(letter_form.format(donor.full_name,
                                              #sum(donor.donations)))
    #print(f"Letters saved in {dir_path}")


def add_donation(name):
    """ add a donation for a new or existing donor """
    database = SqliteDatabase('mailroom.db')
    if name not in get_donor_list():
        addname = input("The name you selected is not in the list,"
                        " would you like to add it(y/n)? ")
        if addname[0].lower() == 'y':
            try:
                database.connect()
                database.execute_sql('PRAGMA foreign_keys = ON;')
                with database.transaction():
                    new_donor = Donor.create(
                        donor_name = name
                    )
                    logger.info('Donor {} was added to db'.format(name))
            except Exception as e:
                logger.error('Unable to create a record for {}. Err: {}'.format(name, e))            
        elif addname.lower() == 'exit':
            return
        else:
            print("\nName was not added, try again\n")
            return
    amount = get_amount()
    try:
        with database.transaction():
            new_donation = Donations.create(
                donation_name = name,
                donation_amount = amount)
            logger.info('Donor {} was added to db'.format(name))
    except Exception as e:
        logger.error('Unable to create a record for {}. Error: {}'.format(name, e))
    finally:
        update_donors()
        database.close()


def delete_donor():
    """remove a donor from the database"""
    delete_name = input("Whose donations are we removing from the database? \n")

    database = SqliteDatabase('mailroom.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        if delete_name in get_donor_list():
            delete_this_donor = Donor.get(Donor.donor_name == delete_name)
            delete_this_donor.delete_instance()

            delete_this_donor = Donations.get(Donations.donation_name == delete_name)
            delete_this_donor.delete_instance()
            print("{} has been removed from the datbase.".format(delete_name))

        else:
            print("Can't find the name you want to delete.")


    except Exception as e:
        logger.info(e)
    finally:
        database.close()


#def challenge_proj(factor=2, min_donation=0, max_donation=9999999999):
    #print('Current Donation List')
    #for donor in dc.donors:
        #str_form1 = "{}'s current donations are: "
        #str_form1 += "${:.2f} " * len(donor.donations)
        #str_form1 += "\n{}'s current total: ${:.2f}"
        #print(str_form1.format(donor.full_name, *donor.donations,
                               #donor.full_name, donor.total_donation))
    #print(f"\nCurrent Total from all donors: ${dc.total_raised:.2f}")
    #page_break()
    #while True:
        #try:
            #factor = float(input("Factor to multiply donations by: "))
            #break
        #except ValueError:
            #print("\nInvalid input\n")
    #while True:
        #try:
            #min_donation = float(input("Minimum Donation"
                                       #"(type '-1' to skip min): "))
            #break
        #except ValueError:
            #print("\nInvalid input\n")
    #while True:
        #try:
            #max_donation = float(input("Maximum Donation"
                                       #"(type '-1' to skip max): "))
            #break
        #except ValueError:
            #print("\nInvalid input\n")
    #filt_dc = DonorChart()
    #mult_dc = DonorChart()
    #if min_donation != -1 and max_donation == -1:
        #filt_dc = dc.min_filter(min_donation)
    #elif max_donation != -1 and min_donation == -1:
        #filt_dc = dc.max_filter(max_donation)
    #else:
        #filt_dc = dc.min_filter(min_donation)
        #filt_dc = filt_dc.max_filter(max_donation)
    #mult_dc = filt_dc.mult_donations(factor)
    #page_break()
    #if min_donation != -1 and max_donation == -1:
        #print('Updated Donation List')
        #for donor in mult_dc.donors:
            #str_form2 = "{}'s donations when multiplying donations "
            #"greater than ${} by {}: "
            #str_form2 += "${:.2f} "*len(donor.donations)
            #str_form2 += "\n{}'s new total: ${:.2f}"
            #print(str_form2.format(donor.full_name, min_donation, factor,
                                   #*donor.donations, donor.full_name,
                                   #donor.total_donation))
    #elif max_donation != -1 and min_donation == -1:
        #for donor in mult_dc.donors:
            #str_form2 = "{}'s donations when multiplying "
            #"donations less than ${} by {}: "
            #str_form2 += "${:.2f} "*len(donor.donations)
            #str_form2 += "\n{}'s new total: ${:.2f}"
            #print(str_form2.format(donor.full_name, max_donation, factor,
                                   #*donor.donations, donor.full_name,
                                   #donor.total_donation))
    #else:
        #for donor in mult_dc.donors:
            #str_form2 = "{}'s donations when multiplying donations "
            #"between ${} and ${} by {}: "
            #str_form2 += "${:.2f} "*len(donor.donations)
            #str_form2 += "\n{}'s new total: ${:.2f}"
            #print(str_form2.format(donor.full_name, min_donation, max_donation,
                                   #factor, *donor.donations, donor.full_name,
                                   #donor.total_donation))
    #print(f"\nYour contribution total would be: ${mult_dc.total_raised:.2f}")
    #print(f"New Total from all contributions: "
           #"${mult_dc.total_raised+dc.total_raised:.2f}")


def menu_quit():
    """ return quit for menus """
    return "Quit"


#dc = DonorChart([Donor("Justin", "Thyme", [1, 1, 1]),
                #Donor("Beau", "Andarrow", [207.121324,
                                           #400.321234, 12345.001234]),
                #Donor("Crystal", "Clearwater", [80082]),
                #Donor("Harry", "Shins", [1.00, 2.00, 3.00]),
                #Donor("Bob", "Zuruncle", [0.53, 7.00]),
                #Donor("Al", "Kaseltzer", [1010101, 666.00]),
                #Donor("Joe", "Somebody", [25])])

options = range(1, 5)
test_dump = "C:/Users/chris.kenyon/Documents/Kenyon/UWPython/Testing_File_dump"
menus = (send_thanks, print_report, delete_donor, menu_quit)
menu_dict = dict(zip(options, menus))

if __name__ == '__main__':
    option = 0
    while True:
        page_break()
        try:
            option = menu_page()
            #if option == 3:
                #menu_dict[option](test_dump)
            if menu_dict[option]() == "Quit":
                break
        except KeyError:
            print("You have made an invalid choice, try again.")
            page_break()
