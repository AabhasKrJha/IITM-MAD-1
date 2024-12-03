from flask import Blueprint, jsonify, render_template_string, request

from HSA import db
from HSA.models import User

users_api = Blueprint("users", __name__, url_prefix="/users")

@users_api.route("/<int:user_id>", methods=["POST"])
def toggle_flag(user_id):
    index = request.form.get("index", type=int)
    user = User.query.get(user_id)
    user.flagged = not user.flagged
    db.session.commit()

    if user.role == "consumer":

        updated_row_html = render_template_string("""
            <div class="row align-items-center" id="consumer-row-{{ user.id }}">
                <div class="col-1 fw-bold">{{ index }}</div>
                <div class="col-3">{{ user.name }}</div>
                <div class="col-3">{{ user.email }}</div>
                <div class="col-2">{{ 'Yes' if user.flagged else 'No' }}</div>
                <div class="col-3">
                    <button class="btn btn-danger" 
                            hx-post="/api/users/{{ user.id }}" 
                            hx-vals='{"index": {{ index }}}' 
                            hx-target="#consumer-row-{{ user.id }}" 
                            hx-swap="outerHTML">
                        {{ 'Unflag' if user.flagged else 'Flag' }}
                    </button>
                </div>
            </div>
        """, user=user, index=index)
    
    else : 

        updated_row_html = render_template_string("""
            <div class="row align-items-center" id="provider-row-{{ user.id }}">
                <div class="col-1 fw-bold">{{ index }}</div>
                <div class="col-3">{{ user.name }}</div>
                <div class="col-3">{{ user.email }}</div>
                <div class="col-2">{{ user.service.name }}</div>
                <div class="col-2">{{ 'Flagged' if user.flagged else 'Not Flagged' if user.approved else 'Not Approved' }}</div>
                <div class="col-1">
                    <button class="btn btn-danger" 
                            hx-post="/api/users/{{ user.id }}" 
                            hx-vals='{"index": {{ index }}}' 
                            hx-target="#provider-row-{{ user.id }}" 
                            hx-swap="outerHTML">
                        {{ 'Unflag' if user.flagged else 'Flag' }}
                    </button>
                </div>
            </div>
        """, user=user, index=index)

    return updated_row_html


@users_api.route("/<int:user_id>/approve", methods=["POST"])
def toggle_provider_approval(user_id):
    index = request.form.get("index", type=int)
    user = User.query.get(user_id)
    user.approved = True
    db.session.commit()

    updated_row_html = render_template_string("""
        <div class="row align-items-center" id="provider-row-{{ user.id }}">
            <div class="col-1 fw-bold">{{ index }}</div>
            <div class="col-3">{{ user.name }}</div>
            <div class="col-3">{{ user.email }}</div>
            <div class="col-2">{{ user.service.name }}</div>
            <div class="col-2">{{ 'Flagged' if user.flagged else 'Not Flagged' if user.approved else 'Not Approved' }}</div>
            <div class="col-1">
                <button class="btn btn-danger" 
                        hx-post="/api/users/{{ user.id }}" 
                        hx-vals='{"index": {{ index }}}' 
                        hx-target="#provider-row-{{ user.id }}" 
                        hx-swap="outerHTML">
                    {{ 'Unflag' if user.flagged else 'Flag' }}
                </button>
            </div>
        </div>
    """, user=user, index=index)

    return updated_row_html
