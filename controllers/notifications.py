@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student') or auth.has_membership('Management'))
def index():
    B_notifications = db((db.Notifications.Given_to_S == None) & (db.Notifications.Given_to_ALL == None)).select()
    S_notifications = db((db.Notifications.Given_to_B == None) & (db.Notifications.Given_to_ALL == None) & (db.Notifications.Given_to_S != auth.user.id)).select()
    ALL_notifications = db((db.Notifications.Given_to_B == None) & (db.Notifications.Given_to_S == None)).select()
    recieved_notifications = db(db.Notifications.Given_to_S == auth.user.id).select()
    batches = db(db.Batch).select()
    students = db(db.Student).select()
    examiners = db(db.Examiners).select()
    managers = db(db.Managers).select()
    if auth.has_membership(3):
        student = db(db.Student.Student_appID == auth.user.id).select()
        batch = db(db.Batch.id == student[0].Batch).select()
        batchQ = db.Notifications.Given_to_B == batch[0].id
        userQ = db.Notifications.Given_to_S == auth.user.id
        givento_queryS = db.Notifications.Given_to_S == auth.user.id
        givento_queryB = db.Notifications.Given_to_B == batch[0].id
        givenby_query = db.Notifications.Given_by == auth.user.id
        notifications = db(givento_queryS | givenby_query | givento_queryB).select()
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student'))
def close_notification():
    db(db.Notifications.id == request.vars.notify_id).update(Status="Closed")
    db.commit()
    action = "closing notification {}".format(request.vars.notify_id)
    db.activity_log.insert(Title_entry=action, 
                            referance_id=auth.user.id,
                            remarks="Closed Notification")
    db.commit()
    redirect(URL('notifications','index'))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def reject_notification():
    db(db.Notifications.id == request.vars.notify_id).update(Status="Rejected")
    db.commit()
    action = "rejected Request notification {}".format(request.vars.notify_id)
    db.activity_log.insert(Title_entry=action, 
                            referance_id=auth.user.id,
                            remarks="Rejected Request")
    db.commit()
    redirect(URL('notifications','index'))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def approve_notification():
    db(db.Notifications.id == request.vars.notify_id).update(Status="Approved")
    db.commit()
    action = "Approved Request notification by {}".format(request.vars.notify_id)
    db.activity_log.insert(Title_entry=action, 
                            referance_id=auth.user.id,
                            remarks="Approved Notification")
    db.commit()
    redirect(URL('notifications','index'))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student') or auth.has_membership('Management'))
def add_notification():
    if request.vars.notify_batch != None:
        db.Notifications.insert(notif_use=request.vars.notify_type,
                                Topic=request.vars.notify_topic,
                                Message_n=request.vars.notify_remarks,
                                Given_by=auth.user.id,
                                Given_to_B=request.vars.notify_batch,
                                Given_to_ALL=None)
        db.commit()
        action = "notification to Batch {}" + format(request.vars.notify_batch)
    if request.vars.notify_student != None:
        notify_stud = db(db.Student.id == request.vars.notify_student).select().first()
        db.Notifications.insert(notif_use=request.vars.notify_type,
                                Topic=request.vars.notify_topic,
                                Message_n=request.vars.notify_remarks,
                                Given_by=auth.user.id,
                                Given_to_S=notify_stud.Student_appID,
                                Given_to_ALL=None)
        db.commit()
        action = "notification to student {}" + format(request.vars.notify_student)
    if (request.vars.notify_batch == None) & (request.vars.notify_student == None):
        new_notif = db.Notifications.insert(notif_use=request.vars.notify_type,
                                Topic=request.vars.notify_topic,
                                Message_n=request.vars.notify_remarks,
                                Given_by=auth.user.id)
        db.commit()
        action = "Notification to All {}".format(new_notif)
    db.activity_log.insert(Title_entry=action, 
                            referance_id=auth.user.id,
                            remarks="All Notification Added")
    db.commit()
    redirect(URL('notifications','index'))
    return locals()


@auth.requires(auth.has_membership('Student'))
def student_notification():
    new_notif = db.Notifications.insert(notif_use="Request",
                                Topic=request.vars.notify_topic,
                                Message_n=request.vars.notify_remarks,
                                Given_to_S=request.vars.notify_examiner,
                                Given_by=auth.user.id,
                                Given_to_ALL=None)
    db.commit()
    action = "Request from student {}".format(new_notif)
    db.activity_log.insert(Title_entry=action, 
                            referance_id=auth.user.id,
                            remarks="Request")
    db.commit()
    redirect(URL('notifications','index'))
    return locals()
