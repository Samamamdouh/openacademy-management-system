from datetime import timedelta
from odoo import models,fields,api

class Course(models.Model):
    _name="openacademy.course"

    name = fields.Char(string="Title",required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(comodel_name="res.users", string="", index=True,ondelete='set null' )
    session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="", required=True, )
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)
