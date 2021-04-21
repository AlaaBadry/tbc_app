from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from datetime import timedelta,date
import datetime
import calendar
import json
import time
import copy



def get_week_dates(base_date, start_day, end_day=None):
    """
    Return entire week of dates based on given date limited by start_day and end_day.
    If end_day is None, return only start_day.

    >>> from datetime import date
    >>> get_week_dates(date(2015,1,16), 3, 5)
    [datetime.date(2015, 1, 14), datetime.date(2015, 1, 15), datetime.date(2015, 1, 16)]

    >>> get_week_dates(date(2015,1,15), 2, 5)
    [datetime.date(2015, 1, 13), datetime.date(2015, 1, 14), datetime.date(2015, 1, 15), datetime.date(2015, 1, 16)]
    """

    
    if base_date.isoweekday() == 7 :
    	""" consider sunday as staring of week """

    	base_date += timedelta(days=1)

    monday = base_date - timedelta(days=base_date.isoweekday())
    week_dates = [monday + timedelta(days=i) for i in range(7)]

    return week_dates[start_day - 1:end_day or start_day]



@frappe.whitelist()
def get_imp_link_data(filters=None):
	filters	= json.loads(filters)

	week_days = ['Sunday', 'Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday']
	week_dates = get_week_dates(date.today(), 1, 7)
	if filters.get("date"):
		filter_date = datetime.datetime.strptime(filters.get("date"), '%Y-%m-%d').date()
		week_dates = get_week_dates(filter_date, 1, 7)


	week_start_date = week_dates[0]
	week_end_date = week_dates[-1]

	data = frappe.db.sql(""" select subject,project,exp_start_date,
				exp_end_date,caliber,completed_by, color ,name
						from `tabTask` 
				where {0} and exp_start_date IS NOT NULL and exp_end_date IS NOT NULL
				and (exp_start_date >= '{1}' and exp_end_date <= '{2}')
				ORDER BY caliber ASC""".format(get_filters_codition(filters),week_start_date,week_end_date),
				as_dict=1)
	


	template_data=[]

	for d in data:
		task_spils = []
		for dt in week_dates:
			if d.get("exp_start_date") <= dt <= d.get("exp_end_date"):
				task_spils.append(calendar.day_name[dt.weekday()])


		week_day = calendar.day_name[d.get("exp_start_date").weekday()]
		
		task_cell = {"subject":d.get("subject"),
					"color":d.get('color'),
					"task_name":d.get("name")}

		
		_p_line = {d:"" for d in week_days}
		
		_p_line.update({"project":d.get("project"),
				"caliber":d.get("caliber"), 
				"caliber_user":d.get("completed_by")
				})


		for t in task_spils:
			_p_line.update({t:task_cell})

		template_data.append(_p_line)



	_template_data = []
	week_days = ['Sunday', 'Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday']
	for td in template_data:
		pc = {"project":td.get("project"),"caliber_user":td.get("caliber_user")}
		
		if not _template_data:
			_template_data.append(td)
		
		else:
			project_line_found =0
			
			for _td in _template_data:
				
				_pc = {"project":_td.get("project"),"caliber_user":_td.get("caliber_user")}
				
				blank_day = [True for w in week_days if _td.get(w)]

				if pc == _pc and any(blank_day):

					for w in week_days:
						if not _td.get(w):
							
							_td.update({w:td.get(w)})
							td.update({w:""})

							project_line_found = 1
						else:
							black_p_line_to_add = 1


			if not project_line_found or black_p_line_to_add:
				blank_day = [True for w in week_days if td.get(w)]
				if any(blank_day):
					_template_data.append(td)


	template_data = _template_data

	if not template_data and filters.get('project') and filters.get('caliber'):
		caliber = frappe.db.get_value("User", {'name':filters.get('caliber')}, 'full_name')
		template_data.append({'Sunday': '', 'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '', 'Friday': '', 'Saturday': '', 'project': filters.get('project'), 'caliber': caliber, 'caliber_user': filters.get('caliber')})


	week_dates = [w.strftime("%d/%b") for w in week_dates]
	
	path = 'cal_view_app/cal_view_app/page/calendar_view_schedu/calendar_view_schedu.html'

	html=frappe.render_template(path,{'data':{"week_days":week_dates,
											"template_data":template_data, "department":filters.get('department')}})

	return {"html":html}

def get_filters_codition(filters):
	conditions = "1=1"
	if filters.get("project"):
		conditions += " and project = '{0}'".format(filters.get('project'))
	if filters.get("status"):
		conditions += " and status = '{0}'".format(filters.get('status'))
	if filters.get("caliber"):
		conditions += " and completed_by = '{0}'".format(filters.get('caliber'))
	if filters.get("department"):
		conditions += " and department = '{0}'".format(filters.get('department'))


	return conditions

@frappe.whitelist()
def update_task_details(data, task):
	task_data=json.loads(data)

	doc = frappe.get_doc("Task", task)
	doc.subject = task_data.get('subject')
	doc.status = task_data.get('status')
	doc.exp_start_date = task_data.get('exp_start_date')
	doc.exp_end_date = task_data.get('exp_end_date')
	doc.department = task_data.get('department')
	doc.description = task_data.get('description')
	doc.color = task_data.get('color')
	doc.project = task_data.get('project')
	doc.save()

@frappe.whitelist()
def get_task_details(name):

	task_details = frappe.db.sql(""" select subject, status, exp_start_date, exp_end_date, department, description, completed_by, color	from `tabTask` where name = '{0}'""".format(name),as_dict=1)

	return task_details


@frappe.whitelist()
def create_new_task(data):
	task_data = json.loads(data)
	split_date=task_data.get('date').split("/")
	task_date = split_date[1]+"-"+split_date[0]+"-"+task_data.get('filters')[0:4]
	exp_start_date = datetime.datetime.strptime(task_date, '%b-%d-%Y')

	doc=frappe.new_doc("Task")
	doc.subject = task_data.get('subject')
	doc.project = task_data.get('project')
	doc.completed_by = task_data.get('caliber')
	doc.exp_start_date = exp_start_date
	doc.exp_end_date = exp_start_date
	doc.save()
	frappe.db.commit()

	return True



@frappe.whitelist()
def delete_task(task_name):
	frappe.db.sql("""delete from `tabTask`
			where name='{0}'""".format(task_name))
	frappe.db.commit()

	return True