from flask import Flask, jsonify, request

from expense import Expense, ExpenseSchema
from income import Income, IncomeSchema
from transaction_type import TransactionType
from auth0 import requires_auth, get_token_auth_header

app = Flask(__name__)

transactions = [
  Income('Salary', 5000),
  Income('Dividends', 200),
  Expense('pizza', 50),
  Expense('Rock Concert', 100)
]

@app.route('/incomes')
@cross_origin(headers=['Content-Type', 'Authorization'])
def get_incomes():
  schema = IncomeSchema(many=True)
  incomes = schema.dump(
    filter(lambda t: t.type == TransactionType.INCOME, transactions)
  )
  return jsonify(incomes)  # .dataを削除

@app.route('/incomes', methods=['POST'])
def add_income():
  income = IncomeSchema().load(request.get_json())
  transactions.append(income)  # .dataを削除
  return "", 204

@app.route('/expenses')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_expenses():
  schema = ExpenseSchema(many=True)
  expenses = schema.dump(
      filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
  )
  return jsonify(expenses)  # .dataを削除

@app.route('/expenses', methods=['POST'])
def add_expense():
  expense = ExpenseSchema().load(request.get_json())
  transactions.append(expense)  # .dataを削除
  return "", 204

if __name__ == "__main__":
    app.run()
