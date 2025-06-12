import random
import string
import time


class GrievanceUtils:
    @staticmethod
    async def generate_complaint_id():
        timestamp = int(time.time())
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"CMP-{timestamp}-{rand}"