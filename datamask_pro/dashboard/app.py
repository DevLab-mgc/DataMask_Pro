import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os
import sys
from django.db.models import Count, Sum

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Django setup
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datamask_pro.settings')
django.setup()

from core.models import FileUpload, ProcessingLog, PIIDetection, User

def authenticate_user():
    """
    Implement authentication logic 
    In a real-world scenario, this would integrate with Django's authentication
    """
    st.sidebar.header("DataMask Pro Admin Dashboard")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        try:
            # Use Django's authentication method
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            
            if user and user.is_staff:
                st.session_state['authenticated'] = True
                st.session_state['user'] = user
                st.sidebar.success("Logged in successfully!")
            else:
                st.sidebar.error("Invalid credentials or insufficient permissions")
        except Exception as e:
            st.sidebar.error(f"Authentication error: {str(e)}")

def dashboard_overview():
    """Main dashboard with system metrics and visualizations"""
    st.title("DataMask Pro - Admin Dashboard")
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_files = FileUpload.objects.count()
        st.metric("Total Files Processed", total_files)
    
    with col2:
        successful_processes = ProcessingLog.objects.filter(success=True).count()
        st.metric("Successful Processes", successful_processes)
    
    with col3:
        failed_processes = ProcessingLog.objects.filter(success=False).count()
        st.metric("Failed Processes", failed_processes)
    
    # PII Detection Breakdown
    st.subheader("PII Detection Types")
    try:
        pii_types = PIIDetection.objects.values('pii_type').annotate(count=Count('id'))
        pii_df = pd.DataFrame(list(pii_types))
        
        if not pii_df.empty:
            fig = px.pie(pii_df, values='count', names='pii_type', 
                         title='Distribution of PII Types Detected')
            st.plotly_chart(fig)
        else:
            st.write("No PII detection data available")
    except Exception as e:
        st.error(f"Error loading PII detection data: {str(e)}")
    
    # Processing Time Analysis
    st.subheader("Processing Time Distribution")
    try:
        processing_logs = ProcessingLog.objects.filter(processing_time__isnull=False)
        processing_times = list(processing_logs.values_list('processing_time', flat=True))
        
        if processing_times:
            fig = px.histogram(x=processing_times, labels={'x': 'Processing Time (seconds)'}, 
                               title='Distribution of File Processing Times')
            st.plotly_chart(fig)
        else:
            st.write("No processing time data available")
    except Exception as e:
        st.error(f"Error loading processing time data: {str(e)}")

def user_management():
    """User management interface"""
    st.header("User Management")
    
    # List Users
    try:
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                'Username': user.username,
                'Email': user.email,
                'Organization': user.organization,
                'Is Staff': user.is_staff,
                'Date Joined': user.date_joined
            })
        
        users_df = pd.DataFrame(user_data)
        st.dataframe(users_df)
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")

def processing_logs():
    """Display processing logs"""
    st.header("Processing Logs")
    
    try:
        logs = ProcessingLog.objects.all().order_by('-started_at')
        log_data = []
        for log in logs:
            log_data.append({
                'File': log.file_upload.original_filename,
                'Started At': log.started_at,
                'Completed At': log.completed_at,
                'Success': log.success,
                'Processing Time (s)': log.processing_time,
                'Error Message': log.error_message
            })
        
        logs_df = pd.DataFrame(log_data)
        st.dataframe(logs_df)
    except Exception as e:
        st.error(f"Error loading processing logs: {str(e)}")

def main():
    # Check authentication
    if 'authenticated' not in st.session_state:
        authenticate_user()
    
    if st.session_state.get('authenticated', False):
        # Sidebar Navigation
        page = st.sidebar.radio("Navigate", 
            ["Dashboard Overview", "User Management", "Processing Logs"])
        
        if page == "Dashboard Overview":
            dashboard_overview()
        elif page == "User Management":
            user_management()
        elif page == "Processing Logs":
            processing_logs()
    else:
        st.warning("Please log in to access the dashboard")

if __name__ == "__main__":
    main()
