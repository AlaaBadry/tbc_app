from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from datetime import timedelta,date
import datetime
import calendar
import json
import time



def validate(doc, method):
	task_name = []
	task = frappe.get_all("Task", {'project':doc.name}, "subject")

	for row in task:
		task_name.append(row.get('subject'))

	if len(doc.task) != len(task_name):
		act_list = [l.subject for l in doc.task]
		to_add = list(set(act_list) - set(task_name))
		add_task(doc, method, to_add)

	if len(doc.task) != len(task_name):
		act_list = [l.subject for l in doc.task]
		to_delete = list(set(task_name) - set(act_list))
		if to_delete:
			delete_tasks(to_delete)
	
	if doc.has_value_changed("task"):
		task_updated(doc,method)

def delete_tasks(to_delete):
	for d in to_delete:
		frappe.db.sql("""delete from `tabTask` where subject='{0}'""".format(d))
	frappe.db.commit()

def add_task(doc, method, to_add):
	for t in to_add:
		t_doc = [i for i in doc.task if i.subject == t]
		if len(t_doc):
			t_doc = t_doc[0]
			task_doc = frappe.new_doc("Task")
			task_doc.subject = t_doc.subject
			task_doc.completed_by = t_doc.complated_by
			task_doc.caliber = t_doc.caliber
			task_doc.exp_start_date = t_doc.expected_start_date
			task_doc.exp_end_date =t_doc.expected_end_date
			task_doc.department = t_doc.department
			task_doc.color = t_doc.color
			task_doc.project = doc.name
			frappe.flags.from_project_insert = 1
			task_doc.save()



@frappe.whitelist()
def task_data(project):
	task_data = frappe.db.sql("""SELECT subject, completed_by, caliber, color, exp_start_date, exp_end_date, department from `tabTask` where project ='{0}'""".format(project), as_dict=1)
	return task_data


def task_updated(doc, method):


	project_task = []
	for row in doc.task:
		project_task.append(row.subject)
		values = frappe.db.get_value("Task", {'subject':row.subject},["completed_by",
																"subject",
																"caliber",
																"exp_start_date",
																"exp_end_date","color"],as_dict=1)

		modified_dict ={}
		if row.complated_by and row.complated_by != values.get("completed_by"):
			modified_dict['completed_by'] = row.complated_by
		
		if row.caliber and row.caliber != values.get("caliber"):
			modified_dict['caliber'] = row.caliber

		if row.expected_start_date and values.get("exp_start_date") and row.expected_start_date != values.get("exp_start_date").strftime("%Y-%m-%d"):
			modified_dict['exp_start_date'] = row.expected_start_date
		
		if row.expected_start_date and not values.get("exp_start_date"):
			modified_dict['exp_start_date'] = row.expected_start_date


		if row.expected_end_date and values.get("exp_start_date") and row.expected_end_date != values.get("exp_end_date").strftime("%Y-%m-%d"):
			modified_dict['exp_end_date'] = row.expected_end_date

		if row.expected_end_date and not values.get("exp_start_date"):
			modified_dict['exp_end_date'] = row.expected_end_date


		if row.color  and row.color != values.get("color"):			
			modified_dict['color'] = row.color


		print(modified_dict,row.subject,"===")
		if modified_dict:
			frappe.db.set_value("Task", {'subject':row.subject},modified_dict)