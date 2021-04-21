# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = []

	if filters.get("exp_start_date") and filters.get("exp_end_date"):

		data = frappe.db.sql("""select distinct project from `tabTask`
				where exp_start_date >= '{0}' and exp_end_date <= '{1}' """.format(filters.get("exp_start_date"),filters.get("exp_end_date")),as_dict=1)
	else:
		data = frappe.db.sql("""select distinct project from `tabTask` """,as_dict=1)
	
	
	_data = []
	for p in data:
		_data.append({"project":p.get("project"),"caliber":"","total_tasks":"","completed_tasks":"","overdue_tasks":"","percent_complete":""})

		calibers = frappe.db.get_all("Task",{"project":p.get("project")},["distinct completed_by", "caliber"])
		
		for c in calibers:

			total_tasks = frappe.db.count("Task", filters={"completed_by": c['completed_by'],"project":p.get("project")}) or 0.0
			
			
			completed_task = frappe.db.count("Task", filters={"completed_by": c['completed_by'],
																			"project":p.get("project"),
																			"status":"Completed"}) or 0.0
			
			overdue_tasks =frappe.db.count("Task", filters={"completed_by": c['completed_by'],
																			"project":p.get("project"),
																			"status":"Overdue"}) or 0.0
			
			percent_complete =(completed_task / total_tasks) * 100 if completed_task and total_tasks else 0.0

			_data.append({"project":"","caliber":c['caliber'] or "Not Available",
						"total_tasks":total_tasks,
						"completed_tasks":completed_task,
						"overdue_tasks":overdue_tasks,
						"percent_complete":percent_complete})



	_data = [frappe._dict(d) for d in _data]
	return columns, _data

def get_columns():
	return [
		{
			"fieldname": "project",
			"label": _("Project"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "caliber",
			"label": _("Caliber"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "total_tasks",
			"label": _("Total Task"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "completed_tasks",
			"label": _("Tasks Completed"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "overdue_tasks",
			"label": _("Tasks Overdue"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "percent_complete",
			"label": _("Completion %"),
			"fieldtype": "Data",
			"width": 120
		}
	]

def get_chart_data(data):
	labels = []
	total = []
	completed = []
	overdue = []

	for task in data:
		
		labels.append(task.caliber)
		total.append(task.total_tasks)
		completed.append(task.completed_tasks)
		overdue.append(task.overdue_tasks)

	return {
		"data": {
			'labels': labels[:30],
			'datasets': [
				{
					"name": "Overdue",
					"values": overdue[:30]
				},
				{
					"name": "Completed",
					"values": completed[:30]
				},
				{
					"name": "Total Tasks",
					"values": total[:30]
				},
			]
		},
		"type": "bar",
		"colors": ["#fc4f51", "#78d6ff", "#7575ff"],
		"barOptions": {
			"stacked": True
		}
	}

def get_report_summary(data):
	
	if not data:
		return None

	avg_completion = sum([task.percent_complete for task in data]) / len(data)
	total = sum([task.total_tasks for task in data])
	total_overdue = sum([task.overdue_tasks for task in data])
	completed = sum([task.completed_tasks for task in data])

	return [
		{
			"value": avg_completion,
			"indicator": "Green" if avg_completion > 50 else "Red",
			"label": "Average Completion",
			"datatype": "Percent",
		},
		{
			"value": total,
			"indicator": "Blue",
			"label": "Total Tasks",
			"datatype": "Int",
		},
		{
			"value": completed,
			"indicator": "Green",
			"label": "Completed Tasks",
			"datatype": "Int",
		},
		{
			"value": total_overdue,
			"indicator": "Green" if total_overdue == 0 else "Red",
			"label": "Overdue Tasks",
			"datatype": "Int",
		}
	]
