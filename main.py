from fastapi import FastAPI, HTTPException
import sqlite3


app = FastAPI()

def init_db():
    conn = sqlite3.connect('example.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS items
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
     description TEXT NOT NULL,
     price REAL NOT NULL
     )''')

@app.on_event('startup')
def startup():
    init_db()

@app.post("/items/")
def create_item(name: str, description: str, price: float):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description, price) VALUES (?, ?, ?)",
    (name, description, price)
                   )
    conn.commit()
    item_id = cursor.lastrowid
    return {"id": item_id, "name": name, "description": description, "price": price}

@app.get("/items/")
def read_items():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return {"items": items}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id, ))
    item = cursor.fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail='Item Not Found')
    return {"id": item[0], "name": item[1], "description": item[2], "price": item[3]}


@app.put('/items/{item_id}')
def update_item(item_id: int, name: str, description: str, price: float):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name=?, description=?, price=? WHERE id=?",
                   (name, description, price, item_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Item Updated"}

@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id, ))
    conn.commit()
    conn.close()
    return {"message": "Item Deleted"}









