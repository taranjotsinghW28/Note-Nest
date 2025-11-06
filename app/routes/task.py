from flask import render_template, redirect, url_for, flash, request, Blueprint
from app.models import User, Note, Tag, db
from flask_login import login_required, current_user

note_bp = Blueprint("note", __name__)

@note_bp.route("/")
@login_required
def home():
    # Show only current user's notes
    notes = Note.query.filter_by(author=current_user).all()
    return render_template("home.html", notes=notes)


@note_bp.route("/add_note", methods=["GET", "POST"])
@login_required
def add_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        new_note = Note(note_title=title, note_content=content, author=current_user)
        db.session.add(new_note)
        db.session.commit()

        flash("Note successfully added!")
        return redirect(url_for("note.home"))

    return render_template("add_note.html")


@note_bp.route("/add_tag/<int:note_id>", methods=["POST"])
@login_required
def add_tag(note_id):
    note = Note.query.get_or_404(note_id)
    name = request.form.get("tag_name")

    tag = Tag.query.filter_by(tag_name=name).first()
    if not tag:
        tag = Tag(tag_name=name)
        db.session.add(tag)

    note.tags.append(tag)
    db.session.commit()

    flash("Tag added successfully!")
    return redirect(url_for("note.home"))


@note_bp.route("/delete_note/<int:note_id>")
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        flash("You cannot delete this note!")
        return redirect(url_for("note.home"))

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted successfully!")
    return redirect(url_for("note.home"))


@note_bp.route("/update_note/<int:note_id>", methods=["GET", "POST"])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.author != current_user:
        flash("You cannot update this note!")
        return redirect(url_for("note.home"))

    if request.method == "POST":
        note.note_title = request.form.get("title")
        note.note_content = request.form.get("content")
        db.session.commit()
        flash("Note updated successfully!")
        return redirect(url_for("note.home"))

    return render_template("update_note.html", note=note)


@note_bp.route("/delete_tag/<int:note_id>/<int:tag_id>")
@login_required
def delete_tag(note_id, tag_id):
    note = Note.query.get_or_404(note_id)
    tag = Tag.query.get_or_404(tag_id)

    if tag in note.tags:
        note.tags.remove(tag)
        db.session.commit()
        flash("Tag removed successfully!")
    else:
        flash("Tag not found on this note!")

    return redirect(url_for("note.home"))
