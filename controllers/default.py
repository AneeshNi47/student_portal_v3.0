# -*- coding: utf-8 -*-
from datetime import date
today = date.today()

def index():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    message = " "
    def invalid_login():
        table_user = auth.table_user()
        username = auth.settings.login_userfield or 'username' if 'username' in table_user.fields else 'email'

        if username in request.vars:
            entered_username = request.vars[username]
            if auth.settings.multi_login and '@' in entered_username:
                # if '@' in username check for email, not username
                user = table_user(email = entered_username)
            else:
                user = table_user(**{username: entered_username})

            if user:
                # If the user exists then the password must be invalid
                return auth.messages.invalid_password
            return auth.messages.invalid_user
        else:
            return " "
    
    auth.settings.login_onaccept = log_entry
    auth.messages.invalid_login = invalid_login()
    auth.settings.login_next = URL('default','home')
    return dict(form=auth(),message = auth.messages.invalid_login)


def log_entry(form):
    db.activity_log.insert(Title_entry="Login By User",
                            referance_id=auth.user.id,
                            remarks="Login")
    db.commit()
    print("hello")


@auth.requires_login() #home page view elements and variables
def home():
    locations = db(db.C_Location).select()
    if auth.user.id == 1149 or auth.user.id == 1583:
        courses = db(db.Course.id.belongs((4,5,6,7,8))).select()
        batches = db(db.Batch.id.belongs((64,76))).select()
    else:
        batches = db(db.Batch).select()
        courses = db(db.Course).select()
    specialisations = db(db.Specialization).select()
    if auth.has_membership(4) or auth.has_membership(3):
        student = db(db.Student.Student_appID == auth.user.id).select()
        semester = db(db.Semester.Batch_id == student[0].Batch).select().first()
        course_name = db(db.Batch.id == student[0].Batch).select()
        course = db(db.Batch.id == student[0].Batch).select(db.Batch.Batch_Course)[0].Batch_Course
        spcl = db(db.Batch.id == student[0].Batch).select(db.Batch.Batch_Specialisation)[0].Batch_Specialisation
        student_query = db.Grades.Student_id == student[0].id
        
        if semester:
            semester_query = db.Grades.Semester_id == semester.id
            Completed_subjects = db((student_query & semester_query) & (db.Grades.Grade != "Fail")).count()
            if course_name[0].Batch_Course == 6:
                MOAR_list = ['Module 1 - Management Research Perspective',
                            'Module 2 - Information Technologies for Business Research',
                            'Module 3 - Global Environments and Management Trends',
                            'Module 4 - Critique Analysis of Research',
                            'Module 5 - Contemporary Management',
                            'Module 6 -Research Methods in Business & Management',
                            'Module 7 - Management Research Design & Methodologies',
                            'Module 8 - Preparation and Presentation of a Research Proposal',
                            'Comprehensive Exam']
                flag = False
                count = 0
                grades_subs = db((student_query & semester_query) & (db.Grades.Grade != "Fail")).select()
                for grades_sub in grades_subs:
                    if db(db.Subjects.id == grades_sub.Subject).select(db.Subjects.Subject_Name)[0].Subject_Name not in MOAR_list:
                        count = count + 1
                MOAR_degree_application = db(db.MOARDegree_file.student_id == auth.user.id).select()
        else:
            Completed_subjects = 0

        if (course_name[0].Batch_Course != 3) and (course_name[0].Batch_Course != 4):
            Total_subjects = 12 #<!--Students not in CEO & BBA3Y will have 12 subjectss-->
        else:
            Total_subjects = db((db.Subjects.Subject_Course == course) & (db.Subjects.Subject_Specialization == spcl)).count()
        degree_application = db(db.Degree_file.student_id == auth.user.id).select()
    return locals()
 

