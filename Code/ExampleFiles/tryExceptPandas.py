try:
    # Pandas operation
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    # Error handling code
    print("File not found. Please check the file path.")
except ValueError:
    # Error handling code
    print("Error in data. Please ensure correct data format.")
