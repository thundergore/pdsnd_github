import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ('chicago', 'new york city', 'washington')
MONTHS = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
DAYS = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city_input = input("\nPlease type in a city. Choose from the following: \nChicago \nNew York City or\nWashington\n: ")
    while city_input.lower() not in CITIES:
        city_input = input("\nHmm, we've no city like that on record, try typing in: \nChicago \nNew York or\nWashington\n: ")
    else:
        city = city_input.lower()

    month_input = input("\nPlease choose a month between January and June (or 'all') in which to view data\n: ")
    while month_input.lower() not in MONTHS:
        month_input = input("\nHmm, we've no month like that on record, try typing in a month between January and June (or 'all')\n: ")
    else:
        month = month_input.lower()

    day_input = input("\nPlease choose a day (or type 'all') in which to view data\n: ")
    while day_input.lower() not in DAYS:
        day_input = input("\nHmm, we've no day like that on record, try typing in a day of the week (or 'all')\n: ")
    else:
        day = day_input.lower()

    print('-'*40)
    print(city, month, day)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    """Added hour here as I encountered an error for hour when debugging"""
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('\n Most common month of travel is: ', common_month)
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\n Most common day of travel is: ', common_day)
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('\n Most common hour of travel is: ', common_hour)

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('\nThe most commonly used departure station is: ', common_start)
    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nThe most commonly used arrival station is: ', common_end)
    # display most frequent combination of start station and end station trip
    common_combo = df.groupby(['Start Station','End Station']).size().idxmax()
    print('\nThe most common combination of departure/arrival stations is: ', common_combo)

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum(), 3)
    print("\nThe total travel time for trips in this data slice is: ", total_travel_time)

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean(), 3)
    print("\nThe mean travel time for trips in this data slice is: ", mean_travel_time)

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("\n The user type count is: ", user_type_count)

    # Display counts of gender
    #After an embarassing amount of debugging I realised Washington is missing last 2 columns
    if 'washington' in city is False:
        gender_count = df['Gender'].value_counts()
        print("\n The gender count is: ", gender_count)

        # Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        latest_yob = df['Birth Year'].max()
        most_common_yob = df['Birth Year'].mode()[0]
        print("\nThe most common birth year is {}. The earliest birth year is {}. And the latest birth year is {}.".format(int(most_common_yob), int(earliest_yob), int(latest_yob)))

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def rawdata(df):
    """Created to satisfy rubric for this project"""
    first_five = 0
    view_data = input("\nWould you like to see more individual trips from your filtered data? Enter yes or no.\n")
    while view_data.lower() == 'yes':
      print(df.iloc[first_five:first_five + 5])
      first_five += 5
      view_data = input("Do you wish to continue? Enter yes or no: ")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
