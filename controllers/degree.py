@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management')) 
def index():
    query = request.vars.query
    if query:
        degree_stats = db(db.Degree_file.status == query).select()
    else:
        degree_stats = db(db.Degree_file).select()
    return locals()

from datetime import date
today = date.today()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin')) 
def docs_rejected():
    student_id = request.vars.student_id
    ret = db(db.Degree_file.id == request.vars.degree_id).validate_and_update(  status="Documents Rejected",
                                                                                Docs_date= today)
    db.commit()
    db.Notifications.insert(    notif_use="Notice",
                                Topic="Documents Rejected",
                                Message_n="Your Documents have been Rejected".format(today),
                                Given_by=auth.user.id,
                                Given_to_S=student_id,
                                Given_to_ALL=None)
    db.commit()
    db.activity_log.insert(Title_entry="Documents Rejected", 
                            referance_id=auth.user.id,
                            remarks="Documents Rejected for {}".format(student_id))
    db.commit()
    return response.json(ret)


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management')) 
def degree_applied():
    student_id = request.vars.student_id
    ret = db(db.Degree_file.id == request.vars.degree_id).validate_and_update(  status="Applied",
                                                                                applied_date= today)
    db.commit()
    db.Notifications.insert(    notif_use="Notice",
                                Topic="Degree applied",
                                Message_n="Your Degree has been Applied on {}".format(today),
                                Given_by=auth.user.id,
                                Given_to_S=student_id,
                                Given_to_ALL=None)
    db.commit()
    db.activity_log.insert(Title_entry="Degree Applied", 
                            referance_id=auth.user.id,
                            remarks="Degree Applied for {}".format(student_id))
    db.commit()
    return response.json(ret)


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management')) 
def degree_recived():
    student_id = request.vars.student_id
    ret = db(db.Degree_file.id == request.vars.degree_id).validate_and_update(  status="Recieved",
                                                                                applied_date= today)
    db.commit()
    db.Notifications.insert(    notif_use="Notice",
                                Topic="Degree Recieved",
                                Message_n="Your Degree has been recieved on {}".format(today),
                                Given_by=auth.user.id,
                                Given_to_S=student_id,
                                Given_to_ALL=None)
    db.commit()
    db.activity_log.insert(Title_entry="Degree Recieved", 
                            referance_id=auth.user.id,
                            remarks="Degree Recieved for {}".format(student_id) )
    db.commit()
    return response.json(ret)

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management')) 
def degree_Collected():
    student_id = request.vars.student_id
    ret = db(db.Degree_file.id == request.vars.degree_id).validate_and_update(  status="Collected",
                                                                                applied_date= today)
    db.commit()
    db.Notifications.insert(    notif_use="Notice",
                                Topic="Degree Collected",
                                Message_n="Your Degree has been collected on {}".format(today),
                                Given_by=auth.user.id,
                                Given_to_S=student_id,
                                Given_to_ALL=None)
    db.commit()
    db.activity_log.insert(Title_entry="Degree Collected", 
                            referance_id=auth.user.id,
                            remarks="Degree Collected for {}".format(student_id))
    db.commit()
    return response.json(ret)

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def del_degree():
    student_id = db(db.Degree_file.id == request.vars.degree_id).select(db.db.Degree_file.student_id)[0].student_id
    ret = db(db.Degree_file.id == request.vars.degree_id).delete()
    db.commit()
    db.activity_log.insert(Title_entry="Degree Deleted",
                            referance_id=auth.user.id,
                            remarks="Degree  for {}".format(student_id))
    db.commit()
    return response.json(ret)

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    if auth.has_membership(1):
        user = "Admin"
    elif auth.has_membership(2):
        user = "Examiner"
    elif auth.has_membership(3):
        user = "student"
    elif auth.has_membership(5):
        user = "Managment"
    
    db.activity_log.insert( Title_entry="Degree Doc downloaded", 
                            referance_id=auth.user.id,
                            remarks="content downloaded by {}".format(user))
    db.commit()
    return response.download(request, db)
