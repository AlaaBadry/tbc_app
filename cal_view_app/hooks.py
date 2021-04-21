# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "cal_view_app"
app_title = "cal_view_app"
app_publisher = "Akshay Jadhao"
app_description = "cal_view_app"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ajadhao86@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cal_view_app/css/cal_view_app.css"
# app_include_js = "/assets/cal_view_app/js/cal_view_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/cal_view_app/css/cal_view_app.css"
# web_include_js = "/assets/cal_view_app/js/cal_view_app.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
fixtures = ['Custom Field','Property Setter','Print Format','Role','Email Template']

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
doctype_js = {"Task" : "cal_view_app/custom_script/task.js",
			"Project": "cal_view_app/custom_script/project/project.js"}

doctype_list_js = {"Task" : "public/js/task_list.js"}


doc_events = {
	"Project": {
		"validate": "cal_view_app.cal_view_app.custom_script.project.project.validate"
	},
	"Task": {
		"validate": "cal_view_app.cal_view_app.custom_script.task.task.validate",
		"on_trash": "cal_view_app.cal_view_app.custom_script.task.task.on_trash",
		"after_insert":"cal_view_app.cal_view_app.custom_script.task.task.after_insert"
	}
}


# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "cal_view_app.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cal_view_app.install.before_install"
# after_install = "cal_view_app.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cal_view_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cal_view_app.tasks.all"
# 	],
# 	"daily": [
# 		"cal_view_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"cal_view_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cal_view_app.tasks.weekly"
# 	]
# 	"monthly": [
# 		"cal_view_app.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "cal_view_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cal_view_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "cal_view_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

