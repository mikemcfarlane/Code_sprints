/*
Functional methods for BankDemo.
*/

import java.io.*;

public class CheckingAccount{
	private double balance;
	private int number;

	public CheckingAccount(int number){
		this.number = number;
	}

	public void deposit(double amount){
		balance += amount;
		System.out.println("\nYour new balance is £" + balance);
	}

	public void withdraw(double amount) throws InsufficientFundsException{
		if (amount <= balance){
			balance -= amount;
			System.out.println("\nYour new balance is £" + balance);
		}
		else{
			double needs = amount - balance;
			throw new InsufficientFundsException(needs);
		}
	}

	public double getBalance(){
		return balance;
	}

	public int getNumber(){
		return number;
	}
}