import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

def start_consumer(script_name):
    """Function to start a consumer process."""
    subprocess.run(["python", script_name])

def get_consumer_scripts(directory):
    """Get a list of all scripts ending with '_consumer.py'"""
    return [
        os.path.join(directory, file) 
        for file in os.listdir(directory) 
        if file.endswith("_consumer.py")
    ]

if __name__ == "__main__":
    # Directory where the consumer scripts are located
    consumers_directory = "events/consumers"
    
    # Get all consumer scripts
    consumer_scripts = get_consumer_scripts(consumers_directory)
    
    # Print the discovered consumer scripts (for debugging)
    print(f"Discovered consumer scripts: {[str(scrpt).split('/')[-1].split('.')[0] for scrpt in consumer_scripts]}")

    # Use ProcessPoolExecutor to run them concurrently
    with ProcessPoolExecutor() as executor:
        executor.map(start_consumer, consumer_scripts)
