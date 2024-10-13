from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

items = Blueprint('items', __name__)

@items.route('/item', methods=['GET', 'POST'])
def item():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new item
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_price = request.form['item_price']

        # Insert the new item into the database
        cursor.execute('INSERT INTO items (item_name, item_price) VALUES (%s, %s)', (item_name, item_price))
        db.commit()

        flash('New item successfully added to database!', 'success')
        return redirect(url_for('items.item'))

    # Handle GET request to display all items
    cursor.execute('SELECT * FROM items')
    all_items = cursor.fetchall()
    return render_template('items.html', all_items=all_items)

@items.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the item's details
        item_name = request.form['item_name']
        item_price = request.form['item_price']

        cursor.execute('UPDATE items SET item_name = %s, item_price = %s WHERE item_id = %s',
                       (item_name, item_price, item_id))
        db.commit()

        flash('Item info updated successfully!', 'success')
        return redirect(url_for('items.item'))

    # GET method: fetch item's current data for pre-populating the form
    cursor.execute('SELECT * FROM items WHERE item_id = %s', (item_id,))
    item = cursor.fetchone()
    return render_template('update_item.html', item=item)

@items.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the item
    cursor.execute('DELETE FROM items WHERE item_id = %s', (item_id,))
    db.commit()

    flash('Item info deleted successfully!', 'danger')
    return redirect(url_for('items.item'))