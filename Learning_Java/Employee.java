/*
Creating a Java package.
*/

import java.io.*;

public class Employee{
	public String name;
	private int age;
	public String designation;
	private double salary;

	// This is the constructor of the class Employee.
	public Employee(String name){
		this.name = name;
	}

	// Assign the age of the Employee to the variable age.
	public void empAge(int empAge){
		age = empAge;
	}

	// Assign the designation to the variable designation.
	public void empDesignation(String empDesig){
		designation = empDesig;
	}

	// Assign the salary to the variable salary.
	public void empSalary(double empSalary){
		salary = empSalary;
	}

	// Print the employee details.
	public void printEmployee(){
		System.out.println("Name: " + name);
		System.out.println("Age: " + age);
		System.out.println("Designation: " + designation);
		System.out.println("Salary: " + salary);
	}
}