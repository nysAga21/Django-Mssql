from django.shortcuts import render
from ok.models import LinkRequests
# myapp/views.py

from django.shortcuts import render
from django.db import connection
from ok.sqlconnection import connect_to_sql_server,execute_query

def employee_list(request):
    data = LinkRequests.objects.all()
    return render(request, 'ok/employee.html', {'data': data})

def new_query(request):
    conn = connect_to_sql_server()
    
    print(conn)
    
    query = 'SELECT AccountNumber FROM CustomerAccounts;'
    
    rows = execute_query(conn, query)
    return render(request, 'ok/query.html', {'account_numbers': rows})

def sanitize_input(input_string):
    # Remove any single quotes from the input string
    sanitized_string = input_string.replace("'", "''")
    return sanitized_string




from django.http import JsonResponse

def get_customer_details(request,account_number):
    # account_number = request.GET.get('account_number')
    sanitized_account_number = sanitize_input(account_number)
    conn = connect_to_sql_server()
    
    query = f"SELECT * FROM CustomerAccounts WHERE AccountNumber = '{sanitized_account_number}'"
    
    row = execute_query(conn, query)
    
    conn.close()
    
    # Extract the retrieved row and map it to a dictionary
    data = {
        'first_name': row[0][1],
        'last_name': row[0][2],
        'email': row[0][3],
        'phone': row[0][4],
    }
    
    return JsonResponse(data)


#for multiple account linkage it would take the first selection and display the information for you, if the first and second choices dont match gives an error to reselect well,
# so aftr taking the first value and diplaying the customer information , it loops through the second and subsequent choices.

from django.http import JsonResponse

def get_ciff(request, ciff):
    conn = connect_to_sql_server()
    
    query1 = f"SELECT AccountNumber FROM Accounts WHERE AccountNumber LIKE '{ciff}%'"
    query2=f"SELECT Tin FROM Accounts WHERE AccountNumber LIKE '{ciff}%' and Tin is not Null"
    query3=f"SELECT IssuerID FROM Accounts WHERE AccountNumber LIKE '{ciff}%' and Tin is not Null"
    query4=f"SELECT AccountType FROM Accounts WHERE AccountNumber LIKE '{ciff}%' and Tin is not Null"
    
    
    row1 = execute_query(conn, query1)
    row2 = execute_query(conn, query2)
    row3 = execute_query(conn, query3)
    row4 = execute_query(conn, query4)
    
    account_numbers = [row[0] for row in row1]  # Extract account numbers from the rows
    tin_number=[row[0] for row in row2]
    issuerid=[row[0] for row in row3]
    account_type=[row[0] for row in row4]
    
    conn.close()
    
    data = {
        "ciffs": account_numbers,
        "tins":tin_number,
        "issuerid":issuerid,
        "account_type":account_type
        
    }
    
    
    return JsonResponse(data)


def makeAccounts(request):
    return render(request, 'ok/aclist.html',)

from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import json


def display(request):
    if request.method == 'POST':
        print("Request Body:", request.body)
        
        
        try:
            data = json.loads(request.body)
            account_numbers = data.get('account_numbers')
            tin = data.get('tin')[0] if data.get('tin') else None
            # account_numbers = data.get('accounts')[0] if data.get('accounts') else None
            issuerid = data.get('issuerid')[0] if data.get('issuerid') else None
            account_type = data.get('account_type')[0] if data.get('account_type') else None
            
            print("tin",tin)
            print("account_numbers",account_numbers)
            print("issuerid",issuerid)
            print("account_type",account_type)


            

            data = {
                "tin": tin,
                "accounts": account_numbers,
                "issuerid":issuerid,
                "account_type":account_type
                
            }
            
            
            my_model_instance = LinkRequests(
                tin=tin,
                issuerid=issuerid,
                account_type=account_type
            )
            
            my_model_instance.save_accounts(account_numbers)

            # Save the instance to the database
            my_model_instance.save()
            return JsonResponse(data)
        
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
            return JsonResponse({"error": "Invalid JSON data"}, status=400)




def link_to_gra(request):
    if request.method == 'POST':
        cif = request.POST.get('tin')
        account_numbers = request.POST.getlist('account_numbers')

        return JsonResponse({'message': 'Success'})
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)  


