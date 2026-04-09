import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Base Class

class Loan:
    def __init__(self, loan_amount, interest_rate, tenure_years):
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.tenure_years = tenure_years
        self.tenure_months = tenure_years * 12

# EMI Calculator Class

class EMICalculator(Loan):

    def calculate_emi(self):
        try:
            r = self.interest_rate / (12 * 100)
            n = self.tenure_months
            p = self.loan_amount

            # zero interest case
            if r == 0:
                return p / n

            emi = (p * r * (1 + r)**n) / ((1 + r)**n - 1)
            return emi

        except Exception as e:
            print("Error in EMI Calculation:", e)


    def calculate_total_payment(self, emi):
        total_payment = emi * self.tenure_months
        total_interest = total_payment - self.loan_amount
        return total_payment, total_interest

# Prepayment Simulator Class

class PrepaymentSimulator(EMICalculator):

    def apply_prepayment(self, prepayment_amount):
        # Validation
        if prepayment_amount > self.loan_amount:
            raise ValueError("Prepayment cannot be greater than loan amount")

        new_loan = self.loan_amount - prepayment_amount

        r = self.interest_rate / (12 * 100)
        emi = self.calculate_emi()

        # zero interest case
        if r == 0:
            new_tenure = int(new_loan / emi)
            return new_loan, new_tenure

        # New tenure calculation
        n = np.log(emi / (emi - new_loan * r)) / np.log(1 + r)
        new_tenure = int(n)

        return new_loan, new_tenure

# Amortization Schedule Class

class AmortizationSchedule(EMICalculator):

    def generate_schedule(self):
        balance = self.loan_amount
        r = self.interest_rate / (12 * 100)
        emi = self.calculate_emi()

        data = []

        for month in range(1, self.tenure_months + 1):
            interest = balance * r
            principal = emi - interest
            balance = max(balance - principal, 0)  

            data.append([month, principal, interest, balance])

        df = pd.DataFrame(data, columns=["Month", "Principal", "Interest", "Balance"])
        return df

# MAIN 

try:
    # Inputs
    loan_amount = float(input("Enter Loan Amount: "))
    interest_rate = float(input("Enter Interest Rate (%): "))
    tenure_years = int(input("Enter Tenure (Years): "))
    prepayment_amount = float(input("Enter Prepayment Amount: "))

    # Objects
    emi_obj = EMICalculator(loan_amount, interest_rate, tenure_years)
    prepay_obj = PrepaymentSimulator(loan_amount, interest_rate, tenure_years)
    schedule_obj = AmortizationSchedule(loan_amount, interest_rate, tenure_years)

    # EMI Calculation
    emi = emi_obj.calculate_emi()
    total_payment, total_interest = emi_obj.calculate_total_payment(emi)

    # Prepayment
    new_loan, new_tenure = prepay_obj.apply_prepayment(prepayment_amount)

    # Schedule
    df = schedule_obj.generate_schedule()

    # File Handling
    df.to_csv("emi_data.csv", index=False)

    with open("loan_summary.txt", "w") as f:
        f.write(f"EMI: {emi}\n")
        f.write(f"Total Payment: {total_payment}\n")
        f.write(f"Total Interest: {total_interest}\n")
        f.write(f"New Loan after Prepayment: {new_loan}\n")
        f.write(f"New Tenure: {new_tenure}\n")

    # Output
    print("\n--- Loan Details ---")
    print("EMI:", round(emi, 2))
    print("Total Payment:", round(total_payment, 2))
    print("Total Interest:", round(total_interest, 2))
    print("New Loan:", round(new_loan, 2))
    print("New Tenure (months):", new_tenure)

    # Visualization

    # Graph 1: Loan Balance
    plt.plot(df["Month"], df["Balance"])
    plt.xlabel("Months")
    plt.ylabel("Remaining Balance")
    plt.title("Loan Balance Reduction")
    plt.show()

    # Graph 2: Interest vs Principal
    plt.plot(df["Month"], df["Interest"], label="Interest")
    plt.plot(df["Month"], df["Principal"], label="Principal")
    plt.xlabel("Months")
    plt.ylabel("Amount")
    plt.title("Interest vs Principal")
    plt.legend()
    plt.show()

except ValueError:
    print("Invalid input! Please enter correct values.")
except Exception as e:
    print("Unexpected Error:", e)
