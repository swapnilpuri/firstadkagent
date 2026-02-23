import sqlite3
from google.adk.agents.llm_agent import Agent
from typing import List, Dict, Any
from google.adk.models.lite_llm import LiteLlm
from logging import basicConfig, getLogger, INFO

# ────────────────────────────────────────────────
# Database Setup (runs once when module is imported)
# ────────────────────────────────────────────────
DB_FILE = "employees.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            geo_location TEXT NOT NULL,
            role TEXT 
        )
    ''')

    # Insert Sample data (only if table is empty)
    cursor.execute('SELECT COUNT(*) FROM employees')
    if cursor.fetchone()[0] == 0:
        sample_employees = [
            ("Alice Johnson", "alicejohnson@company.com", "Engineering", "New York", "Software Engineer"),
            ("Bob Smith", "bobsmith@company.com", "Marketing", "San Francisco", "Marketing Manager"),
            ("Charlie Brown", "charliebrown@company.com", "Sales", "Chicago", "Sales Representative"),
            ("Diana Prince", "dianaprince@company.com", "HR", "Los Angeles", "HR Specialist"),
            ("John Doe", "john.doe@company.com", "Sales", "US", "Account Executive"),
            ("Jane Smith", "jane.smith@company.com", "Sales", "US", "Sales Manager"),
            ("Bob Brown", "bob.brown@company.com", "Engineering", "US", "Senior Engineer"),
            ("Charlie Davis", "charlie.davis@company.com", "Engineering", "EU", "DevOps Engineer"),
            ("Dave Evans", "dave.evans@company.com", "Engineering", "EU", "Backend Developer")
        ]
        cursor.executemany('''
            INSERT INTO employees (name, email, department, geo_location, role) VALUES (?, ?, ?, ?, ?)
        ''', sample_employees)

    conn.commit()
    conn.close()

init_db()

# ────────────────────────────────────────────────
# Tools
# ────────────────────────────────────────────────

def query_employees(sqlQuery: str) -> List[Dict[str, Any]]:
    """
    Executes a SQL query against the employees database and returns results.
    Args:
        sqlQuery (str): The SQL query to execute.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(sqlQuery)
        getLogger("query_employees").info(f"Executed query: {sqlQuery}")
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return f"Error executing query: {str(e)}"
    finally:
        conn.close()

def get_employees(department: str= '*', geo_location: str= '*', role: str = '*') -> List[Dict[str, Any]]:
    """
    Retrieves employee names and emails based on department, geo-location, and role.
    Args:
        department (str): The department to filter employees by.
        geo_location (str): The geographical location to filter employees by.
        role (str): The role to filter employees by.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing employee names and emails.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, email FROM employees
            WHERE department = ? AND geo_location = ? AND role = ?
        ''', (department, geo_location, role))
        results = cursor.fetchall()
        conn.close()
        if len(results) == 0:
            return []

        return [{"name": row[0], "email": row[1]} for row in results]
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return []

def send_email(name: str , email:str, subject: str, body: str) -> str:
    """
    Simulates sending an email to an employee.
    Args:
        recipients List[str]: List of email recipients .
        email (str): Email address to send to.
        subject (str): The subject of the email.
        body (str): The body content of the email.
    Returns:
        str: A confirmation message indicating the email was sent.
    """
    # In a real implementation, you would integrate with an email service here.
    print(f"Email sent to {name} ({email}) with subject '{subject}' and body '{body}'")
    return f"Email sent to {name} at {email} with subject '{subject}'"

root_agent = Agent(
    #model=LiteLlm('ollama/gemma3'),
    #model='gemini-2.0-flash',
    model=LiteLlm('openai/gpt-5'),
    name='employee_email_agent',
    description='Queries SQLite DB for employees by department + geography + role and sends emails.',
    instruction=("""
        You are an employee communication assistant.
        RULES: 
        When asked for employees in a department and geography or role: 
        1. Use query_employees tool to fetch the list. 
        2. Return the list of employees (names, emails, roles) clearly to the user. 
        3. After getting results, ALWAYS format them nicely for the user (names and emails).
        NEVER output the tool schema or JSON yourself — the system will handle calling it.
        If the user then asks to send an email (or implies it), 
        Only use send_email AFTER getting explicit permission or clear intent to send.
        Always summarize what was done and show key details. 
        Be polite and confirm actions when sending emails.
        """
    ),
    #tools=[get_employees, send_email],
    tools=[query_employees, send_email]
)
