
{% include "cal_view_app/cal_view_app/page/calendar_view_schedu/jquery.stickytable.js" %}


frappe.pages["calendar-view-schedu"].on_page_load = function (wrapper) {
	frappe.important_links = new frappe.ImpLinks(wrapper);
}


frappe.ImpLinks= Class.extend({

	init: function (wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: "Calendar View Schedule",
			single_column: true
		});
		this.wrapper = wrapper
		this.filters = {}
		this.make()
		this.get_imp_link_data()
    this.add_filters()
    $('[data-fieldname="new_task"]').css({"background-color":"#00b8ff"});
    this.add_menu_buttons()



	},

	make: function() {
		var me = this;
    $(`<div class="frappe-list list-container" > </div>`).appendTo(me.page.main);
	},

	get_imp_link_data:function(){
    var me = this
    
    $('.frappe-list').html("")

    var filters = {"project":me.project,"status":me.status,"date":me.date,"caliber":me.caliber, "department":me.department}
    frappe.call({
        "method": "cal_view_app.cal_view_app.page.calendar_view_schedu.calendar_view_schedu.get_imp_link_data",
        args: {
            filters: filters,
          },
        callback: function (r) {
          var html = r.message.html

          $('.frappe-list').html(html)
          me.bind_events(me)
          me.edit_task(me)
          me.delete_task(me)
          

        }//calback end
      })
	},

  add_filters:function(){
      var me = this
      user = frappe.session.user;
     
    
        me.page.add_field({
          fieldtype: 'Link',
          label: __('Project'),
          fieldname: 'project',
          options: "Project",
          onchange: function() {
            me.project = this.value?this.value:null
            me.get_imp_link_data()
          }
        })
      me.page.add_field({
          fieldtype: 'Select',
          label: __('Status'),
          fieldname: 'status',
          options: ["","Open","Working","Pending Review","Overdue","Completed","Cancelled"],
          default:"",
          onchange: function() {
            me.status = this.value?this.value:null
            me.get_imp_link_data()
          }
        })

      me.page.add_field({
          fieldtype: 'Link',
          label: __('Caliber'),
          fieldname: 'caliber',
          options: "User",
          onchange: function() {
            me.caliber = this.value?this.value:null
            me.get_imp_link_data()
          }
        })
      const today = frappe.datetime.get_today();
      me.page.add_field({
          fieldtype: 'Date',
          label: __('Date'),
          fieldname: 'date',
          default:today,
          reqd:1,
          onchange: function() {
            me.date = this.value?this.value:null
            me.get_imp_link_data()

          }
        })
       
          me.page.add_field({
          fieldtype: 'Link',
          label: __('Department'),
          fieldname: 'department',
          options:"Department",
          default:me.get_dep_default(),
          onchange:function() {
            me.department = this.value?this.value:null
            me.get_imp_link_data()
          }
        })

      me.page.add_field({
          fieldtype: 'Select',
          label: __('Assign Task'),
          fieldname: 'assign_task',
          options:["Assign Task", "Edit Task","Delete Task"],
          default: "Assign Task",
          onchange:function() {
            me.assign_task = this.value?this.value:null
          }

        })

      // me.page.add_field({
      //     fieldtype: 'Button',
      //     label: __('New Task'),
      //     fieldname: 'new_task',
      //     click:function() {
      //       console.log("qqq")
      //       me.new_task(me)
      //     }

      //   })

  },
  get_dep_default:function(){

    var department = ''
    frappe.call({
        method: "frappe.client.get_value",
        args: {
          doctype: "Employee",
          fieldname: "department",
          filters: { user_id: frappe.session.user },
        },
        async: false,
        callback: function(r) {
          if(r.message) {
            department = r.message.department
            
          }
        }
      });

    return department
  },
  add_menu_buttons:function(){
    me = this
    me.page.show_menu()

    me.page.add_menu_item(__("Refresh"), function() {
        me.get_imp_link_data()
    }, true)
    
    // me.page.add_menu_item(__("New Task"), function() {
    //     var new_doc = frappe.model.get_new_doc("Task");
    //     frappe.ui.form.make_quick_entry("Task", null, null, new_doc);
    // }, true)

    me.page.add_menu_item(__("Task List"), function() {
        window.location.href = 'desk#List/Task/List'
    }, true)

  },
  bind_events:function(me){
    var me = this;
    $('.assign_task').click(function() {
      // var phase = $(this).attr('data-phase')
      var assign_task = frappe.pages['calendar-view-schedu'].page.fields_dict.assign_task.get_value()

      var exceptional_msg = "{{ no such element: str object['task_name'] }}"
      
      var task_name = $(this).attr("task_name")
      var caliber_user = $(this).attr("caliber_user")

      if ((assign_task=="Assign Task") && (task_name) && (task_name != exceptional_msg) ){  
                      
              const assign_to = new frappe.ui.form.AssignToDialog({
                obj: this,
                method: 'frappe.desk.form.assign_to.add',
                doctype: "Task",
                docname: task_name,

              });

              assign_to.dialog.clear();
              assign_to.dialog.show();
              assign_to.dialog.set_value("assign_to",[caliber_user])
      }
      
      
    })




    $( ".dbclick" ).dblclick(function() {

      $(this).attr("contenteditable", "true");

      $('[contenteditable=true]').focus(function() {
              $(this).data("initialText", $(this).html());
          }).blur(function() {
              
              if ($(this).data("initialText") !== $(this).html()) {
                
                  var caliber = $(this).attr("caliber_user");
                  var project = $(this).closest('tr').find('td:first').text()
                  var col_index = $(this).index();
                  var col_index = col_index -1
                  var subject = $(this).html()
                  var date = $($("#main_tbl > thead > tr")[2]).find('th:eq('+col_index+')').text()

                  frappe.call({
                    method: "cal_view_app.cal_view_app.page.calendar_view_schedu.calendar_view_schedu.create_new_task",
                    args: {data:{
                      caliber: caliber,
                      project: project,
                      date: date,
                      filters: me.date,
                      subject: subject},
                    },
                    callback: function(r) {
                      if(r.message) {
                        // me.get_imp_link_data()
                      } 
                    }
                  });            

              }
            $(this).attr("contenteditable", "false");
          });
    });

  },


  edit_task: function(me){
    $('.assign_task').click(function() {
      var task_name = $(this).attr("task_name")

      var project = $(this).closest('tr').find('td:first').text()
      var exceptional_msg = "{{ no such element: str object['task_name'] }}"
      var assign_task = frappe.pages['calendar-view-schedu'].page.fields_dict.assign_task.get_value()
      if ((assign_task == "Edit Task") && (task_name) && ( task_name !=exceptional_msg)){
        var d = new frappe.ui.Dialog({
          title: __(task_name),
          fields: [
            {
              "label": "Subject",
              "fieldname": "subject",
              "fieldtype": "Data",

            },
            {
              "label": "Project",
              "fieldname": "project",
              "fieldtype": "Link",
              "options":"Project",
              "default":project


            },
            {
              "label": "Expected Start Date",
              "fieldname": "exp_start_date",
              "fieldtype": "Date",
            },
            {
              "label": "Department",
              "fieldname": "department",
              "fieldtype": "Link",
              "options":"Department"
            },
            
            {"fieldtype":"Column Break"},
            {
              "label": "Status",
              "fieldname": "status",
              "fieldtype": "Select",
              "default":"Open",
              "options":["Open",'Working','Pending Review','Overdue','Completed', 'Cancelled']
            },
            {
              "label": "Expected End Date",
              "fieldname": "exp_end_date",
              "fieldtype": "Date"
            },
            {
              "label": "Color",
              "fieldname": "color",
              "fieldtype": "Color"
            },
            {
              "label": "Completed By",
              "fieldname": "completed_by",
              "fieldtype": "Link",
              "options":"User"
            },
            
            {"fieldtype":"Section Break"},
            {
              "label": "Description",
              "fieldname": "description",
              "fieldtype": "Text Editor"
            },

          ],
          primary_action: function() {
            var data = d.get_values();
            frappe.call({
              method: "cal_view_app.cal_view_app.page.calendar_view_schedu.calendar_view_schedu.update_task_details",
              args: {
                data: data,
                task: task_name
              },
              callback: function(r) {
                if(r.message) {
                } 
              }
            });
            d.hide();
          },
          primary_action_label: __('Update')
        });
        me.get_dialog_default(d, task_name)
        d.show();
      }
    })

  },//edit task close
  get_dialog_default:function(d,task_name){
    
    var val = ''
    frappe.call({
        method: "cal_view_app.cal_view_app.page.calendar_view_schedu.calendar_view_schedu.get_task_details",
        args: {name: task_name},
        async: false,
        callback: function(r) {
          if(r.message) {
            // val =r.message[fld]
            d.set_values(r.message[0])
            
          }
        }
      });

    return
  },

  new_task: function(me){
    var new_doc = frappe.model.get_new_doc("Task");
    frappe.ui.form.make_quick_entry("Task", null, null, new_doc);
  },

  delete_task: function(me){
    var me = this;
    $('.assign_task').click(function() {
      var task_name = $(this).attr("task_name")
      var exceptional_msg = "{{ no such element: str object['task_name'] }}"
      var assign_task = frappe.pages['calendar-view-schedu'].page.fields_dict.assign_task.get_value()
      if ((assign_task == "Delete Task") && (task_name) && ( task_name !=exceptional_msg)){
        frappe.confirm(__("Do you really want to delete this task?"), function () {
          frappe.call({
            method: "cal_view_app.cal_view_app.page.calendar_view_schedu.calendar_view_schedu.delete_task",
            args: {
              "task_name": task_name
            },
            callback: function(r) {
            }
          })
        })
      }
    });
  }
})//class close


function change_next_week(me){

  var filter_date =  frappe.pages['calendar-view-schedu'].page.fields_dict.date.get_value()
  var curent_week_date = new Date(filter_date)
  var next_week_date = curent_week_date.setDate(curent_week_date.getDate() + 7)
  var next_week_date = new Date(next_week_date)
  console.log(next_week_date)
  frappe.pages['calendar-view-schedu'].page.fields_dict.date.set_value(next_week_date)

}

function change_previous_week(me){

  var filter_date =  frappe.pages['calendar-view-schedu'].page.fields_dict.date.get_value()
  var curent_week_date = new Date(filter_date)
  var next_week_date = curent_week_date.setDate(curent_week_date.getDate() - 7)
  var next_week_date = new Date(next_week_date)
  console.log(next_week_date)
  frappe.pages['calendar-view-schedu'].page.fields_dict.date.set_value(next_week_date)

}



