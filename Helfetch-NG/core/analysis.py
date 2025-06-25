# core/analysis.py

def get_performance_recommendations(system_data):
    """
    Analyzes system data and provides performance recommendations.
    This is a basic implementation; can be expanded with more complex logic.
    """
    recommendations = []

    # RAM Analysis
    ram_usage_percent_str = system_data.get('RAM Usage %', 'N/A').replace('%', '')
    if ram_usage_percent_str != 'N/A':
        try:
            ram_usage_percent = float(ram_usage_percent_str)
            if ram_usage_percent > 85:
                recommendations.append("RAM usage is very high. Consider closing unnecessary applications or upgrading your RAM for better performance.")
            elif ram_usage_percent > 70:
                recommendations.append("RAM usage is high. You might experience performance slowdowns with many open applications.")
        except ValueError:
            pass

    # CPU Analysis (assuming 'CPU Usage' is like "50.0%")
    cpu_usage_str = system_data.get('CPU Usage', 'N/A').replace('%', '')
    if cpu_usage_str != 'N/A':
        try:
            cpu_usage = float(cpu_usage_str)
            if cpu_usage > 90:
                recommendations.append("CPU usage is extremely high. Your system might be struggling with current tasks. Check running processes.")
            elif cpu_usage > 75:
                recommendations.append("CPU usage is consistently high. This could indicate a demanding application or background process.")
        except ValueError:
            pass

    # Disk Analysis (assuming 'Disk' is like "80%")
    disk_usage_str = system_data.get('Disk', 'N/A').replace('%', '')
    if disk_usage_str != 'N/A':
        try:
            disk_usage = float(disk_usage_str)
            if disk_usage > 90:
                recommendations.append("Disk space is critically low. Freeing up space can improve system responsiveness.")
            elif disk_usage > 80:
                recommendations.append("Disk space is running low. Consider archiving or deleting old files.")
        except ValueError:
            pass
            
    # Kernel Analysis (suggesting updates if older)
    kernel_version = system_data.get('Kernel', 'N/A')
    if kernel_version != 'N/A' and "linux" in kernel_version.lower():
        # This is a very basic check. A real-world scenario would need to
        # check against a database of latest stable kernels.
        # For demonstration, let's assume anything below 5.10 is "old" for modern systems.
        try:
            major_kernel_version = int(kernel_version.split('.')[0])
            if major_kernel_version < 5: # Arbitrary old version threshold
                 recommendations.append(f"Your kernel version ({kernel_version}) might be outdated. Consider updating for better performance, security, and hardware compatibility.")
        except ValueError:
            pass


    # No recommendations
    if not recommendations:
        recommendations.append("Your system appears to be running optimally. Keep up the good work!")
    
    return recommendations

# For testing this module independently
if __name__ == "__main__":
    # Example dummy data for testing
    test_data_optimal = {
        'RAM Usage %': '30%',
        'CPU Usage': '15.0%',
        'Disk': '40%',
        'Kernel': '6.8.0-1007-oem'
    }
    print("Optimal System Recommendations:")
    for rec in get_performance_recommendations(test_data_optimal):
        print(f"- {rec}")

    print("\nHigh RAM Usage System Recommendations:")
    test_data_high_ram = {
        'RAM Usage %': '92%',
        'CPU Usage': '20.0%',
        'Disk': '60%',
        'Kernel': '6.8.0-1007-oem'
    }
    for rec in get_performance_recommendations(test_data_high_ram):
        print(f"- {rec}")

    print("\nHigh CPU & Low Disk Space System Recommendations:")
    test_data_stressed = {
        'RAM Usage %': '75%',
        'CPU Usage': '85.0%',
        'Disk': '95%',
        'Kernel': '4.15.0-20-generic'
    }
    for rec in get_performance_recommendations(test_data_stressed):
        print(f"- {rec}")
