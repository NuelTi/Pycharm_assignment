# Package Loading Program
def main():
    MAX_CAP = 20
    MIN_ITEM, MAX_ITEM = 1, 10

    # read maximum number of items
    while True:
        try:
            max_items = int(input("Please enter a max number of items to be shipped: "))
            if max_items >= 0:
                print("The maximum number of items you can ship is:", max_items)
                break
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please try again.")

    packages_sent = 0
    total_weight = 0
    unused_capacity = 0
    unused_capacities = []
    current_weight = 0

    for i in range(max_items):
        try:
            weight = float(input(f"Please enter the weight of item {i + 1} (0 to stop): "))

            if weight == 0:
                print("Terminated as weight 0 was entered.")
                break

            if weight < MIN_ITEM or weight > MAX_ITEM:
                print("Invalid weight value. Please enter a weight between 1 and 10 kg.")
                continue

            # Check if adding exceeds capacity
            if current_weight + weight > MAX_CAP:
                packages_sent += 1
                total_weight += current_weight
                unused = MAX_CAP - current_weight
                unused_capacity += unused
                unused_capacities.append(unused)

                current_weight = weight
            else:
                current_weight += weight

        except ValueError:
            print("Invalid input. Please try again with a valid number.")

    # Handle last package
    if current_weight > 0:
        packages_sent += 1
        total_weight += current_weight
        unused = MAX_CAP - current_weight
        unused_capacity += unused
        unused_capacities.append(unused)

    # Find package with max unused capacity
    if unused_capacities:
        max_unused_capacity = max(unused_capacities)
        package_number = unused_capacities.index(max_unused_capacity) + 1
    else:
        max_unused_capacity = 0
        package_number = 0

    # Display results
    print("\nSummary of Packages Sent:")
    print(f"Number of packages sent: {packages_sent}")
    print(f"Total weight of packages sent: {total_weight} kg")
    print(f"Total unused capacity: {unused_capacity} kg")
    print(f"Package with most unused capacity: {package_number} (Unused: {max_unused_capacity} kg)")


# Run the program
if __name__ == "__main__":
    main()