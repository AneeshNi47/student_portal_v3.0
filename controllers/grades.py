@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin') or auth.has_membership('Student'))
def index():
    if not auth.has_membership(3):
        locations = db(db.C_Location).select()
        courses = db(db.Course).select()
        specializations = db(db.Specialization).select()
        if auth.user.id == 1149:
            batches = db(db.Batch.id.belongs((64,76))).select()
        elif auth.user.id == 1583:
            batches = db(db.Batch.id==76).select()
        else:
            batches = db(db.Batch).select()
    elif auth.has_membership(3):
        student = db(db.Student.Student_appID == auth.user.id).select()
        batch = db(db.Batch.id == student[0].Batch).select()
        semester = db(db.Semester.Batch_id == batch[0].id).select()
        grades = db(db.Grades.Student_id == student[0].id).select()
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def student_grade():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    semesters = db(db.Semester.Batch_id == batch_id).select()
    students = db(db.Student.Batch == batch_id).select()
    batch = db(db.Batch.id == batch_id).select()
    course = batch[0].Batch_Course
    specialisation = batch[0].Batch_Specialisation
    subjects = db((db.Subjects.Subject_Specialization == specialisation) & (db.Subjects.Subject_Course == course)).select()
    grades = db(db.Grades).select()
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))#batch page student view and variables
def semester_create():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    student_id = request.vars.studID
    sem_id = db.Semester.insert(Semester_title=request.vars.sem_title,Batch_id=request.vars.batch_id)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.sem_title, referance_id=request.vars.batch_id,remarks="new semester for batch {} created {}".format(request.vars.sem_title, request.vars.batch_id))
    db.commit()
    redirect(URL('grades','semester_grade',vars=dict(batch_name=batch_name,batch_id=batch_id,semester_id=sem_id,student_id=student_id)))
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def semester_grade():
    batch_name = request.vars.batch_name
    batch_id = request.vars.batch_id
    batch_timing = request.vars.batch_timing
    sem_id = request.vars.semester_id
    student = request.vars.student_id
    student_det = db(db.Student.id == student).select()
    semester = db(db.Semester.id == sem_id).select()
    batch = db(db.Batch.id == batch_id).select()
    course = batch[0].Batch_Course
    specialisation = batch[0].Batch_Specialisation
    subjects = db((db.Subjects.Subject_Specialization == specialisation) & (db.Subjects.Subject_Course == course)).select()
    grades = db((db.Grades.Student_id == student)&(db.Grades.Semester_id == sem_id)).select()
    return locals()
    
@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def add_grade():
    batch_id = request.vars.batch_id
    sem_id = request.vars.sem_id
    student_id = request.vars.student_id
    mark = int(request.vars.smeGrade_marks)
    grade = None
    subject = db(db.Subjects.id == request.vars.grade_sub).select().first()
    if subject.Subject_Name in ["Comprehensive Exam","Module 2 - Information Technologies for Business Research"]:
        grade = DBA_special(mark)
    else:
        course = db(db.Batch.id == batch_id).select(db.Batch.Batch_Course)[0].Batch_Course
        if course not in [1,5,6]:
            grade = graderNonBBA(mark)
        else:
            grade = graderBBA(mark)
    db.Grades.insert(Student_id=student_id,
                    Semester_id=sem_id,
                    Mark=request.vars.smeGrade_marks,
                    Grade=grade,
                    Subject=request.vars.grade_sub,
                    Remarks=request.vars.smeGrade_remarks)
    db.commit()
    db.activity_log.insert( Title_entry="New Grade Added", 
                            referance_id=auth.user.id,
                            remarks="New Grade for student {}, batch {}".format(student_id, request.vars.batch_id))
    db.commit()
    redirect(URL('grades','semester_grade',vars=dict(batch_id=batch_id,semester_id=sem_id,student_id=student_id)))
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def edit_grade():
    batch_id = request.vars.batch_id
    sem_id = request.vars.sem_id
    student_id = request.vars.student_id
    mark = int(request.vars.smeGrade_marks)
    grade = None
    course = db(db.Batch.id == batch_id).select(db.Batch.Batch_Course)[0].Batch_Course
    if course not in [1,5,6]:
        grade = graderNonBBA(mark)
    else:
        grade = graderBBA(mark)
    db(db.Grades.id == request.vars.grade_id).update(Mark=request.vars.smeGrade_marks,
                                                        Grade=grade,
                                                        Remarks=request.vars.smeGrade_remarks)
    db.commit()
    db.activity_log.insert( Title_entry="Grade Edited", 
                            referance_id=auth.user.id,
                            remarks="Grade Edited for student {}, batch {}".format(student_id, request.vars.batch_id))
    db.commit()
    redirect(URL('grades','semester_grade',vars=dict(batch_id=batch_id,semester_id=sem_id,student_id=student_id)))
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def del_grade():
    batch_id = request.vars.batch_id
    sem_id = request.vars.semester_id
    student_id = request.vars.student_id
    db(db.Grades.id == request.vars.grade_id).delete()
    db.commit()
    db.activity_log.insert( Title_entry="Grade Removed", 
                            referance_id=auth.user.id,
                            remarks="Grade Removed for student {}, batch {}".format(student_id, request.vars.batch_id))
    db.commit()
    redirect(URL('grades','semester_grade',vars=dict(batch_id=batch_id,semester_id=sem_id,student_id=student_id)))
    return locals()

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def DBA_special(mark):
    if mark > 60:
        grade = "Pass"
    elif mark < 60:
        grade = "Fail"
    return grade


@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def graderBBA(mark):
    if mark >= 97:
        grade = "A+"
    elif (mark >= 93) & (mark <= 96):
        grade = "A"
    elif (mark >= 90) & (mark <= 92):
        grade = "A-"
    elif (mark >= 87) & (mark <= 89):
        grade = "B+"
    elif (mark >= 83) & (mark <= 86):
        grade = "B"
    elif (mark >= 80) & (mark <= 82):
        grade = "B-"
    elif (mark >= 77) & (mark <= 79):
        grade = "C+"
    elif (mark >= 73) & (mark <= 76):
        grade = "C"
    elif (mark >= 70) & (mark <= 72):
        grade = "C-"
    elif (mark >= 64) & (mark <= 69):
        grade = "D+"
    elif (mark >= 56) & (mark <= 63):
        grade = "D+"
    elif (mark >= 50) & (mark <= 55):
        grade = "D+"
    elif mark <= 50:
        grade = "Fail"
    return grade

@auth.requires(auth.has_membership('Examiner') or auth.has_membership('Admin'))
def graderNonBBA(mark):
    if mark >= 97:
        grade = "A+"
    elif (mark >= 93) & (mark <= 96):
        grade = "A"
    elif (mark >= 90) & (mark <= 92):
        grade = "A-"
    elif (mark >= 87) & (mark <= 89):
        grade = "B+"
    elif (mark >= 83) & (mark <= 86):
        grade = "B"
    elif (mark >= 80) & (mark <= 82):
        grade = "B-"
    elif (mark >= 77) & (mark <= 79):
        grade = "C+"
    elif (mark >= 73) & (mark <= 76):
        grade = "C"
    elif (mark >= 70) & (mark <= 72):
        grade = "C-"
    elif mark < 70:
        grade = "Fail"
    return grade