@auth.requires_login() #home page view elements and variables
def add_degree():
    ret = db.Degree_file.validate_and_insert(  student_id=request.vars.student_id,
                            batch_id=request.vars.batch_id,
                            status="Documents Submitted",
                            PC_agreement=request.vars.pcdoc,
                            Graduation_form=request.vars.graddoc,
                            Docs_date=today)
    db.commit()
    db.Notifications.insert(    notif_use="Request",
                                Topic="Degree application",
                                Message_n="Documents have been uploaded",
                                Given_by=auth.user.id,
                                Given_to_S=4,)
    db.commit()
    if ret.errors:
        error_mark = ret.errors
    else:
        error_mark = "No Errors"
    db.activity_log.insert(Title_entry="Degree Request",
                            referance_id=auth.user.id,
                            remarks="Verification requested with {}".format(error_mark))
    db.commit()
    redirect(URL('default','home'))
    return response.json({'status':'success'})
 

@auth.requires_login() #home page view elements and variables
def add_MOARDdegree():
    ret = db.MOARDegree_file.validate_and_insert(  student_id=request.vars.student_id,
                            batch_id=request.vars.batch_id,
                            status="Documents Submitted",
                            PC_agreement=request.vars.pcdoc,
                            Graduation_form=request.vars.graddoc,
                            Docs_date=today)
    db.commit()
    db.Notifications.insert(    notif_use="Request",
                                Topic="MOAR Degree application",
                                Message_n="MOAR Documents have been uploaded",
                                Given_by=auth.user.id,
                                Given_to_S=4,)
    db.commit()
    if ret.errors:
        error_mark = ret.errors
    else:
        error_mark = "No Errors"
    db.activity_log.insert(Title_entry="MOAR Degree Request",
                            referance_id=auth.user.id,
                            remarks="Verification requested with {}".format(error_mark))
    db.commit()
    redirect(URL('default','home'))
    return response.json({'status':'success'})


@auth.requires_login() #home page view elements and variables
def reapply_MOARDdegree():
    ret = db(db.MOARDegree_file.id == request.vars.degreeId).validate_and_update(   student_id=request.vars.student_id,
                                                                                batch_id=request.vars.batch_id,
                                                                                status="Documents Submitted",
                                                                                PC_agreement=request.vars.pcdoc,
                                                                                Graduation_form=request.vars.graddoc,
                                                                                Docs_date=today)
    db.commit()
    db.Notifications.insert(    notif_use="Request",
                                Topic="MOAR Degree Re-application",
                                Message_n="MOAR Documents have been uploaded",
                                Given_by=auth.user.id,
                                Given_to_S=4,)
    db.commit()
    db.activity_log.insert(Title_entry="MOAR Degree ReApply", 
                            referance_id=auth.user.id,
                            remarks="verification requested")
    db.commit()
    redirect(URL('default','home'))
    return response.json({'status':'success'})

@auth.requires_login() #home page view elements and variables
def reapply_degree():
    ret = db(db.Degree_file.id == request.vars.degreeId).validate_and_update(   student_id=request.vars.student_id,
                                                                                batch_id=request.vars.batch_id,
                                                                                status="Documents Submitted",
                                                                                PC_agreement=request.vars.pcdoc,
                                                                                Graduation_form=request.vars.graddoc,
                                                                                Docs_date=today)
    db.commit()
    db.Notifications.insert(    notif_use="Request",
                                Topic="Degree Re-application",
                                Message_n="Documents have been uploaded",
                                Given_by=auth.user.id,
                                Given_to_S=4,)
    db.commit()
    db.activity_log.insert(Title_entry="Degree ReApply", 
                            referance_id=auth.user.id,
                            remarks="verification requested")
    db.commit()
    redirect(URL('default','home'))
    return response.json({'status':'success'})


@auth.requires_login() #home page view elements and variables
def add_image():
    ret = db(db.Student.Student_appID == auth.user.id).validate_and_update(icon_image=request.vars.prof_image)
    db.commit()
    db.activity_log.insert(Title_entry="Image Added", 
                            referance_id=auth.user.id,
                            remarks="New Profile image added")
    db.commit()
    redirect(URL('default','home'))
    return response.json(ret)


