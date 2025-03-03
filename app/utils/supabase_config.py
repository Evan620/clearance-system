from supabase import create_client, Client

# Initialize Supabase client
SUPABASE_URL = "https://tqxiwpbqoconvqrjjiap.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRxeGl3cGJxb2NvbnZxcmpqaWFwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA2ODU0MzUsImV4cCI6MjA1NjI2MTQzNX0.KubyjnYPeHCDbws5-LOdjGoOfIfBM9ur_buUPeFd8PE"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Test the connection
    response = supabase.table("departments").select("*").execute()
    print("Database connection test:", response)
    print("Number of departments:", len(response.data))
    
except Exception as e:
    print(f"Failed to connect to Supabase: {e}")
    raise