# # Create project
# def create_project(conn, name, start_date, end_date = False):
    
#     """Creates new cross-stitch project (if not existing)."""
    
#     cursor = conn.cursor()
#     cursor.execute("""
#                    SELECT * FROM project_details
#                    """)
    
#     output = cursor.fetchall()
    
#     if len(output) > 0:
#         cursor.execute("""
#                        INSERT INTO project_details (name, start_date, end_date)
#                        VALUES (?, date(?), ?)
#                        """,
#                        (name, start_date, end_date))
        
#         conn.commit()
#         cursor.close()
#         return True
        
#     else:
#         cursor.close()
#         return False
    
    

# Edit project details (including set end date)

# Add to project floss

# Delete from project floss

# Show all projects (names & details)

# Show project (join project_details with project_floss + availabilites)
