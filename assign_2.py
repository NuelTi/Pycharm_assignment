# personalized birthday wishes

recipient_name = input("Please enter your name: ")
year_of_birth = int(input("Please enter year of birth: "))
personalized_message = input("please write a short personalized message: ")
sender_name = input("Please enter sender's name: ")


from datetime import datetime
current_year = datetime.now().year
age = current_year - int(year_of_birth)

print(f"{recipient_name}, let's celebrate your {age} years of awesomeness! ")
print(f"Wishing you a day filled with joy and laughter as you turn {age} ! ")
print(f"{personalized_message} With love and best wishes, {sender_name} ")




