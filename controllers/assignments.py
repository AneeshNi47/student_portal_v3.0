@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student'))
def index():
    locations = db(db.C_Location).select()
    courses = db(db.Course).select()
    specializations = db(db.Specialization).select()
    if auth.user.id == 1149:
        batches = db(db.Batch.id.belongs((64,76))).select()
    elif auth.user.id == 1583:
        batches = db(db.Batch.id==76).select()
    else:
        batches = db(db.Batch).select()
    if auth.has_membership(3):
        student = db(db.Student.Student_appID == auth.user.id).select()
        batch_id = student[0].Batch
        student_query =db.Assignments.student_id == student[0].id
        batch_query = db.Assignments.Batch_id == batch_id
        assignments = db(student_query | batch_query ).select()
        submitals = db(db.Assignment_content.Student_ID == student[0].id).select()
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def batch_assignments():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    submitals = db(db.Assignment_content).select()
    Assignments = db(db.Assignments.Batch_id == request.vars.batch_id).select()
    students = db(db.Student.Batch == request.vars.batch_id).select()
    course = db(db.Batch.id == request.vars.batch_id).select(db.Batch.Batch_Course)[0].Batch_Course
    subjects = db(db.Subjects.Subject_Course == course).select()
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def add_BAassignments():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    course = db(db.Batch.id == batch_id).select(db.Batch.Batch_Course)[0].Batch_Course
    ret = db.Assignments.validate_and_insert(  Assignemnt_title=request.vars.assign_title,
                            Batch_id=batch_id,
                            course=course,
                            subject_assign=request.vars.assign_sub,
                            FinalSubmission_date=request.vars.assign_date,
                            Origianl_content=request.vars.assign_content)
    db.commit()
    if ret.errors:
        error_mark = ret.errors
    else:
        error_mark = "No Errors"
    db.activity_log.insert( Title_entry="Added Batch Assignment", 
                            referance_id=auth.user.id,
                            remarks="Batch Assignemnt added {} with {}".format(request.vars.assign_date, error_mark))
    db.commit()
    redirect(URL('assignments','batch_assignments',vars=dict(batch_name=batch_name,batch_id=batch_id)))
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))   
def add_STassignments():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    course = db(db.Batch.id == batch_id).select(db.Batch.Batch_Course)[0].Batch_Course
    ret = db.Assignments.insert(  Assignemnt_title=request.vars.assign_title,
                            student_id=request.vars.student_id,
                            course=course,
                            subject_assign=request.vars.assign_sub,
                            FinalSubmission_date=request.vars.assign_date,
                            Origianl_content=request.vars.assign_content)
    db.commit()
    if ret.errors:
        error_mark = ret.errors
    else:
        error_mark = "No Errors"
    db.activity_log.insert( Title_entry="Added Student Assignment", 
                            referance_id=auth.user.id,
                            remarks="Student Assignemnt added {} with {}".format(request.vars.assign_title, error_mark))
    db.commit()
    redirect(URL('assignments','batch_assignments',vars=dict(batch_name=batch_name,batch_id=batch_id)))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin')) 
def edit_assignment():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    assignment_old = db(db.Assignments.id == request.vars.assignId).select()
    old_date = assignment_old[0].FinalSubmission_date
    old_title = assignment_old[0].Assignemnt_title
    assign_batch = assignment_old[0].Batch_id
    ret = db(db.Assignments.id == request.vars.assignId).validate_and_update(FinalSubmission_date = request.vars.assign_date)
    if ret:
        db.Notifications.insert(    notif_use= "Announcement",
                                    Topic= "Assignment Submission date Updated",
                                    Message_n= "Submission date for {} Assignment has been updated to {}".format(old_title, request.vars.assign_date),
                                    Given_by= auth.user.id,
                                    Given_to_B= assign_batch,
                                    Given_to_ALL=None)
        db.commit()
        db.activity_log.insert( Title_entry="Edited Batch Assignment Date",
                                referance_id=auth.user.id,
                                remarks="Edited Assignment date from {} to {} ".format(old_date, request.vars.assign_date))
        db.commit()
    redirect(URL('assignments','batch_assignments',vars=dict(batch_name=batch_name,batch_id=batch_id)))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def edit_STassignment():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    assignment_old = db(db.Assignments.id == request.vars.assignId).select()
    old_date = assignment_old[0].FinalSubmission_date
    old_title = assignment_old[0].Assignemnt_title
    assign_student = assignment_old[0].student_id
    ret = db(db.Assignments.id == request.vars.assignId).validate_and_update(FinalSubmission_date = request.vars.assign_date)
    if ret:
        db.Notifications.insert(    notif_use= "Announcement",
                                    Topic= "Assignment Submission date Updated",
                                    Message_n= "Submission date for {} Assignment has been updated to {}".format(old_title, request.vars.assign_date),
                                    Given_by= auth.user.id,
                                    Given_to_S= assign_student,
                                    Given_to_ALL=None)
        db.commit()
        db.activity_log.insert( Title_entry="Edited Student Assignment Date",
                                referance_id=auth.user.id,
                                remarks="Edited Assignment date from {} to {} ".format(old_date, request.vars.assign_date))
        db.commit()
    redirect(URL('assignments','batch_assignments',vars=dict(batch_name=batch_name,batch_id=batch_id)))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student'))
def studentassignment_delete():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    db(db.Assignment_content.id == request.vars.asignID).delete()
    db.commit()
    db.activity_log.insert( Title_entry="Assignment Deleted by student",
                                referance_id=auth.user.id,
                                remarks="Reason for Delete {}: {}".format(request.vars.asignID,request.vars.reason))
    db.commit()
    redirect(URL('assignments','index'))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def delete_assignments():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    if db(db.Assignment_content.Assignemnt_title == request.vars.assing_id).select():
        db.activity_log.insert( Title_entry="Unsuccessful Delete",
                                referance_id=auth.user.id,
                                remarks="Unsuccessful deleted {} from batch {} due to Submitals".format(request.vars.assing_id,batch_id))
        db.commit()
    else:
        db(db.Assignments.id == request.vars.assing_id).delete()
        db.commit()
        db.activity_log.insert( Title_entry="Deleted Batch Assignment", 
                                referance_id=auth.user.id,
                                remarks="Batch Assignemnt deleted {} from batch {}".format(request.vars.assing_id,batch_id))
        db.commit()
    redirect(URL('assignments','batch_assignments',vars=dict(batch_name=batch_name,batch_id=batch_id)))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student'))
def submit_assignments():
    student_id = db(db.Student.Student_appID == auth.user.id).select(db.Student.id)[0].id
    ret = db.Assignment_content.validate_and_insert(Assignemnt_title=request.vars.asignID,
                                    Student_ID=student_id,
                                    Assignment_file=request.vars.assign_content)
    db.commit()
    if ret.errors:
        error_mark= ret.errors
    else:
        error_mark = "No Errors"
    db.activity_log.insert( Title_entry="Submit Assignment", 
                            referance_id=auth.user.id,
                            remarks="Assignemnt Submitted {}, with {}".format(request.vars.asignID, error_mark))
    db.commit()
    redirect(URL('assignments','index'))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student')) 
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

    db.activity_log.insert( Title_entry="Download assignment", 
                            referance_id=auth.user.id,
                            remarks="content downloaded by {}".format(user))
    db.commit()
    return response.download(request, db)
