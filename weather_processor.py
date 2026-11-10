import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Load and clean weather data with error handling
def load_weather_data(filepath):
    try:
        df = pd.read_csv(filepath, parse_dates=['Date'])
        df.dropna(inplace=True)
        df['Month'] = df['Date'].dt.to_period('M')
        df['MonthStr'] = df['Month'].astype(str)
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

# Calculate statistics per month
def calculate_statistics(df):
    stats = df.groupby('Month').agg({
        'Temperature': ['mean', 'max', 'min'],
        'Rainfall': ['sum', 'mean'],
        'Humidity': 'mean'
    })
    stats.columns = ['Avg_Temp', 'Max_Temp', 'Min_Temp', 'Total_Rain', 'Avg_Rain', 'Avg_Humidity']
    stats.index = stats.index.astype(str)
    stats.reset_index(inplace=True)
    stats.rename(columns={'index': 'Month'}, inplace=True)
    return stats

# Sort data
def sort_data(df, column, ascending=True):
    return df.sort_values(by=column, ascending=ascending)

# Search data by date
def search_by_date(df):
    while True:
        date_str = input("🔎 Enter a date (YYYY-MM-DD), or type 'exit': ")
        if date_str.lower() == 'exit':
            break
        try:
            result = df[df['Date'] == pd.to_datetime(date_str)]
            if not result.empty:
                print(result)
            else:
                print("⚠️ No data found for that date.")
        except Exception as e:
            print(f"❌ Invalid date or error: {e}")

# Search by month
def search_by_month(df):
    month_input = input("📅 Enter month (e.g., 2023-05): ")
    result = df[df['MonthStr'] == month_input]
    if not result.empty:
        print(result)
    else:
        print("⚠️ No data found for that month.")

# Filter by value range
def filter_by_range(df):
    print("🔎 Filter by:")
    print("1. Temperature")
    print("2. Humidity")
    print("3. Rainfall")
    choice = input("Choose (1/2/3): ")
    try:
        min_val = float(input("Min value: "))
        max_val = float(input("Max value: "))
        if choice == '1':
            print(df[(df['Temperature'] >= min_val) & (df['Temperature'] <= max_val)])
        elif choice == '2':
            print(df[(df['Humidity'] >= min_val) & (df['Humidity'] <= max_val)])
        elif choice == '3':
            print(df[(df['Rainfall'] >= min_val) & (df['Rainfall'] <= max_val)])
        else:
            print("❗ Invalid option.")
    except:
        print("❌ Invalid input.")

# Export to CSV
def export_to_csv(df):
    filename = input("📁 Enter filename to save (e.g., export.csv): ")
    try:
        df.to_csv(filename, index=False)
        print(f"✅ Data exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting data: {e}")

# Plot graphs
def plot_graphs(df):
    while True:
        print("\n📊 Graph options:")
        print("1. Average Monthly Temperature")
        print("2. Total Monthly Rainfall")
        print("3. Temperature vs Rainfall Trend")
        print("4. Exit")
        choice = input("Choose (1-4): ")

        if choice == "1":
            monthly_avg_temp = df.groupby('MonthStr')['Temperature'].mean().reset_index()
            plt.figure(figsize=(10, 6))
            plt.plot(monthly_avg_temp['MonthStr'], monthly_avg_temp['Temperature'], marker='o', color='orange')
            plt.title("Average Monthly Temperature")
            plt.xlabel("Month")
            plt.ylabel("Avg Temperature (°C)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("avg_monthly_temperature.png")
            plt.show()

        elif choice == "2":
            monthly_rain = df.groupby('MonthStr')['Rainfall'].sum()
            plt.figure(figsize=(10, 5))
            plt.bar(monthly_rain.index, monthly_rain.values, color='skyblue', edgecolor='black')
            plt.title("Monthly Rainfall")
            plt.xlabel("Month")
            plt.ylabel("Total Rainfall (mm)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig("monthly_rainfall.png")
            plt.show()

        elif choice == "3":
            trends = df.groupby('MonthStr').agg({'Temperature': 'mean', 'Rainfall': 'sum'}).reset_index()
            plt.figure(figsize=(10, 6))
            plt.plot(trends['MonthStr'], trends['Temperature'], label='Temperature (°C)', color='red')
            plt.bar(trends['MonthStr'], trends['Rainfall'], alpha=0.5, label='Rainfall (mm)', color='blue')
            plt.title("Monthly Temperature and Rainfall Trend")
            plt.xlabel("Month")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig("temp_rain_trend.png")
            plt.show()

        elif choice == "4":
            break
        else:
            print("❗ Invalid choice.")

# Save to SQLite
def save_to_database(df, db_name="weather_data.db"):
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql("weather_summary", conn, if_exists="replace", index=False)
        conn.close()
        print(f"✅ Data saved to database: {db_name}")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")

# Display overall summary
def show_summary(df):
    print("\n📌 Summary Stats:")
    hottest_day = df[df['Temperature'] == df['Temperature'].max()]
    coldest_day = df[df['Temperature'] == df['Temperature'].min()]
    wettest_day = df[df['Rainfall'] == df['Rainfall'].max()]
    print("\n🔥 Hottest Day:")
    print(hottest_day)
    print("\n❄️ Coldest Day:")
    print(coldest_day)
    print("\n🌧️ Wettest Day:")
    print(wettest_day)

# Interactive menu
def interactive_menu(df, stats):
    while True:
        print("\n📋 MAIN MENU")
        print("1. View Summary Statistics")
        print("2. Search by Date")
        print("3. Search by Month")
        print("4. Filter by Range")
        print("5. Show Graphs")
        print("6. Export Data to CSV")
        print("7. Exit")
        choice = input("Choose (1-7): ")

        if choice == '1':
            show_summary(df)
        elif choice == '2':
            search_by_date(df)
        elif choice == '3':
            search_by_month(df)
        elif choice == '4':
            filter_by_range(df)
        elif choice == '5':
            plot_graphs(df)
        elif choice == '6':
            export_to_csv(df)
        elif choice == '7':
            print("👋 Exiting program.")
            break
        else:
            print("❗ Invalid choice.")

# Main program
def main():
    filepath = "weather_data.csv"
    df = load_weather_data(filepath)

    if df is None:
        return

    stats = calculate_statistics(df)
    save_to_database(stats)
    interactive_menu(df, stats)

if __name__ == "__main__":
    main()
