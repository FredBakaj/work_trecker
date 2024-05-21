import time


class ProfileTracking:
    def delta_time_call(self, name_func: str, func: any) -> any:
        start_time = time.time()
        result = func()
        # Record the end time
        end_time = time.time()
        # Calculate the delta time
        delta_time = end_time - start_time
        print(f"call {name_func} : {delta_time}")
        return result
