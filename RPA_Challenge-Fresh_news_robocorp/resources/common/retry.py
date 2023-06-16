import time

def perform_action_with_retry(action_func, max_retries, retry_interval):
    retries = 0
    while retries < max_retries:
        try:
            action_func()  # Perform the action
            break  # If the action is successful, exit the loop
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print("Retrying...")
            retries += 1
            time.sleep(retry_interval)

    if retries == max_retries:
        raise Exception("Maximum number of retries reached. Exiting.")