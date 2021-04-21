from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from datetime import timedelta,date
import datetime
import calendar
import json
import time



def validate(doc, method):
	if not frappe.flags.from_project_insert:
		if frappe.db.get_value("Project Task", {'subject':doc.subject}, 'name'):
			task_doc = frappe.get_doc("Project Task", {'subject':doc.subject})
			task_doc.subject = doc.subject
			task_doc.complated_by = doc.completed_by
			task_doc.caliber = doc.caliber
			task_doc.expected_start_date = doc.exp_start_date
			task_doc.expected_end_date =doc.exp_end_date
			task_doc.department = doc.department
			task_doc.color = doc.color
			task_doc.project = doc.name
			task_doc.save()


def on_trash(doc, method):
	if frappe.db.get_value("Project Task", {'subject':doc.subject}, 'name'):
		task_doc = frappe.get_doc("Project Task", {'subject':doc.subject})
		task_doc.delete()

def after_insert(doc,method):
	if not frappe.flags.from_project_insert:
		project_doc  = frappe.get_doc("Project",doc.project)
		project_doc.append('task', {"subject":doc.subject,
									"complated_by":doc.completed_by,
									"caliber":doc.caliber,
									"exp_start_date":doc.exp_start_date,
									"exp_end_date":doc.exp_end_date,
									"department":doc.department,
									"color":doc.color,
									"project":doc.project})
		project_doc.save()
