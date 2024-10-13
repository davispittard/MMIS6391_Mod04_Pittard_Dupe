from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

pets = Blueprint('pets', __name__)

@pets.route('/pet', methods=['GET', 'POST'])
def pet():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new pet
    if request.method == 'POST':
        pet_name = request.form['pet_name']
        owner_name = request.form['owner_name']
        owner_email = request.form['owner_email']

        # Insert the new pet into the database
        cursor.execute('INSERT INTO pets (pet_name, owner_name, owner_email) VALUES (%s, %s, %s)', (pet_name, owner_name, owner_email))
        db.commit()

        flash('New pet successfully added to database!', 'success')
        return redirect(url_for('pets.pet'))

    # Handle GET request to display all pets
    cursor.execute('SELECT * FROM pets')
    all_pets = cursor.fetchall()
    return render_template('pets.html', all_pets=all_pets)

@pets.route('/update_pet/<int:pet_id>', methods=['GET', 'POST'])
def update_pet(pet_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the pet's details
        pet_name = request.form['pet_name']
        owner_name = request.form['owner_name']
        owner_email = request.form['owner_email']

        cursor.execute('UPDATE pets SET pet_name = %s, owner_name = %s, owner_email = %s WHERE pet_id = %s',
                       (pet_name, owner_name, owner_email, pet_id))
        db.commit()

        flash('Pet info updated successfully!', 'success')
        return redirect(url_for('pets.pet'))

    # GET method: fetch pet's current data for pre-populating the form
    cursor.execute('SELECT * FROM pets WHERE pet_id = %s', (pet_id,))
    pet = cursor.fetchone()
    return render_template('update_pet.html', pet=pet)

@pets.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the pet
    cursor.execute('DELETE FROM pets WHERE pet_id = %s', (pet_id,))
    db.commit()

    flash('Pet info deleted successfully!', 'danger')
    return redirect(url_for('pets.pet'))