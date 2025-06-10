def length_converter():
    print("\nLength Converter:")
    print("1. Meters to Kilometers")
    print("2. Kilometers to Meters")
    print("3. Inches to Centimeters")
    print("4. Centimeters to Inches")
    choice = int(input("Enter your choice: "))
    value = float(input("Enter the value to convert: "))

    if choice == 1:
        print(f"{value} meters = {value / 1000} kilometers")
    elif choice == 2:
        print(f"{value} kilometers = {value * 1000} meters")
    elif choice == 3:
        print(f"{value} inches = {value * 2.54} centimeters")
    elif choice == 4:
        print(f"{value} centimeters = {value / 2.54} inches")
    else:
        print("Invalid choice!")

def weight_converter():
    print("\nWeight Converter:")
    print("1. Kilograms to Grams")
    print("2. Grams to Kilograms")
    print("3. Pounds to Kilograms")
    print("4. Kilograms to Pounds")
    choice = int(input("Enter your choice: "))
    value = float(input("Enter the value to convert: "))

    if choice == 1:
        print(f"{value} kg = {value * 1000} g")
    elif choice == 2:
        print(f"{value} g = {value / 1000} kg")
    elif choice == 3:
        print(f"{value} lb = {value * 0.453592} kg")
    elif choice == 4:
        print(f"{value} kg = {value / 0.453592} lb")
    else:
        print("Invalid choice!")

def temperature_converter():
    print("\nTemperature Converter:")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    choice = int(input("Enter your choice: "))
    value = float(input("Enter the temperature: "))

    if choice == 1:
        print(f"{value}°C = {(value * 9/5) + 32}°F")
    elif choice == 2:
        print(f"{value}°F = {(value - 32) * 5/9}°C")
    else:
        print("Invalid choice!")

def main():
    while True:
        print("\nUnit Converter")
        print("1. Length")
        print("2. Weight")
        print("3. Temperature")
        print("4. Exit")
        category = int(input("Select a category to convert: "))

        if category == 1:
            length_converter()
        elif category == 2:
            weight_converter()
        elif category == 3:
            temperature_converter()
        elif category == 4:
            print("Exiting the Unit Converter.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()