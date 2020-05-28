import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

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
        city = input('Please enter city(Choosee from chicago, new york city, washington)').lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print('Entered City is not valid. Trying Again')
            continue
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter Month for Filter(all, january, february, ... , june) ').lower()
        if month not in months:
            print('Entered month not valid. Trying Again')
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter day of week for filter(all, monday, tuesday, ... sunday) ').lower()
        if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print('Entered day not valid. Trying Again')
            continue
        else:
            break
    print('-' * 40)
    return city, month, day


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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #  filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month.lower())

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.

    Args:
        df - pandas DataFrame containing city data filtered by month and day
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        print('\nMost Common Month is {}\n'.format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    if day == 'all':
        print('Most Common Day of the Week is {}'.format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print('Most Common Hour of the Day is {}'.format(df['Start Time'].dt.hour.mode()[0]))

    # Print execution time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nMost commonly used start station is {}\n'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('\nMost commonly used End station is {}\n'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' -> ' + df['End Station']
    popular_route = df['route'].mode()[0]
    print('\nMost commonly used start/end station route is {}\n'.format(popular_route))

    # Print execution time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    # Function to convert seconds into days hours and min
    def time_cal(seconds):
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60
        days = seconds // seconds_in_day
        hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
        minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
        second = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour) - (minutes * seconds_in_minute))
        return (days, hours, minutes, second)

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    days, hours, minutes, seconds = time_cal(df['Trip Duration'].sum())
    print('\nTotal travel time for the filtered dataset is {} days {} hours {} minutes & {} seconds\n'
          .format(days, hours, minutes, seconds))

    # TO DO: display mean travel time
    days, hours, minutes, seconds = time_cal(df['Trip Duration'].mean())
    print('\nAverage travel time for the filtered dataset is {} days {} hours {} minutes & {} seconds\n'
          .format(days, hours, minutes, seconds))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Cleansing Nan values in gender
    df['Gender'] = df['Gender'].fillna(value='unknown')
    # TO DO: Display counts of user types
    print('Count of the User Types are as follows')
    print(df['User Type'].value_counts(), '\n')
    # TO DO: Display counts of gender
    print('Count of the User Genders are as follows')
    print(df['Gender'].value_counts(), '\n')
    # TO DO: Display earliest, most recent, and most common year of birth
    print('Earilest Year of Birth for Members is {}\n'.format(int(df['Birth Year'].min())))
    print('Recent Year of Birth for Members is {}\n'.format(int(df['Birth Year'].max())))
    print('Most common Year of Birth for Members is {}\n'.format(int(df['Birth Year'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # Printing Meny to show Statistics
        print('\n Select from the below Menu(Enter number!)\n')
        print('1. Display statistics on the most frequent times of travel.')
        print('2. Display statistics on the most popular stations and trip.')
        print('3. Display statistics on the total and average trip duration.')
        print('4. Displays statistics on bikeshare users. (Only for Chicago/New York City)')
        print('5. Show 5 rows of raw Data\n')
        while True:
            try:
                menu_num = int(input('Enter Number:'))
            except:
                print('Invalid Number Please try Again')
                continue
            else:
                if menu_num in [1, 2, 3, 4, 5]:
                    break
                else:
                    print('Invalid Number Please try Again')
                    continue
        if menu_num == 1:
            time_stats(df, month, day)
        elif menu_num == 2:
            station_stats(df)
        elif menu_num == 3:
            trip_duration_stats(df)
        elif menu_num == 4:
            if city == 'washington':
                print('Gender & Birtday Data not available for Washington')
            else:
                user_stats(df)
        elif menu_num == 5:
            print(df.head(5))
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
