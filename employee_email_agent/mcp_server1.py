from fastmcp import FastMCP
from typing import List, Dict, Any, Optional

# Import with clear aliases to avoid naming conflicts
#from agent import get_employees as get_employees_from_db
from agent import query_employees as query_employees_from_db
from agent import send_email as send_email_to_employee

# app = FastMCP(
#     name="Employee Email Agent MCP Server",
#     instructions="""
#     Use get_employees_tool to find employees by department (e.g. Sales, Engineering), geo_location (e.g. US, New York, EU), and/or role.
#     Any parameter can be left out (pass None or omit) to get broader results.
#
#     Only call send_email_tool when the user explicitly asks to send an email or clearly confirms.
#
#     Always present the list of found employees (names and emails) in a clear, readable way before suggesting to send email.
#     Be professional, polite, and confirm before sending any message.
#     """)
app = FastMCP(
    name="Employee Email Agent MCP Server",
    instructions="""
    Use query_employees_tool to Executes a SQL query against the employees database and returns results..
    
    Only call send_email_tool when the user explicitly asks to send an email or clearly confirms.

    Always present the list of found employees (names and emails) in a clear, readable way before suggesting to send email.
    Be professional, polite, and confirm before sending any message.
    """)
# ────────────────────────────────────────────────
# Register tools with better signatures for MCP clients
# ────────────────────────────────────────────────

# @app.tool
# def query_employees_tool(
#     department: Optional[str] = None,
#     geo_location: Optional[str] = None,
#     role: Optional[str] = None
# ) -> List[Dict[str, Any]]:
#     """
#     Fetches employees from the database based on filters if any.
#     Args:
#         department (str, optional): The department to filter employees by.
#         geo_location (str, optional): The geographical location to filter employees by.
#         role (str, optional): The role to filter employees by.
#     Returns:
#         List[Dict[str, Any]]: A list of dictionaries containing employee names and emails.
#     """
#     return get_employees_from_db(department, geo_location, role)

@app.tool
def query_employees_tool(sqlQuery: str) :
    """
    Executes a SQL query against the employees database and returns results.
    Args:
        sqlQuery (str): The SQL query to execute.

    """
    return query_employees_from_db(sqlQuery)

@app.tool
def send_email_impl(
        name: str,
        email: str,
        subject: str,
        body: str
    ) -> str:
        """
        Simulates sending an email to an employee.
        Args:
            name (str): The name of the email recipient.
            email (str): Email address to send to.
            subject (str): The subject of the email.
            body (str): The body content of the email.
        Returns:
            str: A confirmation message indicating the email was sent.
        """
        return send_email_to_employee(name, email, subject, body)

if __name__ == "__main__":
    app.run(transport="stdio")
