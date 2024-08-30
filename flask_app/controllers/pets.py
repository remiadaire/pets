from flask import request, redirect, render_template, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.pet import Pet
from datetime import datetime

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    user = User.get_by_id({'id': session['user_id']})
    pets = Pet.get_all_with_users()
    return render_template('dashboard.html', user=user, pets=pets)

@app.route('/dashboard/new')
def new_pet():
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['user_id']})
    return render_template('new_pet.html', user=user)

@app.route('/dashboard/new', methods=['POST'])
def create_pet():
    if 'user_id' not in session:
        return redirect('/')
    
    # FLASH VALIDATION NOT WORKING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>.
    
    location = request.form.get('location')
    if not location:
        flash("Location Required", "error")
        return redirect('/dashboard/new')
        
    data = {
        "count": request.form['count'],  
        "location": request.form['location'],
        "what_happened": request.form['what_happened'],
        "date_found": request.form['date'],
        "count": request.form['count'],
        "user_id": session['user_id'],
        "phone_num": request.form['phone_num'],
        # "gender": request.form.get('gender', None),
        # "animal_type": request.form.get('animal_type', None),
        # "approx_weight": request.form.get('approx_weight', None),
        # "age_range": request.form.get('age_range', None),
        # "coloring": request.form.get('coloring', None),
        # "demeanor": request.form.get('demeanor', None),
        # "unique_spots": request.form.get('unique_spots', None),
        # "missing_limb": request.form.get('missing_limb', None),
        # "noticeable_scars": request.form.get('noticeable_scars', None),
        # "solid_coloring": request.form.get('solid_coloring', None),
        # "is_fixed": request.form.get('is_fixed', None),
        # "multicolored": request.form.get('multicolored', None)
        "gender": request.form.get('gender'),
        "animal_type": request.form.get('animalType'),
        "approx_weight": request.form.get('weight'),
        "age_range": request.form.get('age'),
        "coloring": request.form.get('coloring'),
        "demeanor": request.form.get('demeanor'),
        "unique_spots": 'uniqueSpots' in request.form.getlist('keyword'),
        "missing_limb": 'missingLimb' in request.form.getlist('keyword'),
        "noticeable_scars": 'noticeableScars' in request.form.getlist('keyword'),
        "solid_coloring": 'solidColoring' in request.form.getlist('keyword'),
        "is_fixed": 'fixed' in request.form.getlist('keyword'),
        "multicolored": 'multicolored' in request.form.getlist('keyword')

    }
    pet_id = Pet.save(data)
    print (data["user_id"],  "!!!!!!!!!!!!!!!" )
    pet = Pet.get_by_id({'id': pet_id})
    user = User.get_by_id({'id': session['user_id']})
    user_for_pet = User.get_by_id({'id': pet.user_id})
    pet.creator = user_for_pet

    return render_template('view_pet.html', user=user, pet=pet)

@app.route('/pet/<int:pet_id>')
def show_pet(pet_id):
    if 'user_id' not in session:
        return redirect('/')
    
    user = User.get_by_id({'id': session['user_id']})
    pet = Pet.get_by_id({'id': pet_id})
    
    if not pet:
        return redirect('/dashboard')

    user_for_pet = User.get_by_id({'id': pet.user_id})
    pet.creator = user_for_pet

    return render_template('view_pet.html', user=user, pet=pet)

@app.route('/dashboard/<int:pet_id>/delete')
def delete_pet(pet_id):
    pet = Pet.get_by_id({'id': pet_id})
    if pet:
        Pet.delete({'id': pet_id})
    return redirect('/dashboard')


@app.route('/pet/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['user_id']})
    pet = Pet.get_by_id({'id': pet_id})

    if request.method == 'POST':
        location = request.form.get('location')
        what_happened = request.form.get('what_happened')
        date_found = request.form.get('date')
        count = request.form.get('count')
        phone_num = request.form.get('phone_num')
        gender = request.form.get('gender')
        animal_type = request.form.get('animalType')
        approx_weight = request.form.get('approx_weight')
        age_range = request.form.get('age_range')
        coloring = request.form.get('coloring')
        demeanor = request.form.get('demeanor')
        unique_spots = 'unique_spots' in request.form.getlist('keyword')
        missing_limb = 'missing_limb' in request.form.getlist('keyword')
        noticeable_scars = 'noticeable_scars' in request.form.getlist('keyword')
        solid_coloring = 'solid_coloring' in request.form.getlist('keyword')
        is_fixed = 'is_fixed' in request.form.getlist('keyword')
        multicolored = 'multicolored' in request.form.getlist('keyword')


        if not count.isdigit() or int(count) <= 0:
            flash("Please enter a valid number of pets", "error")
            return redirect(f'/pet/{pet_id}/edit')
        
        data = {
            "id": pet_id,
            "location": location,
            "what_happened": what_happened,
            "date_found": date_found,
            "count": int(count),
            "phone_num": phone_num,
            "gender": gender,
            "animal_type": animal_type,
            "approx_weight": approx_weight,
            "age_range": age_range,
            "coloring": coloring,
            "demeanor": demeanor,
            "unique_spots": unique_spots,
            "missing_limb": missing_limb,
            "noticeable_scars": noticeable_scars,
            "solid_coloring": solid_coloring,
            "is_fixed": is_fixed,
            "multicolored": multicolored,
        }

        Pet.update(data)
        
        updated_pet = Pet.get_by_id({'id': pet_id})
        user_for_pet = User.get_by_id({'id': updated_pet.user_id})
        updated_pet.creator = user_for_pet

        return render_template('view_pet.html', user=user, pet=updated_pet)

    return render_template('edit_pet.html', user=user, pet=pet)




