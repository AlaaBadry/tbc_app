frappe.listview_settings['Task'] = {
 onload: function(listview) {
		listview.page.add_menu_item(__("Task Calendar View"), function() {
			window.location.href = 'desk#calendar-view-schedu'
			window.location.reload()

		})

	},
}