from app.services.customer import CustomerService


async def generate_answer(query: str, session_id: str):
    customer_service = CustomerService()
    response = await customer_service.generate_answer(query, session_id)
    return response
