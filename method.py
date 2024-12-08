import requests
import json

base_url = "https://6c26-140-117-172-227.ngrok-free.app/api/"
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
# 取得特定user(可能有兩個因為Car跟Motorcycle)
def get_user_by_id(users, user_id):
    result = []
    for user in users:
        if user.get('user_id') == user_id:
            result.append(user)
    return result
# 取得所有violations
def list_violations():
    url = f"{base_url}/violations"
    try:
        response = requests.get(url)
        response.raise_for_status()
        violations = response.json()
        return violations
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching violations: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to decode JSON response for violations")
        return []
# 取得特定violation(1人可以有多件違規)    
def get_violation_by_id(violations, user_id):
    result = []
    for violation in violations:
        if violation.get('user_id') == user_id:
            result.append(violation)
    return result

def get_notifications(user_id):
    url = f"{base_url}/notifications"
    try:
        response = requests.get(url)
        response.raise_for_status()
        notifications = response.json()
        # Filter notifications for the specific user_id
        user_notifications = [n for n in notifications if n.get('user_id') == user_id]
        return user_notifications
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching notifications: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to decode JSON response for notifications")
        return []
# 使用者資訊回傳(Car跟Motorcycle)
def get_user_details_client_side(user_id):
    users = list_users()
    user = get_user_by_id(users, user_id)
    car_records = [record for record in user if record.get('license_type') == 'Car']
    motorcycle_records = [record for record in user if record.get('license_type') == 'Motorcycle']

    messages = []

    if car_records:
        car = car_records[0]  
        messages.append(
            "Car License Info:\n"
            f"License type: {car.get('license_type', 'N/A')}\n"
            f"Sex: {car.get('sex', 'N/A')}\n"
            f"Birthday: {car.get('birthday', 'N/A')}\n"
            f"Contact: {car.get('contact', 'N/A')}\n"
            f"Expires: {car.get('license_expiry_date', 'N/A')}\n"
            f"License number: {car.get('license_number', 'N/A')}\n"
            f"Name: {car.get('name', 'N/A')}\n"
            f"Your ID number: {car.get('user_id', 'N/A')}"
        )
    if motorcycle_records:
        motorcycle = motorcycle_records[0]  
        messages.append(
            "Motorcycle License Info:\n"
            f"License type: {motorcycle.get('license_type', 'N/A')}\n"
            f"Sex: {motorcycle.get('sex', 'N/A')}\n"
            f"Birthday: {motorcycle.get('birthday', 'N/A')}\n"
            f"Contact: {motorcycle.get('contact', 'N/A')}\n"
            f"Expires: {motorcycle.get('license_expiry_date', 'N/A')}\n"
            f"License number: {motorcycle.get('license_number', 'N/A')}\n"
            f"Name: {motorcycle.get('name', 'N/A')}\n"
            f"Your ID number: {motorcycle.get('user_id', 'N/A')}"
        )
   
    return "".join(messages)
# 違規資訊回傳
def get_violation_details_client_side(user_id):
    violations = list_violations()
    violation = get_violation_by_id(violations, user_id)
    result = []
    for v in violation:
        fine_amount = v["fine_amount"]
        payment_status = v["payment_status"]
        violation_date = v["violation_date"]
        violation_id = v['violation_id']
        violation_type = v['violation_type']
        user_id = v['user_id']

        message = (
            f"Violation type:\n{violation_type}\n\n"
            f"Violation ID:\n{violation_id}\n\n"
            f"Violation date:\n{violation_date}\n\n"
            f"Fine:\n{fine_amount}\n\n"
            f"Payment status:\n{payment_status}\n\n"
            f"Your ID number:\n{user_id}\n{'='*18}\n"
        )
        result.append(message)
    return result
# ID是否存在
def id_exist(user_id):
    users = list_users()
    user = get_user_by_id(users, user_id)
    if not user:
        return False
    return True
