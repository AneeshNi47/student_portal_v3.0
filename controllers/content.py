@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management') or auth.has_membership('Student'))
def index():
    courses = db(db.Course).select()
    specializations = db(db.Specialization).select()
    if auth.has_membership(3):
        student = db(db.Student.Student_appID == auth.user.id).select()
        student_id = student[0].id
        student_batch = student[0].Batch
        course = db(db.Batch.id == student_batch).select(db.Batch.Batch_Course)[0].Batch_Course
        specialise = db(db.Batch.id == student_batch).select(db.Batch.Batch_Specialisation)[0].Batch_Specialisation
        courseQ = db.Subjects.Subject_Course == course
        specialQ = db.Subjects.Subject_Specialization == specialise
        subjects = db(specialQ & courseQ).select()
        contents = db(db.Content_material.Batch_id == student_batch).select()
        studyMaterials = db(db.SelfStudy_material.student_id == student_id).select()
    return locals()

 
@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))       
def course_view():
    course_id= request.vars.course_id
    spcl_id = request.vars.spcl_id
    subjects = db((db.Subjects.Subject_Course ==course_id) & (db.Subjects.Subject_Specialization == spcl_id)).select()
    contents = db(db.Content_material).select()
    batches = db((db.Batch.Batch_Course == course_id) & (db.Batch.Batch_Specialisation == spcl_id)).select()
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))   
def self_study():
    course_id= request.vars.course_id
    spcl_id = request.vars.spcl_id
    subjects = db((db.Subjects.Subject_Course ==course_id) & (db.Subjects.Subject_Specialization == spcl_id)).select()
    study_materials = db((db.SelfStudy_material.Course_id == course_id) & (db.SelfStudy_material.Spcl_id== spcl_id)).select()
    batches = db((db.Batch.Batch_Course == course_id) & (db.Batch.Batch_Specialisation == spcl_id)).select()
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))       
def add_selfcontent():
    course_id= request.vars.course_id
    spcl_id = request.vars.spcl_id
    db.SelfStudy_material.insert(   Content_title=request.vars.content_title, 
                                    Course_id=request.vars.course_id,
                                    Spcl_id=request.vars.spcl_id,
                                    Subject_id=request.vars.file_sub, 
                                    student_id=request.vars.student_id,
                                    selfStudy_file=request.vars.sub_content)
    db.commit()
    db.activity_log.insert( Title_entry="Add Self Study Content", 
                            referance_id=auth.user.id,
                            remarks="Added Self Study content {}".format(request.vars.content_title))
    db.commit()
    redirect(URL('content','self_study',vars=dict(course_id= request.vars.course_id,spcl_id= request.vars.spcl_id)))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))       
def add_content():
    course_id= request.vars.course_id
    spcl_id = request.vars.spcl_id
    db.Content_material.insert( Content_title=request.vars.content_title, 
                                Subject_name=request.vars.file_sub,
                                Batch_id=request.vars.file_batch,
                                Content_file=request.vars.sub_content)
    db.commit()
    db.activity_log.insert( Title_entry="Add Content", 
                            referance_id=auth.user.id,
                            remarks="Added content {}".format(request.vars.content_title))
    db.commit()
    redirect(URL('content','course_view',vars=dict(course_id= request.vars.course_id,spcl_id= request.vars.spcl_id)))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))       
def del_selfcontent():
    course_id= request.vars.course_id
    spcl_id = request.vars.spcl_id
    content_id = request.vars.content_id
    db(db.SelfStudy_material.id == content_id).delete()
    db.activity_log.insert( Title_entry="Delete Content", 
                            referance_id=auth.user.id,
                            remarks="Deleted content {} from course".format(request.vars.content_title))
    db.commit()
    redirect(URL('content','course_view',vars=dict(course_id=course_id,spcl_id=spcl_id)))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))       
def del_content():
    course_id= request.vars.course_id
    spcl_id = request.vars.spcl_id
    content_id = request.vars.content_id
    db(db.Content_material.id == content_id).delete()
    db.activity_log.insert( Title_entry="Delete Content", 
                            referance_id=auth.user.id,
                            remarks="Deleted content {} from course".format(request.vars.content_title))
    db.commit()
    redirect(URL('content','course_view',vars=dict(course_id=course_id,spcl_id=spcl_id)))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student') or auth.has_membership('Management'))
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
    
    db.activity_log.insert( Title_entry="Download content", 
                            referance_id=auth.user.id,
                            remarks="content downloaded by {}".format(user))
    db.commit()
    return response.download(request, db)