@auth.requires_login() #home page view elements and variables
def request_verify():
    db.Notifications.insert(notif_use="Request",
                                Topic="Verification",
                                Message_n="Account verification Request",
                                Given_by=auth.user.id,
                                Given_to_S=4,)
    db.commit()
    db.activity_log.insert(Title_entry="To admin Request", 
                            referance_id=auth.user.id,
                            remarks="verification requested")
    db.commit()
    redirect(URL('default','home'))
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))
def batch_elements():
    locations = db(db.C_Location).select()
    courses = db(db.Course).select()
    specializations = db(db.Specialization).select()
    if auth.user.id == 1149:
        batches = db(db.Batch.id.belongs((64,76))).select()
    elif auth.user.id == 1583:
        batches = db(db.Batch.id==76).select()
    else:
        batches = db(db.Batch).select()
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))# batch page subject view and variables
def subbatch_view():
    batch_id = request.vars.batch_id
    batch_name = request.vars.batch_name
    course = db(db.Batch.id == request.vars.batch_id).select(db.Batch.Batch_Course)[0].Batch_Course
    specialisation = db(db.Batch.id == request.vars.batch_id).select(db.Batch.Batch_Specialisation)[0].Batch_Specialisation
    subjects = db((db.Subjects.Subject_Course == course) & (db.Subjects.Subject_Specialization == specialisation)).select()
    return locals()


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management'))#modal from subbatch_view to add subject to batch
def add_fromsubject():
    db.Subjects.insert(Subject_Name=request.vars.subject,Subject_Course=request.vars.sub_course,Subject_Specialization=request.vars.sub_specialise)
    db.commit()
    new_id = db(db.Subjects.Subject_Name == request.vars.subject).select(db.Subjects.id)[0].id
    db.activity_log.insert(Title_entry=request.vars.subject, referance_id=new_id,remarks="adding new subject")
    db.commit()
    redirect(URL('default','subbatch_view',vars=dict(batch_name=request.vars.sub_batchname,batch_id=request.vars.sub_batchid)))
    return locals()


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin') or auth.has_membership('Management'))# del action for subject from subbatch_view
def del_subject():
    batch_id = request.vars.batchid
    batch_name = request.vars.batchname
    db(db.Subjects.id == request.vars.subject_id).delete()
    db.activity_log.insert(Title_entry=request.vars.batch_id, referance_id=request.vars.subject_id,remarks="delete subject from subbatch view")
    db.commit()
    redirect(URL('default','subbatch_view',vars=dict(batch_name=request.vars.batchname,batch_id=request.vars.batchid)))
    return locals()

@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))# edit action for subject from subbatch_view
def edit_subject():
    batch_id = request.vars.batchid
    batch_name = request.vars.batchname
    old_name = db(db.Subjects.id == request.vars.subjectId).select(db.Subjects.Subject_Name)[0].Subject_Name
    db(db.Subjects.id == request.vars.subjectId).update(Subject_Name=request.vars.new_sub)
    db.commit()
    db.activity_log.insert(
                            Title_entry=request.vars.new_sub, 
                            referance_id=auth.user.id,
                            remarks="Subject Name changed from {} to {}".format(old_name, request.vars.new_sub))
    db.commit()
    redirect(URL('default','subbatch_view',vars=dict(batch_name=request.vars.batchname,batch_id=request.vars.batchid)))
    return locals()
 
@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Management') ) #batch page student view and variables
def batch_view():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    batch_timing = request.vars.batch_timing
    students = db(db.Student.Batch == batch_id).select()
    new_students = db((db.Student.is_active == True) & (db.Student.Batch == None)).select()
    return locals()


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def student_to_batch():  #modal from batch_view to add students to batch
    set_fields = db(db.Batch.id == request.vars.batch_id).select()
    student = db(db.Student.id == request.vars.new_student).select().first()
    ret = db(db.Student.id == request.vars.new_student).validate_and_update(Batch=request.vars.batch_id)
    db.commit()
    db.activity_log.insert( Title_entry="Add Student to Batch", 
                            referance_id=auth.user.id ,
                            remarks="Adding {} to Batch {}".format(request.vars.new_student,request.vars.batch_id))
    db.commit()
    student_count = db(db.Student.Batch == request.vars.batch_id).count()
    db(db.Batch.id == request.vars.batch_id).validate_and_update(Students_no=student_count)
    db.commit()
    redirect(URL('default','batch_view',vars=dict(batch_name=set_fields[0].Batch_title,batch_id=set_fields[0].id)))
    return response.json(ret)

