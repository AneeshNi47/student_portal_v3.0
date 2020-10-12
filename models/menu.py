# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'home'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if auth.has_membership('Admin'):
    	response.menu += (
            (T('Batch Elements'), False, URL('default', 'batch_elements'), []),
            (T('Students'), False, URL( 'student','index'), []),
            (T('Content'), False, URL('content','index'), []),
            (T('Assignments'), False, URL('assignments', 'index'), []),
            (T('Notifications'), False, URL('notifications','index'), []),
            (T('Grades'), False, URL('grades','index'), []),
            (T('Schedule'), False, URL('schedule','index'), []),
            (T('Settings'), False, URL('settings','index'), []),
            (T('Degree'), False, URL('degree','index'), [])
        )


if auth.has_membership('Examiner'):
        if auth.user.id == 1149 or auth.user.id == 1583:
            response.menu += (
                (T('Batch Elements'), False, URL('default', 'batch_elements'), []),
                (T('Assignments'), False, URL('assignments', 'index'), []),
                (T('Grades'), False, URL('grades','index'), []),)
        else:
            response.menu += (
                (T('Batch Elements'), False, URL('default', 'batch_elements'), []),
                (T('Content'), False, URL('content','index'), []),
                (T('Assignments'), False, URL('assignments', 'index'), []),
                (T('Notifications'), False, URL('notifications','index'), []),
                (T('Grades'), False, URL('grades','index'), []),
                (T('Schedule'), False, URL('schedule','index'), []),
                (T('Degree'), False, URL('degree','index'), [])
            )

if auth.has_membership('Management'):
    	response.menu += (
            (T('Batch Elements'), False, URL('default', 'batch_elements'), []),
            (T('Students'), False, URL( 'student','index'), []),
            (T('Content'), False, URL('content', 'index'), []),
            (T('Notifications'), False, URL('notifications','index'), []),
            (T('Schedule'), False, URL('schedule','index'), []),
            (T('Degree'), False, URL('degree','index'), [])
        )

if auth.has_membership('Student'):
    	response.menu += (
            (T('Content'), False, URL('content', 'index'), []),
            (T('Assignments'), False, URL('assignments', 'index'), []),
            (T('Notifications'), False, URL('notifications','index'), []),
            (T('Grades'), False, URL('grades','index'), []),
            (T('Schedule'), False, URL('schedule','index'), [])
        )
