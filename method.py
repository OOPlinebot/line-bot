import requests
import json
from datetime import datetime, timedelta

base_url = "https://9ba4-140-117-172-227.ngrok-free.app/api"
# 取得所有users
def list_users():
    url = f"{base_url}/users"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching users: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to decode JSON response for users")
        return []
# 取得所有information
def list_details(id_number):
    url = f"{base_url}/users/{id_number}/details"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching users: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to decode JSON response for users")
        return []
# 使用者資訊回傳(Car)
def get_car_details_client_(id_number):
    user = list_details(id_number)['user']
    licenses = list_details(id_number)['licenses']
    car_record = [car for car in licenses if car['license_type'] == 'Car']
    messages = []

    if car_record:
        car = car_record[0]  
        messages.append(
            "Car License Info:\n"
            f"License type: {car.get('license_type', 'N/A')}\n"
            f"Sex: {user.get('sex', 'N/A')}\n"
            f"Birthday: {user.get('birthday', 'N/A')}\n"
            f"Contact: {user.get('contact', 'N/A')}\n"
            f"Expires: {car.get('license_expiry_date', 'N/A')}\n"
            f"License number: {car.get('license_number', 'N/A')}\n"
            f"Name: {user.get('name', 'N/A')}\n"
            f"Your ID number: {user.get('id_number', 'N/A')}"
        )
   
    return "".join(messages)
# 使用者資訊回傳(Motorcycle)
def get_moto_details_client_(id_number):
    user = list_details(id_number)['user']
    licenses = list_details(id_number)['licenses']
    motorcycle_record = [moto for moto in licenses if moto['license_type'] == 'Motorcycle']
    messages = []

    if motorcycle_record:
        motorcycle = motorcycle_record[0]  
        messages.append(
            "Motorcycle License Info:\n"
            f"License type: {motorcycle.get('license_type', 'N/A')}\n"
            f"Sex: {user.get('sex', 'N/A')}\n"
            f"Birthday: {user.get('birthday', 'N/A')}\n"
            f"Contact: {user.get('contact', 'N/A')}\n"
            f"Expires: {motorcycle.get('license_expiry_date', 'N/A')}\n"
            f"License number: {motorcycle.get('license_number', 'N/A')}\n"
            f"Name: {user.get('name', 'N/A')}\n"
            f"Your ID number: {user.get('id_number', 'N/A')}"
        )
   
    return "".join(messages)
# 違規資訊回傳
def get_violation_details_client_side(id_number):
    user = list_details(id_number)['user']
    violations = list_details(id_number)['licenses'][0]['violations']

    result = []
    for v in violations:
        fine_amount = v.get("fine_amount", "N/A")
        payment_status = v.get("payment_status", "N/A")
        violation_date = v.get("violation_date", "N/A")
        violation_type = v.get("violation_type", "N/A")
        id_number = v.get("id_number", "N/A")

        message = (
            f"Violation type:\n{violation_type}\n\n"            
            f"Violation date:\n{violation_date}\n\n"
            f"Fine:\n{fine_amount}\n\n"
            f"Payment status:\n{payment_status}\n\n"
            f"Your ID number:\n{id_number}\n{'='*18}\n"
        )
        result.append(message)
    return ''.join(result)
# ID是否存在
def id_exist(id_number):
    users = list_users()
    for user in users:
        if user.get('id_number') == id_number:
            return True    
    return False
# 到期前通知
def notify_license_expiry(id_number):
    user_details = list_details(id_number)
    user = user_details['user']
    licenses = user_details['licenses']
    now = datetime.now()
    message = []
    for license in licenses:
        expiry_date_str = license.get('license_expiry_date')
        if expiry_date_str:
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
            if 0 < (expiry_date - now).days <= 365:  # 一年內到期
                message.append(
                    f"Your {license['license_type']} license is about to expire "
                    f"on {expiry_date.strftime('%Y-%m-%d')}.\nPlease renew it as soon as possible.\n"
                )
    return ''.join(message)