# core/scheduler.py
from datetime import datetime, timedelta

class Scheduler:
    """
    Handles temporal constraints. Ensures that connections are 
    only valid if they depart after the arrival time at the node.
    """
    
    @staticmethod
    def parse_time(time_str):
        """Converts 'HH:MM' string to datetime object."""
        return datetime.strptime(time_str, "%H%M")

    @staticmethod
    def get_valid_edges(edges, current_time_str):
        """
        Filters edges based on the time.
        current_time_str: The arrival time at the current station (e.g., '10:30')
        """
        valid_edges = []
        current_time = Scheduler.parse_time(current_time_str)
        
        for edge in edges:
            departure_time = Scheduler.parse_time(edge['departure'])

            if departure_time >= current_time:
                valid_edges.append(edge)
                
        return valid_edges