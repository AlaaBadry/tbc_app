frappe.ui.form.on("Project", {
	setup:function(frm) {
		frm.add_fetch('complated_by', 'full_name', 'caliber');
	},

	onload:function(frm) {
		frm.trigger('task_data')
	},

	task_data:function(frm) {
		frappe.call({
	        method: "cal_view_app.cal_view_app.custom_script.project.project.task_data",
	        args: {
	          project: frm.doc.name,
	        },
	        async: false,
	        callback: function(r) {
	          	if(r.message) {
	          		var task_name = []
	          		if (frm.doc.task){
	          			$.each(frm.doc.task, function(i, v) {
							task_name.push(v.subject)
						});
	          		}
	          		$.each(r.message,function(i, v){
	          			if (!task_name.includes(v.subject)){
	          				var row = frm.add_child("task");
							row.subject = v.subject;
							row.complated_by = v.completed_by
							row.caliber = v.caliber
							row.expected_start_date = v.exp_start_date
							row.expected_end_date = v.exp_end_date
							row.department = v.department
							row.color = v.color 
	          			}
		  				
		  			})
		  			frm.refresh_fields("task");
		  			frm.save()
	          	}
	        }
      	});
	}
})