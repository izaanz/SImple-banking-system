# Simple Banking System with Luhn Algorithm Implementation

This is a simple banking system implemented in Python using SQLite. It allows users to create bank accounts, log in, check their balance, add income, transfer money, and close accounts. 

**Key Feature:** This system utilizes the Luhn algorithm to generate and validate credit card numbers, ensuring the integrity of account information.

## Features

- **Account Creation:** Generates a unique 16-digit card number with a 4-digit PIN. 
    - **Luhn Algorithm:** The system employs the Luhn algorithm to generate valid credit card numbers, enhancing the realism and security of the application.
- **Login:** Securely logs in users using their card number and PIN.
- **Balance Check:** Displays the current account balance.
- **Add Income:** Allows users to deposit funds into their account.
- **Money Transfer:** Enables users to transfer funds to other accounts within the system.
    - **Luhn Validation:** Before processing a transfer, the system validates the recipient's card number using the Luhn algorithm, preventing transfers to invalid accounts.
- **Account Closure:** Allows users to close their account.
- **Data Persistence:** Stores account information in an SQLite database.

## Requirements

- Python 3.x
- SQLite3

## How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/simple-banking-system.git

2. **Navigate to the project directory:**

  ```bash
  cd simple-banking-system
  ```
3. **Run the script:**

```bash
python banking.py 
```
## Usage

The program presents a menu-driven interface. Follow the on-screen prompts to create an account, log in, and perform various banking operations.

## Database

The program creates an SQLite database named card.s3db to store account information. The database has a single table named card with the following columns:

- **id**: Integer, primary key, auto-incrementing
- **number**: Text, unique card number
- **pin**: Text, 4-digit PIN
- **balance**: Integer, account balance (default 0)

## Luhn Algorithm
- The Luhn algorithm (also known as the "modulus 10" or "mod 10" algorithm) is a simple checksum formula used to validate a variety of identification numbers, such as credit card numbers. This system uses the Luhn algorithm in two ways:

  - **Card Number Generation**: During account creation, the system generates a random card number prefix and then calculates the appropriate check digit using the Luhn algorithm to create a valid card number.
  - **Card Number Validation**: When a user enters a card number for a transfer, the system uses the Luhn algorithm to verify that the card number is valid, helping to prevent errors and fraud.

## Example

1. Create an account
2. Log into account
0. Exit

## Note

This project is for educational purposes and should not be used as a real-world banking system.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```
