import asyncpg

async def connect_db():
    return await asyncpg.connect(
        user='postgres',
        password='1425',
        database='postgres',
        host='localhost'
    )

async def create_table():
    conn = await connect_db()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            phone_number VARCHAR(255)
        );
    ''')
    await conn.close()

async def save_user_info(user_id, first_name, last_name, phone_number):
    conn = await connect_db()
    try:
        await conn.execute('''
            INSERT INTO users (user_id, first_name, last_name, phone_number)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id) DO UPDATE 
            SET first_name = $2, last_name = $3, phone_number = $4;
        ''', user_id, first_name, last_name, phone_number)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await conn.close()