@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin')) #fuction to block access to students
def blocked_login():
    ret = db(db.auth_user.id == request.vars.block_id).update(registration_key=request.vars.block_status)
    db.commit()
    if request.vars.block_status == "blocked":
        status = "blocked"
    elif request.vars.block_status == "":
        status = "Unblocked"
    db.activity_log.insert( Title_entry="Blocked Student Login", 
                            referance_id=auth.user.id ,
                            remarks="{} Login to {}".format(status, request.vars.block_id))
    db.commit()
    return response.json(ret)

@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin')) #fuction to verify documents
def verify_docs():
    ret = db(db.Student.id == request.vars.verify_id).validate_and_update(Status="verified")
    db.commit()
    user_id = db(db.Student.id == request.vars.verify_id).select(db.Student.Student_appID)[0].Student_appID
    db(db.auth_membership.user_id == user_id).validate_and_update(group_id=3)
    db.commit()
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))#batch page student view and variables
def remove_STbatch():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    batch_timing = request.vars.batch_timing
    ret = db(db.Student.id == request.vars.student_id).validate_and_update(Batch=None)
    db.commit()
    db.activity_log.insert( Title_entry="Remove Student From Batch", 
                            referance_id=auth.user.id,
                            remarks="Removed {} from {},{}".format(request.vars.student_id,batch_name,batch_id))
    db.commit()
    redirect(URL('default','batch_view',vars=dict(batch_name=batch_name,batch_id=batch_id,batch_timing=batch_timing)))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def add_course():  #modal from batch elements to add course
    course_id = course_id = db.Course.insert(Course_Name=request.vars.course)
    db.commit()
    db.activity_log.insert( Title_entry="New course Added", 
                            referance_id=auth.user.id,
                            remarks="New course {}, {}".format(request.vars.course,course_id))
    db.commit()
    redirect(URL('default','batch_elements'))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def add_location():#modal from batch elements to add location
    location_id = db.C_Location.insert(location_Name=request.vars.location)
    db.commit()
    db.activity_log.insert( Title_entry="New Location added", 
                            referance_id=auth.user.id,
                            remarks="New Location {}, {}".format(request.vars.location, location_id))
    db.commit()
    redirect(URL('default','batch_elements'))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def add_specialization(): #modal from elements to add specialisation
    special_id = db.Specialization.insert(specialization_Name=request.vars.specialise)
    db.commit()
    db.activity_log.insert( Title_entry="New Specilisation Added", 
                            referance_id=auth.user.id,
                            remarks="New Specialization {}, {}".format(request.vars.specialise, special_id))
    db.commit()
    redirect(URL('default','batch_elements'))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def add_batch():#modal from elements to add batch
    batch_id = db.Batch.insert(
                    Batch_title=request.vars.batch_title, 
                    Batch_Location=request.vars.location, 
                    Batch_type=request.vars.duration, 
                    Batch_Course=request.vars.course, 
                    Batch_Specialisation=request.vars.specialise, 
                    Students_no=0)
    db.commit()
    db.activity_log.insert( Title_entry="New Batch Added", 
                            referance_id=auth.user.id,
                            remarks="New Batch {}, {}".format(request.vars.batch_title, batch_id))
    db.commit()
    redirect(URL('default','batch_elements'))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))#edit batch title 
def edit_batch():
    batch_id = request.vars.batchId
    ret = db(db.Batch.id == batch_id ).validate_and_update(Batch_title=request.vars.batch_title)
    db.commit()
    db.activity_log.insert( Title_entry=request.vars.batch_title, 
                            referance_id=auth.user.id,
                            remarks="Batch title changed {}, {}".format(request.vars.batch_title,batch_id))
    db.commit()
    redirect(URL('default','batch_elements'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))#remove batch from student batch and delete batch 
def del_batch():
    batch_id = request.vars.batch_id
    db(db.Batch.id == batch_id).delete()
    db.activity_log.insert( Title_entry="Batch Deleted",
                            referance_id=request.vars.batch_id,
                            remarks="Batch Removed {}, {}".format(request.vars.batch_title,batch_id))
    db.commit()
    return response.json({'status':'success'})


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    db.auth_user.username.writable = False
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
