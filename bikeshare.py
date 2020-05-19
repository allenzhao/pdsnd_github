# Author: Zehan Zhao
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ["all", "janurary", "feburary", "march", "april", "may", "june"]
weekdays = ["all", "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"]


def get_user_input(msg, valid_list):
    """
    Prompts the user to input information and validate the input.

    Args:
        (str) msg - message to display to users
        (list) valid_list - valid input list
    Returns:
        ret - Return value of validated input
    """
    ret = None
    while True:
        ret = input(msg + "\n")
        if ret.lower() in valid_list:
            return ret.lower()
        else:
            print("Input not valid! Please retry your input!")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_input(
        "Please specify the city (chicago, new york city, washington)", CITY_DATA.keys())
    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_user_input(
        "Please specify the name of the month (janurary, feburary, ..., june , or 'all' to apply no filter", months)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input(
        "Please specify the name of the day (monday, tuesday, ..., sunday , or 'all' to apply no filter", weekdays)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour
    if month != 'all':
        month = months.index(month)
        df = df[df["Month"] == month]
    if day != 'all':
        df = df[df["Day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('*' * 40)
    print("The most common month: {}".format(
        months[df['Month'].mode()[0]].title()))
    # TO DO: display the most common day of week
    print("The most common day: {}".format(df['Day'].mode()[0]))
    # TO DO: display the most common start hour
    print("The most common start hour: {}".format(df['Hour'].mode()[0]))
    print('*' * 40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('*' * 40)
    # TO DO: display most commonly used start station
    print("The most common start station: {}".format(
        df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most common end station: {}".format(
        df['End Station'].mode()[0]))
    df['Station Combination'] = df['Start Station'] + ' to ' + df['End Station']
    # TO DO: display most frequent combination of start station and end station trip
    print("The most common frequent combination of start station and end station trip: {}".format(
        df['Station Combination'].mode()[0]))
    print('*' * 40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time: {}".format(df['Trip Duration'].sum()))
    # TO DO: display mean travel time
    print("Mean travel time: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # TO DO: Display counts of user types
        print("User type counts: {}".format(df['User Type'].value_counts()))
        # TO DO: Display counts of gender
        print("Gender counts: {}".format(df['Gender'].value_counts()))
        # TO DO: Display earliest, most recent, and most common year of birth
        print("Earliest birth: {}".format(df['Birth Year'].min()))
        print("Most recent birth: {}".format(df['Birth Year'].max()))
        print("Most common birth: {}".format(df['Birth Year'].mode()[0]))
    except KeyError:
        print("This data set doesn't contain gender/year of birth information")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df, current_loc_display):
    """Displays 5 rows of data."""
    if current_loc_display + 5 < df.shape[0]:
        print(df.iloc[current_loc_display:current_loc_display + 5])
    else:
        print(df.iloc[current_loc_display:df.shape[0]])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        current_loc_display = 0
        while True:
            show_data = input(
                '\nWould you like to view 5 rows of data? Enter yes or no.\n')
            if show_data.lower() != 'yes' or current_loc_display > df.shape[0]:
                break
            display_data(df, current_loc_display)
            current_loc_display += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
