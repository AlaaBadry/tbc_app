frappe.ui.form.on("Task", {
	onload:function(frm){
		frm.page.add_menu_item(__("Task Calendar View"), function() {
            window.location.href = 'desk#calendar-view-schedu'
			window.location.reload()
        });
	}
})