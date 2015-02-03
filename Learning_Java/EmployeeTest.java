/*
Creates employees from the Employee class.
*/

import java.io.*;

public class EmployeeTest{
	public static void main(String args[]){
		// Creates two objects using constructor.
		Employee empOne = new Employee("James Smith");
		Employee empTwo = new Employee("Mary Smith");

		// Invoking methods for each object created.
		empOne.empAge(26);
		empOne.empDesignation("Senior software engineer");
		empOne.empSalary(1000);
		empOne.printEmployee();

		empTwo.empAge(20);
		empTwo.empDesignation("Software engineer");
		empTwo.empSalary(500);
		empTwo.printEmployee();

	}
}