# routes/main.py

import os
import json
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from database.models import db, Result, User, Recommendation
from modules.face_detector import FaceDetector
from modules.skin_extractor import SkinExtractor
from modules.skin_classifier import SkinClassifier
from modules.recommender import Recommender


main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

detector = FaceDetector()
extractor = SkinExtractor()
classifier = SkinClassifier()
recommender = Recommender()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# LANDING PAGE
@main.route('/')
def landing():
    return render_template('landing.html')


# ANALYSE PAGE (GET)
@main.route('/analyse_page')
@login_required
def analyse_page():
    return render_template('index.html', user=current_user)


# ANALYSE (POST)
@main.route('/analyse', methods=['POST'])
@login_required
def analyse():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image uploaded'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})

    if not allowed_file(file.filename):
        return jsonify({'success': False,
                        'error': 'Invalid file type. Please upload JPG or PNG'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    detection = detector.detect(filepath)
    if not detection['success']:
        return jsonify({'success': False,
                        'error': 'No face detected. Please upload a clear front-facing photo'})

    skin_data = extractor.extract_skin_colours(detection)
    if not skin_data['success']:
        return jsonify({'success': False, 'error': 'Could not extract skin colour'})

    classification = classifier.classify(skin_data)
    if not classification['success']:
        return jsonify({'success': False, 'error': 'Could not classify skin tone'})

    recommendations = recommender.recommend(classification)
    if not recommendations['success']:
        return jsonify({'success': False, 'error': 'Could not generate recommendations'})

    # Save result
    result = Result(
        user_id=current_user.id,
        skin_tone=recommendations['skin_tone'],
        undertone=recommendations['undertone'],
        undertone_description=recommendations['undertone_description'],
        hex_colour=recommendations['hex_colour'],
        image_path=filepath
    )
    db.session.add(result)
    db.session.flush()

    # Save makeup recommendations
    for subcategory, colours in recommendations['makeup'].items():
        for colour in colours:
            rec = Recommendation(
                result_id=result.id,
                category='makeup',
                subcategory=subcategory,
                colour_name=colour
            )
            db.session.add(rec)

    # Save clothing recommendations
    for colour in recommendations['clothing']:
        rec = Recommendation(
            result_id=result.id,
            category='clothing',
            subcategory=None,
            colour_name=colour
        )
        db.session.add(rec)

    # Save hair recommendations
    for colour in recommendations['hair']:
        rec = Recommendation(
            result_id=result.id,
            category='hair',
            subcategory=None,
            colour_name=colour
        )
        db.session.add(rec)

    db.session.commit()

    return jsonify({
        'success': True,
        'result_id': result.id,
        'skin_tone': recommendations['skin_tone'],
        'undertone': recommendations['undertone'],
        'undertone_description': recommendations['undertone_description'],
        'hex_colour': recommendations['hex_colour'],
        'makeup': recommendations['makeup'],
        'clothing': recommendations['clothing'],
        'hair': recommendations['hair'],
        'image_url': '/' + filepath.replace('\\', '/')
    })


# RESULTS PAGE
@main.route('/results/<int:result_id>')
@login_required
def results(result_id):
    result = Result.query.filter_by(
        id=result_id,
        user_id=current_user.id
    ).first()

    if not result:
        return redirect(url_for('main.analyse_page'))

    return render_template('results.html',
        user=current_user,
        result={
            'id': result.id,
            'skin_tone': result.skin_tone,
            'undertone': result.undertone,
            'undertone_description': result.undertone_description,
            'hex_colour': result.hex_colour,
            'makeup': result.get_makeup(),
            'clothing': result.get_clothing(),
            'hair': result.get_hair(),
            'image_path': result.image_path,
            'created_at': result.created_at.strftime('%d %b %Y, %H:%M')
        }
    )


# HISTORY
@main.route('/history')
@login_required
def history():
    all_results = Result.query.filter_by(
        user_id=current_user.id
    ).order_by(Result.created_at.desc()).all()

    parsed = []
    for r in all_results:
        parsed.append({
            'id': r.id,
            'skin_tone': r.skin_tone,
            'undertone': r.undertone,
            'hex_colour': r.hex_colour,
            'makeup': r.get_makeup(),
            'clothing': r.get_clothing(),
            'hair': r.get_hair(),
            'image_path': r.image_path,
            'created_at': r.created_at.strftime('%d %b %Y, %H:%M')
        })

    return render_template('history.html', results=parsed, user=current_user)


# PROFILE
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        if not name or not email:
            flash('Name and email are required', 'error')
            return redirect(url_for('main.profile'))

        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != current_user.id:
            flash('That email is already in use', 'error')
            return redirect(url_for('main.profile'))

        current_user.name = name
        current_user.email = email
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('main.profile'))

    total_results = Result.query.filter_by(user_id=current_user.id).count()
    latest = Result.query.filter_by(
        user_id=current_user.id
    ).order_by(Result.created_at.desc()).first()

    all_results = Result.query.filter_by(user_id=current_user.id).all()
    tone_counts = {}
    for r in all_results:
        tone_counts[r.skin_tone] = tone_counts.get(r.skin_tone, 0) + 1
    most_common_tone = max(tone_counts, key=tone_counts.get) if tone_counts else None

    return render_template('profile.html',
                           user=current_user,
                           total_results=total_results,
                           latest=latest,
                           most_common_tone=most_common_tone)


# CHANGE PASSWORD
@main.route('/profile/password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')

    if not check_password_hash(current_user.password, current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('main.profile'))

    if len(new_password) < 6:
        flash('New password must be at least 6 characters', 'error')
        return redirect(url_for('main.profile'))

    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    flash('Password updated successfully', 'success')
    return redirect(url_for('main.profile'))