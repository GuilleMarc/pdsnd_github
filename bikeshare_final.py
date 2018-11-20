########### Python - Udacity Project ###################################
## Bikeshare data statistics
## Guillermo Marcillo
## Last update: 10/14/2018

import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months= pd.Series(['january', 'february', 'march', 'april', 'may', 'june'])

days= pd.Series(['monday','tuesday','wednesday','thursday','friday','saturday','sunday'],
                                index=list(range(0,7)))


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

    while True:
        print('\n Currently we have data for new york city, chicago, or washington only')
        city= input('Please provide the name of a city, e.g(chicago) :')

        print('\n Currently we have data from january to june only ')
        month= input('Which month you want your data summaries for, e.g(june, or "all" if no filter needed) :')

        day= input('\n What day of the week you want your summaries for, e.g(friday, or "all" if no filter needed) :')

        ### Checking if inputs meet conditions: e.g. lowercase only:
        if (city != city.lower()) and (month != month.lower()) and (day != day.lower()):
            print('\n No valid inputs, insert lowercase only please')
        else:
            city, month, day = city, month, day
            break
    print('-'*40)
    return city,month,day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday


    # filter by month if applicable
    if month != 'all':
        # use the months series to get the month index (see line 14)
        month= months[months == month].index[0] + 1
        # filter by month to create the new dataframe
        df = df[df.month == month]

    # filter by day of week if applicable
    if day != 'all':
        #use the days series to get day index (see line 16)
        day_index= days[days == day].index[0]
        #filter by day of week to create the new dataframe
        df = df[df.day_of_week == day_index]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('\n Month with most trips is: \n')
    print(months[df.month.mode()[0]-1])
    #print(df.month.mode()[0])


    # TO DO: display the most common day of week
    print('\n Day of the week with most trips: \n')

    print(days[df.day_of_week.mode()[0]])
    #print(df.day_of_week.mode()[0])


    # TO DO: display the most common start hour
    print('\n Hour of the day where most trips start: \n')
    hour_of_day= pd.to_datetime(df['Start Time']).dt.hour.mode()[0]
    if hour_of_day < 12:
        print(str(hour_of_day)+' am')
    else:
        print(str(hour_of_day-12)+' pm')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\n Most commonly used start station: \n')
    print(df['Start Station'].mode()[0])


    # TO DO: display most commonly used end station
    print('\n Most commonly end start station: \n')
    print(df['End Station'].mode()[0])


    # TO DO: display most frequent combination of start station and end station trip
    agg_station= df.groupby(by=['Start Station','End Station']).size()
    most_used_station= agg_station.sort_values(ascending=False).index[0]

    print('\n Most frequent combination of start-ending stations for a trip: \n')
    print(most_used_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('\n Total travel time: \n')
    print(str(df['Trip Duration'].sum()/3600) + " hours")


    # TO DO: display mean travel time
    print('\n Average travel time: \n')
    print(str(df['Trip Duration'].mean()/3600) + " hours")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\n User types: \n')
    print(df.groupby(by='User Type').size().sort_values(ascending=False))

    # TO DO: Display counts of gender
    print('\n User by gender: \n ')

    if 'Gender' not in df.columns:
        print('No gender information was available for this city')
    else:
        print(df.Gender.value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    print('\n Year of birth of users: \n')

    try:
        earliest= int(df['Birth Year'].max())
        most_recent= int(df['Birth Year'].min())
        most_common= int(df['Birth Year'].mode()[0])
        print('earliest year:{}\n Most recent year: {}\n Most common year: {}'.format(earliest, most_recent, most_common))
    except KeyError:
        print('No year of birth was available for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df= load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        want_raw= input('\nWould you like to see a few data used in our calculations? \n')
        if want_raw == 'yes':
            print('\n Dataset for {}'.format(city))
            print(df.head())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()
