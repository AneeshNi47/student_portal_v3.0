@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Student') or auth.has_membership('Admin') or auth.has_membership('Management'))
def index():
    if not auth.has_membership(3):
        if auth.user.id == 1149:
            batches = db(db.Batch.Batch_Course.belongs((4,5,6,7,8))).select(orderby=db.Batch.Batch_title)
        else:
            batches = db(db.Batch).select(orderby=db.Batch.Batch_title)
        schedules = db(db.Schedule).select()
    else:
        student = db(db.Student.Student_appID == auth.user.id).select()
        batch = student[0].Batch
    return locals()
 
@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def batch_schView():
    batchID = request.vars.batch_id
    batch = db(db.Batch.id == batchID).select()
    courseID = db(db.Batch.id == batchID).select(db.Batch.Batch_Course)[0].Batch_Course
    specialID = db(db.Batch.id == batchID).select(db.Batch.Batch_Specialisation)[0].Batch_Specialisation
    courseQ = db.Subjects.Subject_Course == courseID
    speclQ = db.Subjects.Subject_Specialization == specialID
    subjects = db( courseQ & speclQ).select()
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def add_schedule():
    batchID = request.vars.sch_batch
    db.Schedule.insert( sch_type=request.vars.sche_type, 
                        Batch=request.vars.sch_batch,
                        Subject=request.vars.sch_sub,
                        class_location=request.vars.sch_location,
                        lecturer_name=request.vars.sch_lectname,
                        lect_profile=request.vars.sch_lectprofile,
                        Start_date=request.vars.start_date,
                        Remarks=request.vars.sch_remarks)
    db.commit()
    db.activity_log.insert( Title_entry="New Schedule Added",
                            referance_id=auth.user.id,
                            remarks="Adding new schedule to batch{}".format(batchID))
    db.commit()
    redirect(URL('schedule','batch_schView',vars=dict(batch_id=batchID)))
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def delete_schedule():
    batchID = request.vars.batch_id
    db(db.Schedule.id == request.vars.sch_id).delete()
    db.commit()
    db.activity_log.insert( Title_entry="Delete Schedule", 
                            referance_id=auth.user.id,
                            remarks="Delete schedule {} for batch {}".format(request.vars.sch_id,batchID))
    db.commit()
    redirect(URL('schedule','batch_schView',vars=dict(batch_id=batchID)))
    return locals()
