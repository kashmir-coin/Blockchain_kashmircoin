from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)

# Initialize Flask app
app = Flask(__name__)

# In-memory databases (can be replaced with real blockchain nodes in the future)
wallets = {}
transactions = []

# Function to generate a secure wallet (private and public key)
def generate_wallet():
    private_key = ''.join(random.choices(string.ascii_letters + string.digits, k=64))  # 64 characters for private key
    public_address = ''.join(random.choices(string.ascii_letters + string.digits, k=34))  # 34 characters for public address
    wallet = {"private_key": private_key, "public_address": public_address}
    wallets[public_address] = wallet
    return wallet

# Endpoint for generating a wallet
@app.route('/generate_wallet', methods=['GET'])
def generate_wallet_route():
    wallet = generate_wallet()
    return jsonify(wallet)

# Function to get the balance for an address (mock)
def get_balance(address):
    if address in wallets:
        # In real scenarios, balance would come from blockchain nodes
        balance = random.randint(0, 1000)  # Mock balance
        return balance
    return None

# Endpoint for retrieving balance of a given address
@app.route('/balance/<address>', methods=['GET'])
def get_balance_route(address):
    balance = get_balance(address)
    if balance is not None:
        return jsonify({"address": address, "balance": balance})
    else:
        return jsonify({"error": "Address not found"}), 404

# Function to send KashmirCoins (mock transaction logic)
def send_transaction_logic(from_address, to_address, amount):
    if from_address not in wallets or to_address not in wallets:
        return {"error": "Invalid address"}
    
    # Mock blockchain logic here (replace with real blockchain validation)
    transaction = {
        "from": from_address,
        "to": to_address,
        "amount": amount,
        "transaction_id": hashlib.sha256(f"{from_address}{to_address}{amount}".encode()).hexdigest()
    }
    transactions.append(transaction)
    return {"status": "success", "message": "Transaction sent", "transaction": transaction}

# Endpoint for sending a transaction
@app.route('/send', methods=['POST'])
def send_transaction_route():
    data = request.get_json()
    from_address = data.get('from')
    to_address = data.get('to')
    amount = data.get('amount')

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    # Process transaction logic
    result = send_transaction_logic(from_address, to_address, amount)

    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

# Endpoint to fetch all transactions (for tracking purposes)
@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

# Health check endpoint for the server
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "KashmirCoin API is up and running."})

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0")
