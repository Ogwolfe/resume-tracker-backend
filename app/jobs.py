from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from .models import db, JobApplication
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/', methods=['GET'])
@login_required
def get_jobs():
    jobs = JobApplication.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': job.id,
        'company': job.company,
        'position': job.position,
        'resume_used': job.resume_used,
        'date_applied': job.date_applied.isoformat() if job.date_applied else None,
        'status': job.status
    } for job in jobs])

@jobs_bp.route('/', methods=['POST'])
@login_required
def create_job():
    data = request.get_json()
    try:
        job = JobApplication(
            company=data['company'],
            position=data['position'],
            resume_used=data.get('resume_used'),
            date_applied=datetime.strptime(data['date_applied'], '%Y-%m-%d').date() if data.get('date_applied') else None,
            status=data.get('status', 'applied'),
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({'message': 'Job created', 'id': job.id}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {e.args[0]}'}), 400

@jobs_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_job(id):
    job = JobApplication.query.filter_by(id=id, user_id=current_user.id).first()
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    data = request.get_json()
    for field in ['company', 'position', 'resume_used', 'date_applied', 'status']:
        if field in data:
            if field == 'date_applied' and data[field]:
                setattr(job, field, datetime.strptime(data[field], '%Y-%m-%d').date())
            else:
                setattr(job, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Job updated'})

@jobs_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_job(id):
    job = JobApplication.query.filter_by(id=id, user_id=current_user.id).first()
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'}) 